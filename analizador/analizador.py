# Analizador de Ciruelas (el lenguaje de programación)

from explorador.explorador import TipoComponente, ComponenteLéxico
from utils.árbol import ÁrbolSintáxisAbstracta, NodoÁrbol, TipoNodo

class Analizador:

    componentes_léxicos : list
    cantidad_componentes: int
    posición_componente_actual : int
    componente_actual : ComponenteLéxico

    def __init__(self, lista_componentes):

        self.componentes_léxicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)

        self.posición_componente_actual = 0
        self.componente_actual = lista_componentes[0]

        self.asa = ÁrbolSintáxisAbstracta()

    def imprimir_asa(self):
        """
        Imprime el árbol de sintáxis abstracta
        """
            
        if self.asa.raiz is None:
            print([])
        else:
            self.asa.imprimir_preorden()


    def analizar(self):
        """
        Método principal que inicia el análisis siguiendo el esquema de
        análisis por descenso recursivo
        """
        self.asa.raiz = self.__analizar_programa()


    def __analizar_programa(self):
        """
        Programa ::= (Comentario | Asignación | Función)* Principal
        """

        nodos_nuevos = []

        # Los comentarios me los paso por el quinto forro del pantalón (y
        # de todos modos el Explorador ni siquiera los guarda como
        # componentes léxicos)

        # pueden venir múltiples asignaciones o funciones
        while (True):

            # Si es asignación
            if self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
                nodos_nuevos = [self.__analizar_asignación()]

            # Si es función
            elif (self.componente_actual.texto == 'mae'):
                nodos_nuevos += [self.__analizar_función()]

            else:
                break

        # De fijo al final una función principal
        if (self.componente_actual.texto in ['jefe', 'jefa']):
            nodos_nuevos += [self.__analizar_principal()]
        else:
            raise SyntaxError(str(self.componente_actual))

        
        return NodoÁrbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos)
        

    def __analizar_asignación(self):
        """
        Asignación ::= Identificador metale ( Literal | ExpresiónMatemática | (Invocación | Identificador) )

        Acá también cambié la gramática
        """

        nodos_nuevos = []

        # El identificador en esta posición es obligatorio
        nodos_nuevos += [self.__verificar_identificador()]

        # Igual el métale
        self.__verificar('metale')


        # El siguiente bloque es de opcionales


        if self.componente_actual.tipo in [TipoComponente.ENTERO, TipoComponente.FLOTANTE, TipoComponente.VALOR_VERDAD, TipoComponente.TEXTO] :
            nodos_nuevos += [self.__analizar_literal()]

        # los paréntesis obligatorios (es un poco feo)
        elif self.componente_actual.texto == '(': 
            nodos_nuevos += [self.__analizar_expresión_matemática()]

        # Acá tengo que decidir si es Invocación o solo un identificador
        elif self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:

            if self.__componente_venidero().texto == '(':
                nodos_nuevos += [self.__analizar_invocación()]
            else:
                nodos_nuevos += [self.__verificar_identificador()]

        else:
            raise SyntaxError('Viejo... acá algo reventó', self.componente_actual)

        return NodoÁrbol(TipoNodo.ASIGNACIÓN, nodos=nodos_nuevos)


    def __analizar_expresión_matemática(self):
        """
        ExpresiónMatemática ::= (Expresión) | Número | Identificador
        """

        nodos_nuevos = []
        
        # Primera opción
        if self.componente_actual.texto == '(':

            # Los verificar no se incluyen por que son para forzar cierta
            # forma de escribir... pero no aportan nada a la semántica
            self.__verificar('(')

            nodos_nuevos += [self.__analizar_expresión()]

            self.__verificar(')')

        # Acá yo se que estan bien formados por que eso lo hizo el
        # explorador... es nada más revisar las posiciones.
        elif self.componente_actual.tipo == TipoComponente.ENTERO:
            nodos_nuevos += [self.__verificar_entero()]

        elif self.componente_actual.tipo == TipoComponente.FLOTANTE:
            nodos_nuevos += [self.__verificar_flotante()]

        # Este código se simplifica si invierto la opción anterior y esta
        else:
            nodos_nuevos += [self.__verificar_identificador()]

        return NodoÁrbol(TipoNodo.EXPRESIÓN_MATEMÁTICA, nodos=nodos_nuevos)


    def __analizar_expresión(self):
        """
        Expresión ::= ExpresiónMatemática Operador ExpresiónMatemática
        """

        nodos_nuevos = []

        # Acá no hay nada que hacer todas son obligatorias en esas
        # posiciones
        nodos_nuevos += [self.__analizar_expresión_matemática()]

        nodos_nuevos += [self.__verificar_operador()]

        nodos_nuevos += [self.__analizar_expresión_matemática()]

        return NodoÁrbol(TipoNodo.EXPRESIÓN , nodos=nodos_nuevos)

    def __analizar_función(self):
        """
        Función ::= (Comentario)? mae Identificador (ParámetrosFunción) BloqueInstrucciones
        """

        nodos_nuevos = []
        # Comentario con doble check azul dela muerte... (ignorado)

        # Esta sección es obligatoria en este orden
        self.__verificar('mae')

        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parámetros_función()]
        self.__verificar(')')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        # La función lleva el nombre del identificador
        return NodoÁrbol(TipoNodo.FUNCIÓN, \
                contenido=nodos_nuevos[0].contenido, nodos=nodos_nuevos)

    def __analizar_invocación(self):
        """
        Invocación ::= Identificador ( ParámetrosInvocación )
        """
        nodos_nuevos = []

        #todos son obligatorios en ese orden
        nodos_nuevos += [self.__verificar_identificador()]
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_parámetros_invocación()]
        self.__verificar(')')

        return NodoÁrbol(TipoNodo.INVOCACIÓN , nodos=nodos_nuevos)

    def __analizar_parámetros_función(self):
        """
        ParametrosFunción ::= Identificador (/ Identificador)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        nodos_nuevos += [self.__verificar_identificador()]

        while( self.componente_actual.texto == '/'):
            self.__verificar('/')
            nodos_nuevos += [self.__verificar_identificador()]

        # Esto funciona con lógica al verrís... Si no revienta con error
        # asumimos que todo bien y seguimos.

        return NodoÁrbol(TipoNodo.PARÁMETROS_FUNCIÓN , nodos=nodos_nuevos)

    def __analizar_parámetros_invocación(self):
        """
        ParametrosInvocación ::= Valor (/ Valor)+
        """
        nodos_nuevos = []

        # Fijo un valor tiene que haber
        nodos_nuevos += [self.__analizar_valor()]

        while( self.componente_actual.texto == '/'):
            self.__verificar('/')
            nodos_nuevos += [self.__analizar_valor()]

        # Esto funciona con lógica al verrís... Si no revienta con error
        # asumimos que todo bien y seguimos.

        return NodoÁrbol(TipoNodo.PARÁMETROS_INVOCACIÓN , nodos=nodos_nuevos)
        


    def __analizar_instrucción(self):
        """
        Instrucción ::= (Repetición | Bifurcación | Asignación | Invocación | Retorno | Error | Comentario )

        Acá hay un error en la gramática por que no reconoce las
        Invocaciones por la falta de corregir un error en la gramática LL

        Invocación y Asignación ... ambas dos inician con un Identificador
        y acá no se sabe por cuál empezar.
        ...
        La solución en código que yo presentó acá esta sería como algo así

        Instrucción ::= (Repetición | Bifurcación | (Asignación | Invocación) | Retorno | Error | Comentario )

                                                    ^                       ^
        Ojo los paréntesis extra                    |                       |
        """

        nodos_nuevos = []        


        # Acá todo con if por que son opcionales
        if self.componente_actual.texto == 'upee':
            nodos_nuevos += [self.__analizar_repetición()]

        elif self.componente_actual.texto == 'diay siii':
            nodos_nuevos += [self.__analizar_bifurcación()]

        elif self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:


            if self.__componente_venidero().texto == 'metale':
                nodos_nuevos += [self.__analizar_asignación()]
            else:
                nodos_nuevos += [self.__analizar_invocación()]

        elif self.componente_actual.texto == 'sarpe':
            nodos_nuevos += [self.__analizar_retorno()]

        else: # Muy apropiado el chiste de ir a revisar si tiene error al último.
            nodos_nuevos += [self.__analizar_error()]

        # Ignorado el comentario

        # Acá yo debería volarme el nivel Intrucción por que no aporta nada
        return NodoÁrbol(TipoNodo.INSTRUCCIÓN, nodos=nodos_nuevos)


    def __analizar_repetición(self):
        """
        Repetición ::= upee ( Condición ) BloqueInstrucciones
        """
        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('upee')
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_condición()]
        self.__verificar(')')

        # Yo acá tengo dos elecciones... creo otro nivel con Bloque de
        # instrucciones o pongo directamente las instrucciones en este
        # nivel... yo voy con la primera por facilidad... pero eso hace más
        # grande el árbol
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return NodoÁrbol(TipoNodo.REPETICIÓN, nodos=nodos_nuevos)
        

    def __analizar_bifurcación(self):
        """
        Bifurcación ::= DiaySi (Sino)?
        """
        nodos_nuevos = []

        # el sino es opcional
        nodos_nuevos += [self.__analizar_diaysi()]

        if self.componente_actual.texto == 'sino ni modo':
            nodos_nuevos += [self.__analizar_sino()]

        # y sino era solo el 'diay siii'
        return NodoÁrbol(TipoNodo.BIFURCACIÓN, nodos=nodos_nuevos)

    def __analizar_diaysi(self):
        """
        DiaySi ::= diay siii ( Condición ) BloqueInstrucciones
        """
        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('diay siii')
        self.__verificar('(')
        nodos_nuevos += [self.__analizar_condición()]
        self.__verificar(')')

        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return NodoÁrbol(TipoNodo.DIAYSI, nodos=nodos_nuevos)

    def __analizar_sino(self):
        """
        Sino ::= sino ni modo BloqueInstrucciones
        """

        nodos_nuevos = []

        # Todos presentes en ese orden... sin opciones
        self.__verificar('sino ni modo')
        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return NodoÁrbol(TipoNodo.SINO, nodos=nodos_nuevos)

    def __analizar_condición(self):
        """
        Condición ::= Comparación ((divorcio|casorio) Comparación)?
        """
        nodos_nuevos = []

        # La primera sección obligatoria la comparación
        nodos_nuevos += [self.__analizar_comparación()]

        # Esta parte es opcional
        if self.componente_actual.tipo == TipoComponente.PALABRA_CLAVE:

            # Acá estoy en problemas por que esto debió ser un nuevo nivel
            # en el árbol algo ási cómo OperadorLógico...  voy a hacer una
            # porquería... pero a ustedes les toca arreglarlo

            # opcional el AND o el OR
            if componente_actual.texto == 'divorcio':
                nodo = NodoÁrbol(TipoNodo.OPERADOR_LÓGICO, contenido='divorcio')
                nodos_nuevos += [nodo]
                self.__verificar('divorcio')


            else: # Aquí hay potencial horrible para fallo
                nodo = NodoÁrbol(TipoNodo.OPERADOR_LÓGICO, contenido='casorio')
                nodos_nuevos += [nodo]

                self.__verificar('casorio')

            # Un poco tieso, pero funcional
            nodos_nuevos += [self.__analizar_comparación()]

        # Si no ha reventado vamos bien
        return NodoÁrbol(TipoNodo.CONDICIÓN, nodos=nodos_nuevos)


    def __analizar_comparación(self):
        """
        Comparación ::= Valor Comparador Valor
        """
        nodos_nuevos = []

        # Sin opciones, todo se analiza
        nodos_nuevos += [self.__analizar_valor()]
        nodos_nuevos += [self.__verificar_comparador()]
        nodos_nuevos += [self.__analizar_valor()]

        return NodoÁrbol(TipoNodo.COMPARACIÓN, nodos=nodos_nuevos)

    def __analizar_valor(self):
        """
        Valor ::= (Identificador | Literal)
        """
        # Acá voy a cambiar el esquema de trabajo y voy a elminar algunos
        # niveles del árbol

        # El uno o el otro
        if self.componente_actual.tipo is TipoComponente.IDENTIFICADOR:
            nodo = self.__verificar_identificador()
        else:
            nodo = self.__analizar_literal()

        return nodo

    def __analizar_retorno(self):
        """
        Retorno :: sarpe (Valor)?
        """
        nodos_nuevos = []

        self.__verificar('sarpe')

        # Este hay que validarlo para evitar el error en caso de que no
        # aparezca
        if self.componente_actual.tipo in [TipoComponente.IDENTIFICADOR, TipoComponente.ENTERO, TipoComponente.FLOTANTE, TipoComponente.VALOR_VERDAD, TipoComponente.TEXTO] :
            nodos_nuevos += [self.__analizar_valor()]

        # Sino todo bien...
        return NodoÁrbol(TipoNodo.RETORNO, nodos=nodos_nuevos)

    def __analizar_error(self):
        """
        Error ::= safis Valor
        """
        nodos_nuevos = []        

        # Sin opciones
        self.__verificar('safis')
        nodos_nuevos += [self.__analizar_valor()]

        return NodoÁrbol(TipoNodo.ERROR, nodos=nodos_nuevos)

    def __analizar_principal(self):
        """
        Esta versión esta chocha por que no cumple con ser una gramática LL
        Principal ::= (Comentario)?  mae (jefe | jefa) BloqueInstrucciones
        """
        nodos_nuevos = []
        # Ya en este punto estoy harto de poner comentarios

        if self.componente_actual.texto == 'jefa':
            self.__verificar('jefa')
        else:
            self.__verificar('jefe')

        self.__verificar('mae')

        nodos_nuevos += [self.__analizar_bloque_instrucciones()]

        return NodoÁrbol(TipoNodo.PRINCIPAL, nodos=nodos_nuevos)


    def __analizar_literal(self):
        """
        Literal ::= (Número | Texto | ValorVerdad)
        """

        # Acá le voy a dar vuelta por que me da pereza tanta validación
        if self.componente_actual.tipo is TipoComponente.TEXTO:
            nodo = self.__verificar_texto()

        elif  self.componente_actual.tipo is TipoComponente.VALOR_VERDAD:
            nodo = self.__verificar_valor_verdad()

        else:
            nodo = self.__analizar_número()

        return nodo

    def __analizar_número(self):
        """
        Número ::= (Entero | Flotante)
        """
        if self.componente_actual.tipo == TipoComponente.ENTERO:
            nodo = self.__verificar_entero()
        else:
            nodo = self.__verificar_flotante()

        return nodo

    def __analizar_bloque_instrucciones(self):
        """
        Este es nuevo y me lo inventé para simplicicar un poco el código...
        correspondería actualizar la gramática.

        BloqueInstrucciones ::= { Instrucción+ }
        """
        nodos_nuevos = []

        # Obligatorio
        self.__verificar('{')

        # mínimo una
        nodos_nuevos += [self.__analizar_instrucción()]

        # Acá todo puede venir uno o más 
        while self.componente_actual.texto in ['upee', 'diay siii', 'sarpe', 'safis'] \
                or self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
        
            nodos_nuevos += [self.__analizar_instrucción()]

        # Obligatorio
        self.__verificar('}')

        return NodoÁrbol(TipoNodo.BLOQUE_INSTRUCCIONES, nodos=nodos_nuevos)

# Todos estos verificar se pueden unificar =*=
    def __verificar_operador(self):
        """
        Operador ::= (echele | quitele | chuncherequee | desmadeje)
        """
        self.__verificar_tipo_componente(TipoComponente.OPERADOR)

        nodo = NodoÁrbol(TipoNodo.OPERADOR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()

        return nodo

    def __verificar_valor_verdad(self):
        """
        ValorVerdad ::= (True | False)
        """
        self.__verificar_tipo_componente(TipoComponente.VALOR_VERDAD)

        nodo = NodoÁrbol(TipoNodo.VALOR_VERDAD, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __verificar_comparador(self):
        """
        Comparador ::= (cañazo | poquitico | misma vara | otra vara | menos o igualitico | más o igualitico)
        """
        self.__verificar_tipo_componente(TipoComponente.COMPARADOR)

        nodo = NodoÁrbol(TipoNodo.COMPARADOR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo

    def __verificar_texto(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo TEXTO

        Texto ::= ~/\w(\s\w)*)?~
        """
        self.__verificar_tipo_componente(TipoComponente.TEXTO)

        nodo = NodoÁrbol(TipoNodo.TEXTO, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar_entero(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo ENTERO

        Entero ::= (-)?\d+
        """
        self.__verificar_tipo_componente(TipoComponente.ENTERO)

        nodo = NodoÁrbol(TipoNodo.ENTERO, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar_flotante(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo FLOTANTE

        Flotante ::= (-)?\d+.(-)?\d+
        """
        self.__verificar_tipo_componente(TipoComponente.FLOTANTE)

        nodo = NodoÁrbol(TipoNodo.FLOTANTE, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar_identificador(self):
        """
        Verifica si el tipo del componente léxico actuales de tipo
        IDENTIFICADOR

        Identificador ::= [a-z][a-zA-Z0-9]+
        """
        self.__verificar_tipo_componente(TipoComponente.IDENTIFICADOR)

        nodo = NodoÁrbol(TipoNodo.IDENTIFICADOR, contenido =self.componente_actual.texto)
        self.__pasar_siguiente_componente()
        return nodo


    def __verificar(self, texto_esperado ):

        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """

        if self.componente_actual.texto != texto_esperado:
            print()
            raise SyntaxError ((texto_esperado, str(self.componente_actual)))

        self.__pasar_siguiente_componente()


    def __verificar_tipo_componente(self, tipo_esperado ):
        """
        Verifica un componente por tipo... no hace mucho pero es para
        centralizar el manejo de errores
        """

        if self.componente_actual.tipo is not tipo_esperado:
            print()
            raise SyntaxError ((tipo_esperado, str(self.componente_actual)))



    def __pasar_siguiente_componente(self):
        """
        Pasa al siguiente componente léxico

        Esto revienta por ahora
        """
        self.posición_componente_actual += 1

        if self.posición_componente_actual >= self.cantidad_componentes:
            return

        self.componente_actual = \
                self.componentes_léxicos[self.posición_componente_actual]


    def __componente_venidero(self, avance=1):
        """
        Retorna el componente léxico que está 'avance' posiciones más
        adelante... por default el siguiente. Esto sin adelantar el
        contador del componente actual.
        """
        return self.componentes_léxicos[self.posición_componente_actual+avance]
