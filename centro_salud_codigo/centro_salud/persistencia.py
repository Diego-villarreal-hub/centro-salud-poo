"""Persistencia en archivos de texto: cada clase guarda sus instancias
en [NombreClase].txt (una instancia por línea, campos separados por '|')."""
import os


class Persistente:
    SEPARADOR = "|"
    CARPETA = "datos"          # carpeta donde se crean los .txt

    # ---- lo que cada clase hija debe definir ----
    def a_registro(self):
        raise NotImplementedError

    @classmethod
    def desde_registro(cls, campos):
        raise NotImplementedError

    def clave(self):
        raise NotImplementedError

    def validar(self):
        pass

    # ---- utilidades ----
    @classmethod
    def ruta(cls):
        os.makedirs(cls.CARPETA, exist_ok=True)
        return os.path.join(cls.CARPETA, f"{cls.__name__}.txt")

    def _a_linea(self):
        campos = [str(c) for c in self.a_registro()]
        for c in campos:
            if self.SEPARADOR in c or "\n" in c:
                raise ValueError(f"El valor '{c}' no puede contener '|' ni saltos de línea")
        return self.SEPARADOR.join(campos)

    @classmethod
    def _reescribir(cls, objetos):
        with open(cls.ruta(), "w", encoding="utf-8") as archivo:      # modo w
            for o in objetos:
                archivo.write(o._a_linea() + "\n")

    # ---- CRUD ----
    def guardar(self):
        """CREATE: agrega la instancia al final del archivo (modo a)."""
        self.validar()
        if type(self).buscar(self.clave()) is not None:
            raise ValueError(f"Ya existe un registro con clave '{self.clave()}' en {type(self).ruta()}")
        with open(type(self).ruta(), "a", encoding="utf-8") as archivo:
            archivo.write(self._a_linea() + "\n")

    @classmethod
    def listar(cls):
        """READ: lee todo el archivo (modo r) y devuelve una lista de objetos."""
        if not os.path.exists(cls.ruta()):
            return []
        objetos = []
        with open(cls.ruta(), "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.rstrip("\n")
                if linea:
                    objetos.append(cls.desde_registro(linea.split(cls.SEPARADOR)))
        return objetos

    @classmethod
    def buscar(cls, clave):
        for o in cls.listar():
            if o.clave() == str(clave):
                return o
        return None

    def actualizar(self):
        """UPDATE: reemplaza el registro con la misma clave y reescribe el archivo."""
        self.validar()
        objetos = type(self).listar()
        for i, o in enumerate(objetos):
            if o.clave() == self.clave():
                objetos[i] = self
                type(self)._reescribir(objetos)
                return
        raise KeyError(f"No existe un registro con clave '{self.clave()}'")

    @classmethod
    def eliminar(cls, clave):
        """DELETE: quita el registro y reescribe el archivo. Devuelve True/False."""
        objetos = cls.listar()
        restantes = [o for o in objetos if o.clave() != str(clave)]
        if len(restantes) == len(objetos):
            return False
        cls._reescribir(restantes)
        return True
