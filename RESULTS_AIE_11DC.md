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
| Tools pedidas en la consulta | get_charged_fees(customer_id=CUS-1001) | get_charged_fees(customer_id=CUS-1001)|
| La acción sensible quedó **NO SE EJECUTA** | NO SE EJECUTA, pendiente de aprobación "status": "pendiente_aprobacion" | NO SE EJECUTA, pendiente de aprobación "status": "pendiente_aprobacion" |
| Pregunta de memoria respondida sin `→` | Si, "Su código de cliente es CUS-1001. Usted pidió la devolución de la comisión FEE-4002 (Mantenimiento de cuenta — S/12.00 — 01/10/2026). La solicitud quedó pendiente de aprobación por un asesor." | Si, Su código de cliente es CUS-1001. Usted pidió la devolución de la comisión FEE-4002 — Mantenimiento de cuenta — S/ 12.00 (01/10/2026). La solicitud está pendiente de aprobación por un asesor. |
| Primer texto (ms) | 16370 ms | 16931 ms  |
| Respuesta completa (ms) | 16512 ms | 17070 ms |
| Tokens (entrada / salida) | 2723/1749 | 2924/1430 |

### ¿La skill frenó la tool de otro dominio?

Mensaje: ¿Dónde hay una agencia en Miraflores?. Respuesta: Agente [out_of_scope]: Lo siento, eso está fuera del alcance de este agente de comisiones. Puedo ayudar con comisiones, tarifas, ITF y devoluciones. Para ubicar una agencia en Miraflores, consulte la web o la app del Banco Demo o contacte atención al cliente desde esos canales..

### Diferencias entre los dos runtimes

A simple vista, el runtime agent framework utiliza mas token y consume mayor tiempo en las respuestas. Al nivel de las respuestas, ambos runtime tienen la misma calidad de respuesta. El detalle mas importante es la memoria, que permite al agent framework reducir cantidad de llamadas a los tools.

### Conclusión

En casos donde importe mas el tiempo de respuesta y consumo de token, un runtime local como react es factible y puede ser beneficioso. Pero si se busca reducción de llamadas y que con la memoria pueda dar mejores respuestas, utilizar en agent framework es superior.