# Implementa el veficador de ciruelas

from utils.árbol import ÁrbolSintáxisAbstracta, NodoÁrbol, TipoNodo
from generador.visitadores import VisitantePython

class Generador:

    asa            : ÁrbolSintáxisAbstracta
    visitador      : VisitantePython

    ambiente_estandar = """import sys

def hacer_menjunje(texto1, texto2):
    return texto1 + texto2

def viene_bolita(texto, indice):
    return texto[indice]

def trome(texto):
    return len(texto)

def sueltele(texto):
    print(texto)

def echandi_jiménez():
    return input()
"""

    def __init__(self, nuevo_asa: ÁrbolSintáxisAbstracta):

        self.asa            = nuevo_asa
        self.visitador      = VisitantePython() 

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()

    def generar(self):
        resultado = self.visitador.visitar(self.asa.raiz)
        print(self.ambiente_estandar)
        print(resultado)


