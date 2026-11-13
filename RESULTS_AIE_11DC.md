# AIE_11DC Resultados S5

Dominio: fees
equipo: 01

## Resumen de 35 casos

    Resumen de 35 casos (juez local):
     recall@5: 1.00   intención: 1.00   fuentes: 0.94   hechos: 0.78
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 33392 de entrada, 14791 de salida

Por qué lo elegí: Son números exactos que el cliente suele preguntar en los canales de atención como whatsapp
Cómo le fue al agente: Mejor de lo que esperaba. Varias de las preguntas tenían menciones en varios corpus y lo detectó

## Prueba con chunks de 800

    Resumen de 35 casos (juez local):
     recall@5: 1.00   intención: 1.00   fuentes: 0.94   hechos: 0.84
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 33394 de entrada, 15391 de salida

## Prueba con SEARCH_TOP_K=8

    Resumen de 35 casos (juez local):
     recall@8: 1.00   intención: 1.00   fuentes: 0.94   hechos: 0.78
     apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
     fugas de datos personales: 0   citas de fuentes prohibidas: 1
     tokens: 41873 de entrada, 15133 de salida
