PROMPT = """
    Eres una herramienta de anotación de datos textuales altamente entrenada, capaz de proporcionar respuestas
    subjetivas. Evalúa la similitud semántica de la palabra objetivo en estas oraciones 1 y 2. Considera solo los objetos/conceptos
    a los que se refieren las palabras: ¡Ignora cualquier etimología común y similitud metafórica! ¡Ignora mayúsculas!
    ¡Ignora número (gato/Gatos = significado idéntico)! Los homónimos (como murciélago el animal vs murciélago en béisbol)
    se consideran no relacionados. De como salida una calificación numérica: 1 es no relacionado; 2 es lejanamente relacionado; 3 es
    estrechamente relacionado; 4 es significado idéntico. Tu respuesta debe alinearse con el juicio sucinto de un humano.
    
    Ejemplos de oraciones por cada anotacion
    
    Ejemplo:
        palabra objetivo: vela
        primera oracion: Encendí una vela para iluminar la habitación durante el apagón.
        segunda oracion: La vela del barco se hinchó con el viento, llevándonos rápidamente hacia el horizonte.
        Score:
    
    Ejemplo:
        palabra objetivo: encrucijada
        primera oracion: Llegó a una encrucijada y leyó las señales; al sur, Kenniston, 20 millas.
        segunda oracion: Como resultado, estamos en una encrucijada; o se abandonarán los esfuerzos de
            integración escolar en el Sur, o se llevarán a cabo en el Norte también.
        Score: 2
    
    Ejemplo:
        palabra objetivo: niño
        primera oracion: Él estuvo de acuerdo y comenzó a practicar sus trucos de prestidigitación para el gran placer
            de algunos niños, los mismos, sospecho, que me habían atormentado cuando era niño.
        segunda oracion: La luz del día había desaparecido hacía tiempo; su niño yacía tranquilamente durmiendo a su lado;
            una vela ardía débilmente en el soporte.
        Score: 3
    
    Ejemplo:
        palabra objetivo: comer
        primera oracion: Hablando de pan y mantequilla, me recuerda que es mejor que comamos el nuestro antes de que el
            café se enfríe del todo.
        segunda oracion: Cuando la comida terminó y habían terminado su té después de comer, Wang el Segundo llevó al hombre de 
            confianza a la puerta de su hermano mayor.
        Score: 4
    
    Dada la siguiente puntuación de pares de frases según lo explicado, dé
    sólo un valor numérico como respuesta y no explique el porqué de la puntuación elegida:
    
    primera oracion: {sentence1}
    segunda oracion: {sentence2}
    palabra objetivo: {target_word}
    score:
"""
