# Implementa el veficador de ciruelas

from utils.árbol import ÁrbolSintáxisAbstracta, NodoÁrbol, TipoNodo

class VisitantePython:

    tabuladores = 0

    def visitar(self, nodo :TipoNodo):
        """
        Este método es necesario por que uso un solo tipo de nodo para
        todas las partes del árbol por facilidad... pero cómo lo hice
        tuanis allá... pues bueno... acá hay que pagar el costo.
        """

        resultado = ''

        if nodo.tipo is TipoNodo.PROGRAMA:
            resultado = self.__visitar_programa(nodo)

        elif nodo.tipo is TipoNodo.ASIGNACIÓN:
            resultado = self.__visitar_asignación(nodo)

        elif nodo.tipo is TipoNodo.EXPRESIÓN_MATEMÁTICA:
            resultado = self.__visitar_expresión_matemática(nodo)

        elif nodo.tipo is TipoNodo.EXPRESIÓN:
            resultado = self.__visitar_expresión(nodo)

        elif nodo.tipo is TipoNodo.FUNCIÓN:
            resultado = self.__visitar_función(nodo)

        elif nodo.tipo is TipoNodo.INVOCACIÓN:
            resultado = self.__visitar_invocación(nodo)

        elif nodo.tipo is TipoNodo.PARÁMETROS_INVOCACIÓN:
            resultado = self.__visitar_parámetros_invocación(nodo)

        elif nodo.tipo is TipoNodo.PARÁMETROS_FUNCIÓN:
            resultado = self.__visitar_parámetros_función(nodo)

        elif nodo.tipo is TipoNodo.INSTRUCCIÓN:
            resultado = self.__visitar_instrucción(nodo)

        elif nodo.tipo is TipoNodo.REPETICIÓN:
            resultado = self.__visitar_repetición(nodo)

        elif nodo.tipo is TipoNodo.BIFURCACIÓN:
            resultado = self.__visitar_bifurcación(nodo)

        elif nodo.tipo is TipoNodo.DIAYSI:
            resultado = self.__visitar_diaysi(nodo)

        elif nodo.tipo is TipoNodo.SINO:
            resultado = self.__visitar_sino(nodo)

        elif nodo.tipo is TipoNodo.OPERADOR_LÓGICO:
            resultado = self.__visitar_operador_lógico(nodo)

        elif nodo.tipo is TipoNodo.CONDICIÓN:
            resultado = self.__visitar_condición(nodo)

        elif nodo.tipo is TipoNodo.COMPARACIÓN:
            resultado = self.__visitar_comparación(nodo)

        elif nodo.tipo is TipoNodo.RETORNO:
            resultado = self.__visitar_retorno(nodo)

        elif nodo.tipo is TipoNodo.ERROR:
            resultado = self.__visitar_error(nodo)

        elif nodo.tipo is TipoNodo.PRINCIPAL:
            resultado = self.__visitar_principal(nodo)

        elif nodo.tipo is TipoNodo.BLOQUE_INSTRUCCIONES:
            resultado = self.__visitar_bloque_instrucciones(nodo)

        elif nodo.tipo is TipoNodo.OPERADOR:
            resultado = self.__visitar_operador(nodo)

        elif nodo.tipo is TipoNodo.VALOR_VERDAD:
            resultado = self.__visitar_valor_verdad(nodo)

        elif nodo.tipo is TipoNodo.COMPARADOR:
            resultado = self.__visitar_comparador(nodo)

        elif nodo.tipo is TipoNodo.TEXTO:
            resultado = self.__visitar_texto(nodo)

        elif nodo.tipo is TipoNodo.ENTERO:
            resultado = self.__visitar_entero(nodo)

        elif nodo.tipo is TipoNodo.FLOTANTE:
            resultado = self.__visitar_flotante(nodo)

        elif nodo.tipo is TipoNodo.IDENTIFICADOR:
            resultado = self.__visitar_identificador(nodo)

        else:
            # Puse esta opción nada más para que se vea bonito... 
            raise Exception('En realidad nunca va a llegar acá')

        return resultado

    def __visitar_programa(self, nodo_actual):
        """
        Programa ::= (Comentario | Asignación | Función)* Principal
        """

        instrucciones = []
        # Se ignoran los comentarios

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return '\n'.join(instrucciones) 

    def __visitar_asignación(self, nodo_actual):
        """
        Asignación ::= Identificador metale (Identificador | Literal | ExpresiónMatemática | Invocación )
        """

        resultado = """{} = {}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0],instrucciones[1])

    def __visitar_expresión_matemática(self, nodo_actual):
        """
        ExpresiónMatemática ::= (Expresión) | Número | Identificador

        Ojo esto soportaría un texto
        """

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return ' '.join(instrucciones) 

    def __visitar_expresión(self, nodo_actual):
        """
        Expresión ::= ExpresiónMatemática Operador ExpresiónMatemática
        """

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return ' '.join(instrucciones) 


    def __visitar_función(self, nodo_actual):
        """
        Función ::= (Comentario)? mae Identificador (ParámetrosFunción) BloqueInstrucciones
        """

        resultado = """\ndef {}({}):\n{}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return resultado.format(instrucciones[0],instrucciones[1], '\n'.join(instrucciones[2]))

    def __visitar_invocación(self, nodo_actual):
        """
        Invocación ::= Identificador ( ParámetrosInvocación )
        """

        resultado = """{}({})"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return resultado.format(instrucciones[0], instrucciones[1])

    def __visitar_parámetros_invocación(self, nodo_actual):
        """
        ParámetrosInvocación ::= Valor (/ Valor)+
        """
        parámetros = []

        for nodo in nodo_actual.nodos:
            parámetros.append(nodo.visitar(self))

        if len(parámetros) > 0:
            return ','.join(parámetros)

        else:
            return ''


    def __visitar_parámetros_función(self, nodo_actual):
        """
        ParámetrosFunción ::= Identificador (/ Identificador)+
        """

        parámetros = []

        for nodo in nodo_actual.nodos:
            parámetros.append(nodo.visitar(self))

        if len(parámetros) > 0:
            return ','.join(parámetros)

        else:
            return ''



    def __visitar_instrucción(self, nodo_actual):
        """
        Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )
        """

        valor = ""

        for nodo in nodo_actual.nodos:
            valor = nodo.visitar(self)

        return valor


    def __visitar_repetición(self, nodo_actual):
        """
        Repetición ::= upee ( Condición ) BloqueInstrucciones
        """

        resultado = """while {}:\n{}"""

        instrucciones = []

        # Visita la condición
        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0],'\n'.join(instrucciones[1]))

    def __visitar_bifurcación(self, nodo_actual):
        """
        Bifurcación ::= DiaySi (Sino)?
        """

        resultado = """{}{}"""

        instrucciones = []

        # Visita los dos nodos en el siguiente nivel si los hay
        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0], '')

    def __visitar_diaysi(self, nodo_actual):
        """
        DiaySi ::= diay siii ( Condición ) BloqueInstrucciones
        """

        resultado = """if {}:\n{}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        return resultado.format(instrucciones[0],'\n'.join(instrucciones[1]))

    def __visitar_sino(self, nodo_actual):
        """
        Sino ::= sino ni modo BloqueInstrucciones
        """

        resultado = """else:\n  {}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return resultado.format('\n'.join(instrucciones[0]))


    def __visitar_condición(self, nodo_actual):
        """
        Condición ::= Comparación ((divorcio|casorio) Comparación)?
        """

        resultado = """{} {} {}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        if len(instrucciones) == 1:
            return resultado.format(instrucciones[0],'', '')
        else:
            return resultado.format(instrucciones[0],instrucciones[1],instrucciones[2])




    def __visitar_comparación(self, nodo_actual):
        """
        Comparación ::= Valor Comparador Valor
        """

        resultado = '{} {} {}'

        elementos = []

        # Si los 'Valor' son identificadores se asegura que existan (IDENTIFICACIÓN)
        for nodo in nodo_actual.nodos:
            elementos.append(nodo.visitar(self))

        return resultado.format(elementos[0], elementos[1], elementos[2])


    def __visitar_valor(self, nodo_actual):
        """
        Valor ::= (Identificador | Literal)
        """
        # En realidad núnca se va a visitar por que lo saqué del árbol
        # duránte la etapa de análisiss

    def __visitar_retorno(self, nodo_actual):
        """
        Retorno :: sarpe (Valor)?
        """

        resultado = 'return {}'
        valor = ''

        for nodo in nodo_actual.nodos:
            valor = nodo.visitar(self)

        return resultado.format(valor)
       
    def __visitar_error(self, nodo_actual):
        """
        Error ::= safis Valor
        """
        resultado = 'print("\033[91m", {}, "\033[0m", file=sys.stderr)'
        valor = ''

        # Verifico si 'Valor' es un identificador que exista (IDENTIFICACIÓN)
        for nodo in nodo_actual.nodos:
            valor = nodo.visitar(self)

        return resultado.format(valor)

    def __visitar_principal(self, nodo_actual):
        """
        Principal ::= (Comentario)?  (jefe | jefa) mae BloqueInstrucciones
        """
        # Este mae solo va a tener un bloque de instrucciones que tengo que
        # ir a visitar

        resultado = """\ndef principal():\n{}\n

if __name__ == '__main__':
    principal()
"""

        instrucciones = []

        # Lo pongo así por copy/paste... pero puede ser como el comentario
        # de más abajo.
        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        return resultado.format('\n'.join(instrucciones[0]))

    def __visitar_literal(self, nodo_actual):
        """
        Literal ::= (Número | Texto | ValorVerdad)
        """
        # En realidad núnca se va a visitar por que lo saqué del árbol
        # duránte la etapa de análisiss

    def __visitar_número(self, nodo_actual):
        """
        Número ::= (Entero | Flotante)
        """
        # En realidad núnca se va a visitar por que lo saqué del árbol
        # duránte la etapa de análisiss

    def __visitar_bloque_instrucciones(self, nodo_actual):
        """
        BloqueInstrucciones ::= { Instrucción+ }
        """
        self.tabuladores += 2

        instrucciones = []

        # Visita todas las instrucciones que contiene
        for nodo in nodo_actual.nodos:
            instrucciones += [nodo.visitar(self)]

        instrucciones_tabuladas = []

        for instruccion in instrucciones:
            instrucciones_tabuladas += [self.__retornar_tabuladores() + instruccion]
            

        self.tabuladores -= 2

        return instrucciones_tabuladas

    def __visitar_operador(self, nodo_actual):
        """
        Operador ::= (echele | quitele | chuncherequee | desmadeje)
        """
        if nodo_actual.contenido == 'echele':
            return '+'

        elif nodo_actual.contenido == 'quitele':
            return '-'

        elif nodo_actual.contenido == 'chuncherequee':
            return '*'

        elif nodo_actual.contenido == 'desmadeje':
            return '/'

        else:
            # Nunca llega aquí  
            return 'jijiji'


    def __visitar_valor_verdad(self, nodo_actual):
        """
        ValorVerdad ::= (True | False)
        """
        return nodo_actual.contenido
        

    def __visitar_comparador(self, nodo_actual):
        """
        Comparador ::= (cañazo | poquitico | misma vara | otra vara | menos o igualitico | más o igualitico)
        """
        if nodo_actual.contenido == 'cañazo':
            return '>'

        elif nodo_actual.contenido == 'poquitico':
            return '<'

        elif nodo_actual.contenido == 'misma vara':
            return '=='

        elif nodo_actual.contenido == 'otra vara':
            return '!='

        elif nodo_actual.contenido == 'menos o igualitico':
            return '<='

        elif nodo_actual.contenido == 'más o igualitico':
            return '>='

        else:
            # Nunca llega aquí  
            return 'jojojo'


    def __visitar_texto(self, nodo_actual):
        """
        Texto ::= ~/\w(\s\w)*)?~
        """
        return nodo_actual.contenido.replace('~', '"')

    def __visitar_entero(self, nodo_actual):
        """
        Entero ::= (-)?\d+
        """
        return nodo_actual.contenido

    def __visitar_flotante(self, nodo_actual):
        """
        Flotante ::= (-)?\d+.(-)?\d+
        """
        return nodo_actual.contenido
        

    def __visitar_identificador(self, nodo_actual):
        """
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        return nodo_actual.contenido

    def __retornar_tabuladores(self):
        return " " * self.tabuladores
