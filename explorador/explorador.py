# Explorador para el lenguaje Ciruelas (scanner)
from enum import Enum, auto

import re

class TipoComponente(Enum):
    """
    Enum con los tipos de componentes disponibles

    Esta clase tiene mayormente un propósito de validación
    """
    COMENTARIO = auto()
    PALABRA_CLAVE = auto()
    CONDICIONAL = auto()
    REPETICION = auto()
    ASIGNACION = auto()
    OPERADOR = auto()
    COMPARADOR = auto()
    TEXTO = auto()
    IDENTIFICADOR = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    VALOR_VERDAD = auto()
    PUNTUACION = auto()
    BLANCOS = auto()
    NINGUNO = auto()


class ComponenteLéxico:
    """
    Clase que almacena la información de un componente léxico

    Notese que no almacena información auxiliar para mostrar errores lo
    cuál es terrible
    """

    tipo    : TipoComponente
    texto   : str 

    def __init__(self, tipo_nuevo: TipoComponente, texto_nuevo: str):
        self.tipo = tipo_nuevo
        self.texto = texto_nuevo

    def __str__(self):
        """
        Da una representación en texto de la instancia actual usando un
        string de formato de python (ver 'python string formatting' en
        google)
        """

        resultado = f'{self.tipo:30} <{self.texto}>'
        return resultado

class Explorador:
    """
    Clase que lleva el proceso principal de exploración y deja listos los 
    los componentes léxicos usando para ello los descriptores de
    componente.

    Un descriptor de componente es una tupla con dos elementos:
        - El tipo de componente
        - Un string de regex que describe los textos que son generados para
          ese componente
    """

    descriptores_componentes = [ (TipoComponente.COMENTARIO, r'^Bomba:.*'),
            (TipoComponente.PALABRA_CLAVE, r'^(mae|sarpe|jefe|jefa|safis)'),
            (TipoComponente.CONDICIONAL, r'^(diay siii|sino ni modo)'),
            (TipoComponente.REPETICION, r'^(upee)'),
            (TipoComponente.ASIGNACION, r'^(metale)'),
            (TipoComponente.OPERADOR, r'^(echele|quitele|chuncherequee|desmadeje|divorcio|casorio)'),
            (TipoComponente.COMPARADOR, r'^(cañazo|poquitico|misma vara|otra vara|menos o igualitico|más o igualitico)'),
            (TipoComponente.TEXTO, r'^(~.?[^~]*)~'),
            (TipoComponente.IDENTIFICADOR, r'^([a-z]([a-zA-z0-9])*)'),
            (TipoComponente.ENTERO, r'^(-?[0-9]+)'),
            (TipoComponente.FLOTANTE, r'^(-?[0-9]+\.[0-9]+)'),
            (TipoComponente.VALOR_VERDAD, r'^(True|False)'),
            (TipoComponente.PUNTUACION, r'^([/{}()])'),
            (TipoComponente.BLANCOS, r'^(\s)*')]

    def __init__(self, contenido_archivo):
        self.texto = contenido_archivo
        self.componentes = []

    def explorar(self):
        """
        Itera sobre cada una de las líneas y las va procesando de forma que
        se generan los componentes lexicos necesarios en la etapa de
        análisis

        Esta clase no esta manejando errores de ningún tipo
        """

        for linea in self.texto:
            resultado = self.procesar_linea(linea)
            self.componentes = self.componentes + resultado

    def imprimir_componentes(self):
        """
        Imprime en pantalla en formato amigable al usuario los componentes
        léxicos creados a partir del archivo de entrada
        """

        for componente in self.componentes:
            print(componente) # Esto funciona por que el print llama al
                              # método __str__ de la instancia 


    def procesar_linea(self, linea):
        """
        Toma cada línea y la procesa extrayendo los componentes léxicos.

        Acá se deberían generar los errores y almacenar la información
        adicional necesaria para tener errores inteligentes
        """

        componentes = []

        # Toma una línea y le va cortando pedazos hasta que se acaba
        while(linea !=  ""):

            # Separa los descriptores de componente en dos variables
            for tipo_componente, regex in self.descriptores_componentes:


                # Trata de hacer match con el descriptor actual
                respuesta = re.match(regex, linea)

                # Si hay coincidencia se procede a generar el componente
                # léxico final
                if respuesta is not None :

                    # si la coincidencia corresponde a un BLANCO o un
                    # COMENTARIO se ignora por que no se ocupa
                    if tipo_componente is not TipoComponente.BLANCOS and \
                            tipo_componente is not TipoComponente.COMENTARIO:

                        #Crea el componente léxico y lo guarda
                        nuevo_componente = ComponenteLéxico(tipo_componente, respuesta.group()) 
                        componentes.append(nuevo_componente)


                    # Se elimina el pedazo que hizo match
                    linea = linea[respuesta.end():]
                    break;

        return componentes

