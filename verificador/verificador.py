# Implementa el veficador de ciruelas

from utils.árbol import ÁrbolSintáxisAbstracta, NodoÁrbol, TipoNodo
from utils.tipo_datos import TipoDatos

class TablaSímbolos:
    """ 
    Almacena información auxiliar para decorar el árbol de sintáxis
    abstracta con información de tipo y alcance.

    La estructura de símbolos es una lista de diccionarios 
    """

    profundidad : int  = 0

    def abrir_bloque(self):
        """
        Inicia un bloque de alcance (scope)
        """
        self.profundidad += 1

    def cerrar_bloque(self):
        """
        Termina un bloque de alcance y al acerlo elimina todos los
        registros de la tabla que estan en ese bloque
        """

        for registro in self.símbolos:
            if registro['profundidad'] == self.profundidad:
                self.símbolos.remove(registro)

        self.profundidad -= 1

    def nuevo_registro(self, nodo, nombre_registro=''):
        """
        Introduce un nuevo registro a la tabla de símbolos
        """
        # El nombre del identificador + el nivel de profundidad 

        """
        Los atributos son: nombre, profundidad, referencia

        referencia es una referencia al nodo dentro del árbol
        (Técnicamente todo lo 'modificable (mutable)' en python es una
        referencia siempre y cuando use la POO... meh... más o menos.
        """

        diccionario = {}

        diccionario['nombre']      = nodo.contenido 
        diccionario['profundidad'] = self.profundidad
        diccionario['referencia']  = nodo

        self.símbolos.append(diccionario)

    def verificar_existencia(self, nombre):
        """
        Verficia si un identificador existe cómo variable/función global o local
        """
        for registro in self.símbolos:

            # si es local
            if registro['nombre'] == nombre and \
                    registro['profundidad'] <= self.profundidad:

                return registro

        raise Exception('Esa vara no existe', nombre)

    def __str__(self):

        resultado = 'TABLA DE SÍMBOLOS\n\n'
        resultado += 'Profundidad: ' + str(self.profundidad) +'\n\n'
        for registro in self.símbolos:
            resultado += str(registro) + '\n'

        return resultado


class Visitante:

    tabla_símbolos: TablaSímbolos

    def __init__(self, nueva_tabla_símbolos):
        self.tabla_símbolos = nueva_tabla_símbolos 

    def visitar(self, nodo :TipoNodo):
        """
        Este método es necesario por que uso un solo tipo de nodo para
        todas las partes del árbol por facilidad... pero cómo lo hice
        tuanis allá... pues bueno... acá hay que pagar el costo.
        """

        if nodo.tipo is TipoNodo.PROGRAMA:
            self.__visitar_programa(nodo)

        elif nodo.tipo is TipoNodo.ASIGNACIÓN:
            self.__visitar_asignación(nodo)

        elif nodo.tipo is TipoNodo.EXPRESIÓN_MATEMÁTICA:
            self.__visitar_expresión_matemática(nodo)

        elif nodo.tipo is TipoNodo.EXPRESIÓN:
            self.__visitar_expresión(nodo)

        elif nodo.tipo is TipoNodo.FUNCIÓN:
            self.__visitar_función(nodo)

        elif nodo.tipo is TipoNodo.INVOCACIÓN:
            self.__visitar_invocación(nodo)

        elif nodo.tipo is TipoNodo.PARÁMETROS_INVOCACIÓN:
            self.__visitar_parámetros_invocación(nodo)

        elif nodo.tipo is TipoNodo.PARÁMETROS_FUNCIÓN:
            self.__visitar_parámetros_función(nodo)

        elif nodo.tipo is TipoNodo.INSTRUCCIÓN:
            self.__visitar_instrucción(nodo)

        elif nodo.tipo is TipoNodo.REPETICIÓN:
            self.__visitar_repetición(nodo)

        elif nodo.tipo is TipoNodo.BIFURCACIÓN:
            self.__visitar_bifurcación(nodo)

        elif nodo.tipo is TipoNodo.DIAYSI:
            self.__visitar_diaysi(nodo)

        elif nodo.tipo is TipoNodo.SINO:
            self.__visitar_sino(nodo)

        elif nodo.tipo is TipoNodo.OPERADOR_LÓGICO:
            self.__visitar_operador_lógico(nodo)

        elif nodo.tipo is TipoNodo.CONDICIÓN:
            self.__visitar_condición(nodo)

        elif nodo.tipo is TipoNodo.COMPARACIÓN:
            self.__visitar_comparación(nodo)

        elif nodo.tipo is TipoNodo.RETORNO:
            self.__visitar_retorno(nodo)

        elif nodo.tipo is TipoNodo.ERROR:
            self.__visitar_error(nodo)

        elif nodo.tipo is TipoNodo.PRINCIPAL:
            self.__visitar_principal(nodo)

        elif nodo.tipo is TipoNodo.BLOQUE_INSTRUCCIONES:
            self.__visitar_bloque_instrucciones(nodo)

        elif nodo.tipo is TipoNodo.OPERADOR:
            self.__visitar_operador(nodo)

        elif nodo.tipo is TipoNodo.VALOR_VERDAD:
            self.__visitar_valor_verdad(nodo)

        elif nodo.tipo is TipoNodo.COMPARADOR:
            self.__visitar_comparador(nodo)

        elif nodo.tipo is TipoNodo.TEXTO:
            self.__visitar_texto(nodo)

        elif nodo.tipo is TipoNodo.ENTERO:
            self.__visitar_entero(nodo)

        elif nodo.tipo is TipoNodo.FLOTANTE:
            self.__visitar_flotante(nodo)

        elif nodo.tipo is TipoNodo.IDENTIFICADOR:
            self.__visitar_identificador(nodo)

        else:
            # Puse esta opción nada más para que se vea bonito... 
            raise Exception('En realidad nunca va a llegar acá')

    def __visitar_programa(self, nodo_actual):
        """
        Programa ::= (Comentario | Asignación | Función)* Principal
        """
        for nodo in nodo_actual.nodos:
            # acá 'self' quiere decir que al método 'visitar' le paso el
            # objetto visitante que estoy usando (o sea, este mismo...
            # self)
            nodo.visitar(self)

    def __visitar_asignación(self, nodo_actual):
        """
        Asignación ::= Identificador metale (Identificador | Literal | ExpresiónMatemática | Invocación )
        """
        # Metó la información en la tabla de símbolos (IDENTIFICACIÓN)
        self.tabla_símbolos.nuevo_registro(nodo_actual.nodos[0])

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # Si es una función verifico el tipo que retorna para incluirlo en
        # la asignación y si es un literal puedo anotar el tipo (TIPO) 

        nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']

        nodo_actual.nodos[0].atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']


    def __visitar_expresión_matemática(self, nodo_actual):
        """
        ExpresiónMatemática ::= (Expresión) | Número | Identificador

        Ojo esto soportaría un texto
        """
        for nodo in nodo_actual.nodos:

            # Verifico que exista si es un identificador (IDENTIFICACIÓN)
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_símbolos.verificar_existencia(nodo.contenido)

            nodo.visitar(self)

        # Anoto el tipo de datos 'NÚMERO' (TIPO)
        nodo_actual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitar_expresión(self, nodo_actual):
        """
        Expresión ::= ExpresiónMatemática Operador ExpresiónMatemática
        """
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # Anoto el tipo de datos 'NÚMERO' (TIPO)
        nodo_actual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitar_función(self, nodo_actual):
        """
        Función ::= (Comentario)? mae Identificador (ParámetrosFunción) BloqueInstrucciones
        """

        # Meto la función en la tabla de símbolos (IDENTIFICACIÓN)
        self.tabla_símbolos.nuevo_registro(nodo_actual)

        self.tabla_símbolos.abrir_bloque()

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        self.tabla_símbolos.cerrar_bloque()

        # Anoto el tipo de retorno (TIPO)
        nodo_actual.atributos['tipo'] = nodo_actual.nodos[2].atributos['tipo']


    def __visitar_invocación(self, nodo_actual):
        """
        Invocación ::= Identificador ( ParámetrosInvocación )
        """

        # Verfica que el 'Identificador' exista (IDENTIFICACIÓN) y que sea
        registro = self.tabla_símbolos.verificar_existencia(nodo_actual.nodos[0].contenido)

        if registro['referencia'].tipo != TipoNodo.FUNCIÓN:
            raise Exception('Esa vara es una variable...', registro)

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # El tipo resultado de la invocación es el tipo inferido de una
        # función previamente definida
        nodo_actual.atributos['tipo'] = registro['referencia'].atributos['tipo']


    def __visitar_parámetros_invocación(self, nodo_actual):
        """
        ParámetrosInvocación ::= Valor (/ Valor)+
        """

        # Recordemos que 'Valor' no existe en el árbol...

        # Si es 'Identificador' verifico que exista (IDENTIFICACIÓN)
        for nodo in nodo_actual.nodos:

            # Si existe y no es función ya viene con el tipo por que
            # fue producto de una asignación
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_símbolos.verificar_existencia(nodo.contenido)

            elif nodo.tipo == TipoNodo.FUNCIÓN:
                raise Exception('Esa vara es una función...', nodo.contenido) 

            # Si es número o texto nada más los visito
            nodo.visitar(self)

        # No hay tipos en los parámetros... se sabe en tiempo de ejecución


    def __visitar_parámetros_función(self, nodo_actual):
        """
        ParámetrosFunción ::= Identificador (/ Identificador)+
        """

        # Registro cada 'Identificador' en la tabla
        for nodo in nodo_actual.nodos:
                self.tabla_símbolos.nuevo_registro(nodo)
                nodo.visitar(self)


    def __visitar_instrucción(self, nodo_actual):
        """
        Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )
        """
        # Por alguna razón no me volé este nivel.. así que lo visitamos... 
        # Esto es un desperdicio de memoria y de cpu

        # Visita la instrucción 

        # Lo pongo así por copy/paste... pero puede ser como el comentario
        # de más abajo.
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)
            nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

        # nodo_actual.nodos[0].visitar(self)

    def __visitar_repetición(self, nodo_actual):
        """
        Repetición ::= upee ( Condición ) BloqueInstrucciones
        """
        # Visita la condición


        # Visita el bloque de instrucciones

        # Lo pongo así por copy/paste... pero puede ser como el comentario
        # de más abajo.
        self.tabla_símbolos.abrir_bloque()

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # nodo_actual.nodos[0].visitar(self)

        self.tabla_símbolos.cerrar_bloque()

        # Anoto el tipo de retorno (TIPO)
        nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']


    def __visitar_bifurcación(self, nodo_actual):
        """
        Bifurcación ::= DiaySi (Sino)?
        """

        # Visita los dos nodos en el siguiente nivel si los hay
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        nodo_actual.atributos['tipo'] = TipoDatos.CUALQUIERA 

    def __visitar_diaysi(self, nodo_actual):
        """
        DiaySi ::= diay siii ( Condición ) BloqueInstrucciones
        """


        # Visita la condición


        # Visita el bloque de instrucciones

        # Lo pongo así por copy/paste... pero puede ser como el comentario
        # de más abajo.
        self.tabla_símbolos.abrir_bloque()

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # nodo_actual.nodos[0].visitar(self)

        self.tabla_símbolos.cerrar_bloque()

        # Anoto el tipo de retorno (TIPO)
        nodo_actual.atributos['tipo'] = nodo_actual.nodos[1].atributos['tipo']

    def __visitar_sino(self, nodo_actual):
        """
        Sino ::= sino ni modo BloqueInstrucciones
        """
        # Visita el bloque de instrucciones

        # Lo pongo así por copy/paste... pero puede ser como el comentario
        # de más abajo.
        self.tabla_símbolos.abrir_bloque()

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # nodo_actual.nodos[0].visitar(self)

        self.tabla_símbolos.cerrar_bloque()

        # Anoto el tipo de retorno (TIPO)
        nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']

    def __visitar_condición(self, nodo_actual):
        """
        Condición ::= Comparación ((divorcio|casorio) Comparación)?
        """

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # Comparación retorna un valor de verdad (TIPO)
        nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD


    def __visitar_comparación(self, nodo_actual):
        """
        Comparación ::= Valor Comparador Valor
        """

        # Si los 'Valor' son identificadores se asegura que existan (IDENTIFICACIÓN)
        for nodo in nodo_actual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                registro = self.tabla_símbolos.verificar_existencia(nodo.contenido)

            nodo.visitar(self)


        # Verifico que los tipos coincidan (TIPO)
        valor_izq      = nodo_actual.nodos[0]
        comparador  = nodo_actual.nodos[1]
        valor_der      = nodo_actual.nodos[2]
        # Ya se que eso se ve sueltelefeo... pero ya el cerebro se me apagó...

        if valor_izq.atributos['tipo'] == valor_der.atributos['tipo']:
            comparador.atributos['tipo'] = valor_izq.atributos['tipo']

            # Una comparación siempre tiene un valor de verdad
            nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

        # Caso especial loco: Si alguno de los dos es un identificador de
        # un parámetro de función no puedo saber que tipo tiene o va a
        # tener por que este lenguaje no es tipado... tons vamos a poner
        # que la comparación puede ser cualquiera
        elif valor_izq.atributos['tipo'] == TipoDatos.CUALQUIERA or \
                valor_der.atributos['tipo'] == TipoDatos.CUALQUIERA:

            comparador.atributos['tipo'] = TipoDatos.CUALQUIERA

            # Todavía no estoy seguro.
            nodo_actual.atributos['tipo'] = TipoDatos.CUALQUIERA

        else:
            raise Exception('Papo, algo tronó acá', str(nodo_actual))


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

        for nodo in nodo_actual.nodos:
            nodo.visitar(self)
        
        if nodo_actual.nodos == []:
            # Si no retorna un valor no retorna un tipo específico 
            nodo_actual.atributos['tipo'] = TipoDatos.NINGUNO

        else:

            for nodo in nodo_actual.nodos:

                nodo.visitar(self)

                if nodo.tipo == TipoNodo.IDENTIFICADOR:
                    # Verifico si valor es un identificador que exista (IDENTIFICACIÓN)
                    registro = self.tabla_símbolos.verificar_existencia(nodo.contenido)

                    # le doy al sarpe el tipo de retorno del identificador encontrado
                    nodo_actual.atributos['tipo'] = registro['referencia'].atributos['tipo']

                else:
                    # Verifico si es un Literal de que tipo es (TIPO)
                    nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitar_error(self, nodo_actual):
        """
        Error ::= safis Valor
        """
        # Verifico si 'Valor' es un identificador que exista (IDENTIFICACIÓN)
        for nodo in nodo_actual.nodos:
            if nodo.tipo == TipoNodo.IDENTIFICADOR:
                self.tabla_símbolos.verificar_existencia(nodo.contenido)

        # Un safis imprime a stderr y sigue sin retornar nada
        nodo_actual.atributos['tipo'] = TipoDatos.NINGUNO 


    def __visitar_principal(self, nodo_actual):
        """
        Principal ::= (Comentario)?  (jefe | jefa) mae BloqueInstrucciones
        """
        # Este mae solo va a tener un bloque de instrucciones que tengo que
        # ir a visitar

        # Lo pongo así por copy/paste... pero puede ser como el comentario
        # de más abajo.
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # nodo_actual.nodos[0].visitar(self)

        # Anoto el tipo de retorno (TIPO)
        nodo_actual.atributos['tipo'] = nodo_actual.nodos[0].atributos['tipo']

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
        # Visita todas las instrucciones que contiene
        for nodo in nodo_actual.nodos:
            nodo.visitar(self)

        # Acá yo debería agarrar el tipo de datos del Retorno si lo hay
        nodo_actual.atributos['tipo'] = TipoDatos.NINGUNO 

        for nodo in nodo_actual.nodos:
            if nodo.atributos['tipo'] != TipoDatos.NINGUNO:
                nodo_actual.atributos['tipo'] = nodo.atributos['tipo']

    def __visitar_operador(self, nodo_actual):
        """
        Operador ::= (hechele | quitele | chuncherequee | desmadeje)
        """
        # Operador para trabajar con números (TIPO)
        nodo_actual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitar_valor_verdad(self, nodo_actual):
        """
        ValorVerdad ::= (True | False)
        """
        # Valor de verdad (TIPO)
        nodo_actual.atributos['tipo'] = TipoDatos.VALOR_VERDAD

    def __visitar_comparador(self, nodo_actual):
        """
        Comparador ::= (cañazo | poquitico | misma vara | otra vara | menos o igualitico | más o igualitico)
        """
        # Estos comparadores son numéricos  (TIPO) 
        # (cañazo | poquitico | misma vara | otra vara | menos o igualitico | más o igualitico)
        if nodo_actual.contenido not in ['misma vara', 'otra vara' ]:
            nodo_actual.atributos['tipo'] = TipoDatos.NÚMERO

        else:
            nodo_actual.atributos['tipo'] = TipoDatos.CUALQUIERA
            # Si no es alguno de esos puede ser Numérico o texto y no lo puedo
            # inferir todavía


    def __visitar_texto(self, nodo_actual):
        """
        Texto ::= ~/\w(\s\w)*)?~
        """
        # Texto (TIPO)
        nodo_actual.atributos['tipo'] = TipoDatos.TEXTO

    def __visitar_entero(self, nodo_actual):
        """
        Entero ::= (-)?\d+
        """
        # Entero (TIPO) 
        nodo_actual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitar_flotante(self, nodo_actual):
        """
        Flotante ::= (-)?\d+.(-)?\d+
        """
        # Flotante (TIPO) 
        nodo_actual.atributos['tipo'] = TipoDatos.NÚMERO

    def __visitar_identificador(self, nodo_actual):
        """
        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        nodo_actual.atributos['tipo'] = TipoDatos.CUALQUIERA
        # No hace nada


class Verificador:

    asa            : ÁrbolSintáxisAbstracta
    visitador      : Visitante
    tabla_símbolos : TablaSímbolos

    def __init__(self, nuevo_asa: ÁrbolSintáxisAbstracta):

        self.asa            = nuevo_asa

        self.tabla_símbolos = TablaSímbolos()
        self.__cargar_ambiente_estándar()

        self.visitador      = Visitante(self.tabla_símbolos)

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()

    def __cargar_ambiente_estándar(self):

        funciones_estandar = [ ('hacer_menjunje', TipoDatos.NINGUNO),
                ('viene_bolita', TipoDatos.TEXTO),
                ('trome', TipoDatos.NÚMERO),
                ('sueltele', TipoDatos.NINGUNO),
                ('echandi_jiménez', TipoDatos.TEXTO)]

        for nombre, tipo in  funciones_estandar:
            nodo = NodoÁrbol(TipoNodo.FUNCIÓN, contenido=nombre, atributos= {'tipo': tipo})
            self.tabla_símbolos.nuevo_registro(nodo)

    def verificar(self):
        self.visitador.visitar(self.asa.raiz)






