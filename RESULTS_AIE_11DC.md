# AIE_11DC Resultados S5

Dominio: fees
equipo: 01

Por qué lo elegí: Son números exactos que el cliente suele preguntar en los canales de atención como whatsapp
Cómo le fue al agente: Mejor de lo que esperaba. Varias de las preguntas tenían menciones en varios corpus y lo detectó

## Resumen de 35 casos (chunks 1500, SEARCH_TOP_K=5)

    Resumen de 41 casos (juez local):
     recall@5: 1.00   intención: 1.00   fuentes: 0.95   hechos: 0.79
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 39531 de entrada, 17364 de salida

## Prueba con chunks más chicos (800)

    Resumen de 35 casos (juez local):
     recall@5: 1.00   intención: 1.00   fuentes: 0.94   hechos: 0.84
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 33394 de entrada, 15391 de salida

## Prueba menos fragmentos SEARCH_TOP_K=3

    Resumen de 41 casos (juez local):
     recall@3: 1.00   intención: 1.00   fuentes: 0.98   hechos: 0.79
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 33577 de entrada, 16086 de salida

## Prueba más fragmentos SEARCH_TOP_K=8

    Resumen de 41 casos (juez local):
     recall@8: 1.00   intención: 1.00   fuentes: 0.95   hechos: 0.74
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 48983 de entrada, 17564 de salida

## Prueba base local, sin reranker

    Resumen de 41 casos (juez local):
     recall@3: 0.82   intención: 1.00   fuentes: 0.80   hechos: 0.71
     apoyo: 5.0/5   relevancia: 4.8/5   cita correcta: 0.9
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 30888 de entrada, 18890 de salida

## Prueba con juez azure_evaluation

    Resumen de 41 casos (juez azure_evaluation):
     recall@5: 1.00   intención: 1.00   fuentes: 0.95   hechos: 0.71
     apoyo: 5.0/5   relevancia: 4.9/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 39574 de entrada, 17553 de salida

## mejor corrida

La mejor: SEARCH_TOP_K=3 (chunks 1500, con reranker)

Por qué gana top_k=3
Tiene el mejor puntaje en fuentes (0.98) y empata con la base en hechos (0.79).
El recall@3 sigue en 1.00. El fragmento correcto siempre aparece entre los 3 primeros, así que los 2 de más que trae top_k=5 no suman nada, solo ruido.
Es más barata: gasta cerca de un 15% menos de tokens de entrada y un 7% menos de salida que la base.

##

    Resumen de 41 casos (juez azure_evaluation):
     recall@5: 1.00   intención: 1.00   fuentes: 0.95   hechos: 0.76
     apoyo: 5.0/5   relevancia: 4.9/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 39503 de entrada, 16847 de salida