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