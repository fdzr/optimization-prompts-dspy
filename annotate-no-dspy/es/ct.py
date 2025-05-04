PROMPT = """
    Eres una herramienta de anotación de datos textuales altamente entrenada, capaz de proporcionar respuestas
    subjetivas. Evalúa la similitud semántica de la palabra objetivo en estas oraciones 1 y 2. Considera solo los objetos/conceptos
    a los que se refieren las palabras: ¡Ignora cualquier etimología común y similitud metafórica! ¡Ignora mayúsculas!
    ¡Ignora número (gato/Gatos = significado idéntico)! Los homónimos (como murciélago el animal vs murciélago en béisbol)
    se consideran no relacionados. De como salida una calificación numérica: 1 es no relacionado; 2 es lejanamente relacionado; 3 es
    estrechamente relacionado; 4 es significado idéntico. Tu respuesta debe alinearse con el juicio sucinto de un humano.
    
    Ejemplo:
        palabra objetivo: planta
        primera oracion: Las plantas sembradas en el jardin, brotan un inmenso aroma.
        segunda oracion: Las plantas de carbon son capaces de generar energia electrica
                    para toda una ciudad

        Score: 1, razonemos paso a paso en este caso la anotacion es 1 porque en  la primera oracion planta esta relacionada
            a los arboles, flores, y en la segunda oracion planta esta relacionada a industrias, fabricas, el significado es
            no esta relacionado.
            
    Ejemplo:
        palabra objetivo: arbol
        primera oracion: Un arbol binario es una estructura de datos para almacenas datos organizados.
        segunda oracion: Los arboles de ese bosque son ricos en aroma y colores.
        
        Score: 2, razonemos paso a paso en este caso la anotacion es 2 porque en la primera oracion arbol significa estructura de datos en la computacion y
        en la segunda oracion arboles significa la planta que tiene hojas, el significado es lejanamente relacionado
        porque ellos comparten la forma de un arbol pero en un caso es una estructura de datps y en la segunda oracion
        es un arbol.
        
    Ejemplo: 
        palabra objetivo: celda
        primera oracion: Con este conocido programa podremos manipular los datos a traves de sus celdas.
        segunda oracion: Como resultados de dicho analisis vamos a obtener un mapa diferente, un mapa
                    donde cada celda visible nos viene con un numero de 0 o 180 grados.

        Score: 3, razonemos paso a paso en este caso la anotacion es 3 porque en la primera oracion el significado de celda es
            relacionado a cuadriculas donde usted puede poner informacion  y en la segunda oraicon el significado esta relacionado ademas
            a cuadriculas donde puedes juntar informacion, no es 4 porque los significados difieren en que en una
            oracion se usan en u programa y en la otra oracion se usan en unn mapa.
            
    Ejemplo:
        palara objetivo: caballo
        primera oracion: El caballo blanco de Marti galopa sin parar hasta la victoria.
        segunda oracion: Los caballos cuando estan en manada se protegen los unos a los otros.

        Score: 4, razonemos paso a paso en este caso, la anotacion es 4 porque en embas oraciones, el significado de
            caballo y caballos estan relacionados al animal. Por favor note que caballo esta en singular y caballos
            esta en plural y no afecta la anotacion.
    
    Dada la siguiente puntuación de pares de frases según lo explicado, dé
    sólo un valor numérico como respuesta y no explique el porqué de la puntuación elegida:
    
    primera oracion: {sentence1}
    segunda oracion: {sentence2}
    palabra objetivo: {target_word}
    score:

"""
