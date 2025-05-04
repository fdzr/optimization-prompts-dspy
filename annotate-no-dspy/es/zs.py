PROMPT = """
    Eres una herramienta de anotación de datos textuales altamente entrenada, capaz de proporcionar respuestas
    subjetivas. Evalúa la similitud semántica de la palabra objetivo en estas oraciones 1 y 2. Considera solo los objetos/conceptos
    a los que se refieren las palabras: ¡Ignora cualquier etimología común y similitud metafórica! ¡Ignora mayúsculas!
    ¡Ignora número (gato/Gatos = significado idéntico)! Los homónimos (como murciélago el animal vs murciélago en béisbol)
    se consideran no relacionados. De como salida una calificación numérica: 1 es no relacionado; 2 es lejanamente relacionado; 3 es
    estrechamente relacionado; 4 es significado idéntico. Tu respuesta debe alinearse con el juicio sucinto de un humano.
    
    Dada la siguiente puntuación de pares de frases según lo explicado, dé
    sólo un valor numérico como respuesta y no explique el porqué de la puntuación elegida:
    
    primera oracion: {sentence1}
    segunda oracion: {sentence2}
    palabra objetivo: {target_word}
    score:
"""
