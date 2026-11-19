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


## Sesión 7 — Skills, memoria de trabajo y Agent Framework

Dominio: `fees`. La misma conversación con los dos runtimes (paso 7).

| | `react` | `agent_framework` |
|---|---|---|
| Tools pedidas en la consulta | 3 tools | 3 tools |
| La acción sensible quedó **NO SE EJECUTA** | NO SE EJECUTA, pendiente de aprobación "status": "pendiente_aprobacion" | NO SE EJECUTA, pendiente de aprobación "status": "pendiente_aprobacion" |
| Pregunta de memoria respondida sin `→` | _(anotar)_ | _(anotar)_ |
| Primer texto (ms) | 19538ms | 22464ms |
| Respuesta completa (ms) | 19959ms | 22899ms |
| Tokens (entrada / salida) | 3150/1281 | 3150/2117 |

### ¿La skill frenó la tool de otro dominio?

Mensaje: ¿Dónde hay una agencia en Miraflores?. Respuesta: Agente [out_of_scope]: Lo siento, eso está fuera del alcance de este agente de comisiones. Puedo ayudar con comisiones, tarifas, ITF y devoluciones. Para ubicar una agencia en Miraflores, consulte la web o la app del Banco Demo o contacte atención al cliente desde esos canales..

### Diferencias entre los dos runtimes

El runtime agent_framework al tener memoria puede adaptarse a la pregunta, respondiendo de otra manera, aun respetando las reglas pero con mayor conocimiento.

### Conclusión

El tener memoria mejora los agentes al poder dar una respuesta personalizada. Esto tiene desventajas como la respuesta no ser deterministica, pero gracias a los guard se puede tener un agente que siga en parámetros.