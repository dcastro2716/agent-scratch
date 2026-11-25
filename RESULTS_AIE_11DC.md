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

## Sesión 6 — Tools del MCP en el chat

Dominio: `fees`. MCP: el mock (`http://127.0.0.1:8200/mcp`) y, si ya tienes `MCP_URL`, el compartido (`bank-mcp`).

### Tools de tu dominio

| MCP | Tools que lista `dev/mcp/mcp_tools.py` |
|---|---|
| Mock | get_charged_fees, get_transactions, request_fee_refund |
| Compartido | get_charged_fees, get_transactions, request_fee_refund |

### Conversación en `dev/chat.py` (paso 12)

| Prueba | Mensaje | Tool pedida (`→`) | Qué pasó | Primer texto / respuesta completa (ms) |
|---|---|---|---|---|
| Consulta de tu dominio | Soy CUS-1001, ¿por qué me cobraron comisiones este mes? ¿Alguna se puede devolver? | get_charged_fees(customer_id=CUS-1001) | El agente obtuvo la información de los cobros, identificó cual podía devolverse (a diferencia del mock) y ofrecía registrar la solicitud de devoluciónx | 16766 ms / 17855 ms|
| Acción confirmada | Sí, pide la devolución de esa, el motivo es cobro indebido | request_fee_refund(fee_id=FEE-4002, reason=cobro indebido)| Devolvió: NO SE EJECUTA, pendiente de aprobación: {"status": "pendiente_aprobacion", "detail": "Acción sensible: no se ejecutó ni se registró todavía. Dile al cliente que la pediste y que un asesor la va a revizar y eso fue lo que hizo el agente y le dio los tiempos | 31523 ms / 31672 ms |
| Sin tool que la resuelva | cual es la sede mas cercana | [out_of_scope] | el agente identificó que la pregunta estaba fuera de su ambito y dio recomendaciones de cómo encontrar una respuesta | 12699 ms / 12844 ms |
| Tool de otro dominio | Soy CUS-1001, ¿puedo subir la línea de mi tarjeta CRD-2001 a 4000?| [out_of_scope] (get_credit_line) | identificó que la pregunta está fuera del ambito de comisiones y mando a centro de ayuda| 12762 ms / 12917 ms |

### ¿El modelo inventó algún dato cuando ninguna tool lo resolvía?

No, trabajó con la información y tools de comisiones que tenía. Si intento ayudar cuando se pregunto sobre una sede, incluso diciendo que utilices google maps. Eso si esta fuera del ambito de comisiones. Cuando se le preguntó sobre otro dominio, mandó a centro de ayuda.

### Conclusión

El agente es capaz de obtener las tools que puede utilizar y solo las que debe usar. Es capaz de determinar en base a la solicitud del usuario si es necesario invocar una tool y como componer la peticion. 

También es capaz de terminar que solicitudes del usuario están fuera de su ambito y es capaz de recomendar en base a la pregunta por donde el cliente debe buscar o continuar con su solicitud.

También puede determinar cuales son sensibles y requieren que un humano esté involucrado.

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


## Sesión 8 — Aprobación humana, validación y reintentos

Dominio: `fees` (paso 6).

| Caso | Runtime | Mensaje | Qué pasó | Resultado o ID |
|---|---|---|---|---|
| Aprobar | `agent_framework` | He registrado la solicitud de devolución RFD-9002 para la comisión FEE-4002 con motivo “cobro indebido”. La solicitud está registrada para que el banco la procese; no se ha aplicado el reembolso.| se pidió aprobación del asesor y al ser aprobada realizó la devolución | resultado: {"id": "RFD-9002", "fee_id": "FEE-4002", "status": "registered", "reason": "cobro indebido"}|
| Rechazar | `react` | El asesor rechazó la solicitud de devolución; la acción no se ejecutó. | no se ejecuta la acción, en este caso la devolución | rechazada por el asesor: {"status": "rechazada", "detail": "El asesor rechazó la acción: no se ejecutó."} |
| Error de negocio (`CUS-9999`) | `agent_framework` |  No encuentro el código CUS-9999 en nuestro sistema. Confirme por favor su código de cliente (formato CUS-xxxx) o indique el correcto para que pueda consultar las comisiones. | el mcp devolvio error al invocar get_charged_feeds al no existir el usuario| error: {"error": "El cliente CUS-9999 no existe"}|
| Input inválido | `agent_framework` | Necesito su código de cliente en formato CUS-xxxx (por ejemplo: CUS-1001). Confirme el código para que pueda consultar las comisiones cobradas. | en este caso no se llego a invocar al mcp, sino fallo en la validacion de la data ya que el codigo del cliente no tiene el formato correcto| (primer texto en 17075 ms, respuesta completa en 17237 ms, 3543 tokens de entrada, 1449 de salida) |

### La trayectoria en el log
Aprobar
INFO agent.application.chat_service: trayectoria 18add1a9-74be-447e-bb97-2ace4f7107d6: request_fee_refund pending_approval → respuesta sensitive_action
INFO agent.application.chat_service: trayectoria 18add1a9-74be-447e-bb97-2ace4f7107d6: decisión del asesor → request_fee_refund ok

Rechazar
INFO agent.application.chat_service: trayectoria a73ccf5c-80f6-4839-bf46-ecd8b1f2130d: request_fee_refund pending_approval → respuesta sensitive_action
INFO agent.application.chat_service: trayectoria a73ccf5c-80f6-4839-bf46-ecd8b1f2130d: decisión del asesor → request_fee_refund rejected

Error de negocio 
INFO agent.application.chat_service: trayectoria 18add1a9-74be-447e-bb97-2ace4f7107d6: get_charged_fees error → respuesta data_query

Input inválido
INFO agent.application.chat_service: trayectoria 18add1a9-74be-447e-bb97-2ace4f7107d6: sin tools → respuesta data_query

### ¿Algo se ejecutó sin que lo aprobaras?

No, en la trayectoria se ve que el flujo fue respetado

### Conclusión

Con la configuración correcta de control humano, se puede tener flujos manejados por IA que realicen operaciones monetarias o sensibles, que terminen con aprobación humana. Se puede tener controles de idempotencia y manejo de errores para evitar duplicados o que no se sepa el estado de la operación.
