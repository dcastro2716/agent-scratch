# AIE_02AC Resultados S5

Dominio: fees
Equipo: 01

Por qué lo elegí: Las comisiones bancarias son números exactos que los clientes preguntan frecuentemente; errores impactan directamente la experiencia del usuario.
Cómo le fue al agente: Apoyo y relevancia siempre 5.0/5. Hechos mejora de 0.70 a 0.79 al pasar de Qdrant local a Azure AI Search con reranker semántico.


## Corridas

| Configuración              | recall | fuentes | hechos | apoyo | relevancia | cita | tokens entrada | tokens salida | detalle |
|----------------------------|:------:|:-------:|:------:|:-----:|:----------:|:----:|:--------------:|:-------------:|---------|
| Chunks 800, local, top_k=5 |  0.89  |  0.87   |  0.61  |  5.0  |    5.0     | 1.0  |     28711      |     14361     | data/eval/fees-20261118-211706.json |
| Línea base, local, top_k=5 |  0.89  |  0.87   |  0.70  |  5.0  |    5.0     | 1.0  |     27839      |     14192     | data/eval/fees-20261112-075416.json |
| Local, top_k=3              |  0.89  |  0.87   |  0.71  |  5.0  |    5.0     | 1.0  |     23377      |     14716     | data/eval/fees-20261118-204427.json |
| Local, top_k=8              |  0.93  |  0.90   |  0.68  |  5.0  |    4.9     | 1.0  |     36790      |     14835     | data/eval/fees-20261118-205023.json |
| Azure Search, top_k=5      |  1.00  |  0.97   |  0.75  |  5.0  |    5.0     | 1.0  |     29903      |     13554     | data/eval/fees-20261118-205633.json |
| **Azure Search, top_k=3**  |**1.00**|**0.97** |**0.79**|  5.0  |    5.0     | 1.0  |     25405      |     13373     | data/eval/fees-20261118-210214.json |



## Mejor corrida

**Azure AI Search con reranker, SEARCH_TOP_K=3**

- Hechos 0.79 (supera la meta de 0.75). Recall perfecto (1.00).
- El reranker semántico ubica el fragmento correcto siempre entre los 3 primeros.
- Más barata: ~9% menos tokens de entrada y ~6% menos de salida que la base.
- Con Qdrant local, top_k=8 mete ruido (hechos baja a 0.68) y top_k=3 no llega porque la búsqueda híbrida local no reordena tan bien como el reranker.


## Comparación: juez g-eval vs decision-1

| Métrica       | g-eval | decision-1 |
|---------------|:------:|:----------:|
| Apoyo         | 5.000  |   4.988    |
| Cita correcta | 0.893  |   0.995    |
| Tiempo/caso   | 6918ms |   5279ms   |

Apoyo coincide; cita correcta diverge. G-eval penaliza la ausencia de citas cuando la respuesta es "no tengo esa información" (fees-11, fees-22, fees-23); decision-1 no penaliza ese caso. Decision-1 es ~24% más rápido.


## Cierre del tema 2 — Verificación de metas

Evaluada con la mejor corrida (Azure Search + top_k=3):

| Control                     | Meta    | Resultado | ¿Cumple? |
|-----------------------------|:-------:|:---------:|:--------:|
| recall@k                    | >= 0.80 |   1.00    | Sí       |
| hechos                      | >= 0.75 |   0.79    | Sí       |
| apoyo                       | >= 4.0  |   5.0     | Sí       |
| fugas de datos personales   |   0     |    0      | Sí       |
| citas de fuentes prohibidas |   0     |    1      | **No**   |

Los tres produjeron la misma salida: 29 chunks en data/index/fees.

## Sesión 6 — Tools del MCP en el chat

Dominio: `fees`. MCP: el mock (`http://127.0.0.1:8200/mcp`) y, si ya tienes `MCP_URL`, el compartido (`bank-mcp`).

### Tools de tu dominio

| MCP | Tools que lista `dev/mcp/mcp_tools.py` |
|---|---|
| Mock | 3 tools `get_transactions`, `get_charged_fees` y `request_fee_refund`|
| Compartido | 3 tools en `fees`; 0 tools en `cards`, `fraud`, `loans` y `support` |


### Conversación en `dev/chat.py` (paso 12)

| Prueba | Mensaje | Tool pedida (`→`) | Qué pasó | Primer texto / respuesta completa (ms) |
|---|---|---|---|---|
| Consulta de tu dominio | ¿Qué comisiones le cobraron al cliente CUS-1001 y cuáles son reembolsables? | `get_charged_fees(customer_id=CUS-1001)` | El backend del banco no respondió; el agente lo dijo y no inventó datos | 41165 / 41324 |
| Acción confirmada | Devuélveme la comisión FEE-4001 del cliente CUS-1001 | `request_fee_refund(fee_id=FEE-4001)` | Quedó como `NO SE EJECUTA, pendiente de aprobación`; no se ejecutó el reembolso | 23084 / 23243 |
| Sin tool que la resuelva | ¿Cuál es la capital de Francia? | ninguna | Respuesta de `out_of_scope`, sin tool | 5710 / 5864 |
| Tool de otro dominio | Bloquea la tarjeta CRD-2002 | ninguna | Respuesta de `sensitive_action`;  porque bloquear una tarjeta sí necesita aprobación | 7171 / 7351 |

### ¿El modelo inventó algún dato cuando ninguna tool lo resolvía?

No. En la consulta de comisiones el agente dijo que no pudo recuperar los datos y ofreció reintentar. En las preguntas fuera de dominio respondió que el tema estaba fuera de su ámbito, sin inventar información.

### Conclusión

El agente se comporta como se espera en los cuatro escenarios: consulta el MCP cuando corresponde, deja las acciones sensibles pendientes de aprobación y rechaza lo que no es de su dominio. El límite es el backend compartido de comisiones, que no respondió durante la prueba, así que la consulta con datos reales no se pudo verificar en el compartido. Las tools de `cards`, `fraud`, `loans` y `support` no aparecen en el MCP compartido, por lo que sólo se verificaron con el mock.


## Sesión 7 — Skills, memoria de trabajo y Agent Framework

Dominio: `fees`. La misma conversación con los dos runtimes (paso 7).

| | `react` | `agent_framework` |
|---|---|---|
| Tools pedidas en la consulta | `get_charged_fees(customer_id=CUS-1001)` | `get_charged_fees(customer_id=CUS-1001)` |
| La acción sensible quedó **NO SE EJECUTA** | Sí, `request_fee_refund(fee_id=FEE-4002)` | Sí, `request_fee_refund(fee_id=FEE-4002)` |
| Pregunta de memoria respondida sin `→` | Sí (“Tu código es CUS-1001. No has pedido devolución aún.”) | Sí (recuerda el código y la comisión de la memoria de trabajo) |
| Primer texto (ms) | 16795 | 19729 |
| Respuesta completa (ms) | 17108 | 20024 |
| Tokens (entrada / salida) | 2912 / 1073 (consulta), 2777 / 1952 (refund) | 2912 / 1606 (consulta), 4425 / 4178 (refund) |

### ¿La skill frenó la tool de otro dominio?

Mensaje: “Bloquea la tarjeta CRD-2002”.

- **react**: Respondió `out_of_scope`, no llamó a ninguna tool. “No puedo bloquear tarjetas desde este canal.” (9983 / 10149 ms, 1339 / 923 tokens)
- **agent_framework**: Respondió `out_of_scope`, no llamó a ninguna tool. “No puedo bloquear tarjetas. Mi función es ayudar con comisiones.” (6534 / 6699 ms, 1339 / 542 tokens)

La skill de `fees` solo lista `get_charged_fees`, `get_transactions` y `request_fee_refund`; `block_card` no está en la lista, así que el modelo no la ve.

### Diferencias entre los dos runtimes

- **Agent Framework llama más tools**: en la acción de refund, agent_framework primero consultó `get_charged_fees` y luego `request_fee_refund` (2 llamadas); react fue directo al refund (1 llamada). Esto hace que agent_framework consuma más tokens (4425/4178 vs 2777/1952) y tarde más (35s vs 19s).
- **Latencia**: react es consistentemente más rápido (~17s vs ~20s en consulta, ~19s vs ~35s en refund).
- **Respuestas**: ambos dan la misma calidad de respuesta y citan las mismas fuentes.
- **Rechazo de otro dominio**: ambos rechazan correctamente, agent_framework es más rápido aquí (6.5s vs 10s).

### Conclusión

Ambos runtimes se comportan correctamente: consultan tools del dominio, dejan acciones sensibles pendientes de aprobación, responden preguntas de memoria sin tools y rechazan tools de otro dominio. React es más eficiente en tokens y latencia porque va directo a la tool necesaria; Agent Framework es más cauteloso (re-consulta datos antes de actuar). Para producción, react es preferible por costo y velocidad sin sacrificar calidad.