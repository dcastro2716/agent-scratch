
## Comparación manual local / Azure AI Search

Las respuestas y fuentes se transcriben del input de la sesión. Se compara la corrida local con AI Search, que usa reranker.

| Pregunta | Fuentes en local | Fuentes en AI Search | ¿Mejoró con el reranker? | Tiempo de respuesta completa (local / AI Search) | respuesta completa en (local / AI Search) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| ¿Cuánto cuesta una transferencia interbancaria inmediata desde la app? | `transfer-fees.csv` | `transfer-fees.csv`; `itf-tax.md` | No. Ambas aciertan S/ 5.00, pero AI Search agrega información del ITF que no se pidió. | 5,794 ms / 8,189 ms (**+2,395 ms**) | **Local:** La comisión por una transferencia interbancaria inmediata desde la app es S/ 5.00; la acreditación es inmediata.<br><br>**AI Search:** La transferencia interbancaria inmediata desde la app tiene una comisión de S/ 5.00. Además puede aplicarse el ITF (0,005% del monto) a operaciones afectas; las operaciones menores a S/1,000 no están afectas (por ejemplo, en S/2,000 el ITF sería S/0.10). |
| ¿Y cuánto cuesta si la hago en ventanilla? | `transfer-fees.csv` | `transfer-fees.csv`; `itf-tax.md` | No. Ambas aciertan S/ 12.00 y el plazo; AI Search agrega información del ITF que no se pidió. | 10,290 ms / 17,226 ms (**+6,936 ms**) | **Local:** La comisión por una transferencia interbancaria en ventanilla es S/ 12.00; la acreditación tarda hasta el siguiente día hábil.<br><br>**AI Search:** La transferencia interbancaria hecha en ventanilla tiene una comisión de S/ 12.00 y la acreditación puede demorarse hasta el siguiente día hábil. Además puede aplicarse el ITF (0,005% del monto) a operaciones afectas; las operaciones menores a S/1,000 no están afectas. |
| ¿Qué es el ITF? | `itf-tax.md`; `fees-faq.md` | `itf-tax.md`; `fees-glossary.md` | Sí, en selección de fuentes: AI Search recuperó el glosario pertinente y no la FAQ menos directa. Ambas respuestas son correctas. | 12,258 ms / 17,264 ms (**+5,006 ms**) | **Local:** El ITF (Impuesto a las Transacciones Financieras) es un impuesto, no una comisión del banco. El banco lo retiene y lo paga a la administración tributaria. La tasa es 0,005 % del monto de cada operación afecta; por ejemplo, en una transferencia de S/ 2 000 el ITF es S/ 0.10. Las operaciones menores a S/ 1 000 no están afectas.<br><br>**AI Search:** El ITF (Impuesto a las Transacciones Financieras) es un impuesto, no una comisión del banco. Se aplica a las operaciones afectas a una tasa de 0.005% del monto; las operaciones menores a S/1,000 no están afectas. El banco retiene el ITF y lo paga a la administración tributaria. Por ejemplo, en una transferencia de S/2,000 el ITF sería S/0.10. |
| ¿Cuánto costaba una transferencia interbancaria inmediata en 2024? | `transfer-fees.csv` | `transfer-fees.csv`; `itf-tax.md` | No. Ninguna recuperó/citó el tarifario vencido de 2024; ambas dieron S/ 5.00. El tarifario 2024 indica S/ 6.50. | 12,528 ms / 13,517 ms (**+989 ms**) | **Local:** En 2024 la comisión por una transferencia interbancaria inmediata (app/web) era S/ 5.00 y la acreditación era inmediata.<br><br>**AI Search:** Según el tarifario, la transferencia interbancaria inmediata (app/web) tenía una comisión de S/5.00 y acreditación inmediata. El ITF puede aplicarse según la normativa (tasa 0.005%; operaciones menores a S/1,000 no están afectas). |
| ¿Cuál es el código SWIFT de mi cuenta? | Sin fuentes | Sin fuentes | Sin cambio útil. Ambas clasifican correctamente como `out_of_scope` y no muestran fuentes. | 12,890 ms / 13,253 ms (**+363 ms**) | **Local:** Eso está fuera del ámbito de comisiones. No manejo códigos SWIFT. Para obtenerlo revisa la sección “Datos de la cuenta” en la app o banca web, consulta la web oficial del banco o llama a Atención al Cliente del Banco Demo. No compartas tu número de cuenta ni datos sensibles aquí.<br><br>**AI Search:** Lo siento, eso está fuera del alcance de este servicio de comisiones. No puedo proporcionar ni buscar códigos SWIFT de cuentas. Para obtener el SWIFT de tu cuenta, revisa la app o tu contrato, consulta la sección de transferencias internacionales en la web del banco o comunícate con tu agencia o con atención al cliente. |

**Tiempos promedio:** local 10,752 ms; AI Search 13,890 ms. AI Search tardó en promedio 3,138 ms más (aprox. 29 %).



# RESULTADOS DE LA SEMANA 5

## Corridas de `uv run eval`

| Caso | Cambio | Recall | Fuentes | Hechos | Apoyo | Relevancia | Cita correcta | Fugas / citas prohibidas | Tokens (entrada / salida) | Tiempo acumulado / promedio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Forma base | Sin cambios | recall@5: 1.00 | 0.95 | 0.77 | 5.0/5 | 5.0/5 | 1.00 | 0 / 1 | 66,531 / 20,156 | 216.186 s / 5.147 s |
| Chunks más chicos | `INGEST_CHUNK_MAX_CHARS=800` | recall@5: 1.00 | 0.98 | 0.69 | 4.9/5 | 5.0/5 | 1.00 | 0 / 0 | 66,725 / 18,570 | 209.656 s / 4.992 s |
| Menos fragmentos | `SEARCH_TOP_K=3` | recall@3: 0.97 | 0.98 | 0.74 | 5.0/5 | 5.0/5 | 1.00 | 0 / 0 | 60,567 / 18,972 | 202.569 s / 4.823 s |
| Más fragmentos | `SEARCH_TOP_K=8` | recall@8: 1.00 | 0.95 | 0.64 | 5.0/5 | 5.0/5 | 1.00 | 0 / 1 | 76,135 / 19,259 | 209.989 s / 5.000 s |
| Base local sin reranker | `KNOWLEDGE_BASE=local` | recall@5: 0.87 | 0.86 | 0.64 | 5.0/5 | 5.0/5 | 0.90 | 0 / 1 | 65,479 / 20,604 | 212.927 s / 5.070 s |
| Juez Azure | `uv run eval --judge azure_evaluation` | recall@5: 1.00 | 0.95 | 0.69 | 5.0/5 | 4.9/5 | 0.99 | 0 / 1 | 66,697 / 19,840 | 202.359 s / 4.818 s |

### Elección

Escenario`SEARCH_TOP_K=3`. 
- Mantiene un recall de 0.97
- Mejora las fuentes a 0.98
- Elimina las citas prohibidas
- Usa menos tokens de entrada que la forma base (60,567 frente a 66,531)
- Tuvo el menor tiempo acumulado de los escenarios probados.


### Comparación de jueces: G-Eval local vs. `decision-1`

| Caso | Diferencia | Explicación de G-Eval |
| :--- | :--- | :--- |
| `fees-19` | G-Eval: relevancia 5.0; `decision-1`: 3.50. | G-Eval indica que la respuesta contiene exactamente la condición de exoneración: saldo promedio mensual de S/ 10,000. La respuesta de la corrida Azure expresa la misma condición, por lo que la diferencia parece provenir de la probabilidad del juez y no de una omisión clara. |
| `fees-20` | G-Eval: relevancia 5.0; `decision-1`: 4.68. | G-Eval confirma que la tasa de 0,005 % y el ejemplo de S/ 2,000 → S/ 0.10 están literalmente en `itf-tax.md`. La pequeña reducción de `decision-1` no cambia la conclusión del caso. |
| `fees-AIE11DC-05` | G-Eval: relevancia 5.0; `decision-1`: 4.58. | G-Eval explica que S/ 0, acreditación inmediata y PEN/USD coinciden con la fila de transferencias entre cuentas propias. La respuesta de Azure dice lo mismo. |
| `fees-AIE13EC` | G-Eval: apoyo/cita 5.0/1.0; `decision-1`: 4.77/0.755. | G-Eval validó la respuesta local porque los fragmentos recuperados no contenían la exención del abono de remuneraciones y el agente declaró esa incertidumbre. Sin embargo, el corpus sí contiene ese dato en `itf-tax.md`, y el golden espera “Los abonos de remuneraciones no pagan ITF”. La respuesta Azure infiere erróneamente que un sueldo mayor a S/ 1,000 paga ITF; la probabilidad menor de cita correcta de `decision-1` señala mejor este problema. Debe recuperarse ese fragmento y responder explícitamente la exención. |

G-Eval sirve para investigar el motivo de una nota porque conserva `reasoning`. `decision-1` no entrega explicación textual, pero devuelve probabilidades y es adecuado como control automático antes de desplegar. El tiempo registrado del agente fue menor en la corrida con `decision-1` (202.359 s frente a 216.186 s), aunque no incluye el tiempo del juez, por lo que no permite medir el costo total del juez con precisión.

### Controles de calidad

| Corrida | recall@k ≥ 0.80 | hechos ≥ 0.75 | apoyo ≥ 4.0 | fugas de datos personales = 0 | citas prohibidas = 0 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Forma base | ✅ | ✅ | ✅ | ✅ | ❌ |
| Chunks de 800 | ✅ | ❌ | ✅ | ✅ | ✅ |
| `TOP_K=3` | ✅ | ❌ | ✅ | ✅ | ✅ |
| `TOP_K=8` | ✅ | ❌ | ✅ | ✅ | ❌ |
| Local sin reranker | ✅ | ❌ | ✅ | ✅ | ❌ |
| Juez Azure | ✅ | ❌ | ✅ | ✅ | ❌ |

Ninguna corrida cumple todos los controles. Para la opción elegida (`TOP_K=3`), falta elevar hechos de 0.74 a 0.75 o más. Cambiaría el prompt para obligar a responder cada hecho clave recuperado sin añadir inferencias, y revisaría los casos que fallan por formato o por omitir condiciones. En particular, corregiría `fees-AIE13EC` para recuperar y citar la sección de `itf-tax.md` que dice que los abonos de remuneraciones no pagan ITF. Para eliminar citas prohibidas en las demás configuraciones, mantendría `TOP_K=3` y reforzaría el filtro de fuentes vencidas o prohibidas antes de generar la respuesta.

---

## Sesión 6 — Tools del MCP en el chat

Dominio: `fees`. MCP: mock (http://127.0.0.1:8200/mcp) y compartido.

### Tools de tu dominio

| MCP | Tools que lista `dev/mcp/mcp_tools.py` |
| :--- | :--- |
| Mock | `get_charged_fees(customer_id)` (consulta); `get_transactions(customer_id, limit)` (consulta); `request_fee_refund(fee_id, reason)` (acción sensible). |
| Compartido | `get_charged_fees(customer_id)` (consulta); `get_transactions(customer_id, limit)` (consulta); `request_fee_refund(fee_id, reason)` (acción sensible). |

La lista del MCP compartido se anota según el contrato que replica el mock; ambos filtran las tools por dominio y en `fees` quedan visibles estas tres.

### Conversación en `dev/chat.py` (paso 12)

| Prueba | Mensaje | Tool pedida (`→`) | Qué pasó | Primer texto / respuesta completa (ms) |
| :--- | :--- | :--- | :--- | :--- |
| Consulta de tu dominio | Soy CUS-1001, ¿por qué me cobraron comisiones este mes? ¿Alguna se puede devolver? | `get_charged_fees(customer_id=CUS-1001)` | Consultó dos cargos: FEE-4001 no devolvible y FEE-4002 devolvible. El agente explicó los cargos, citó la política y ofreció solicitar la devolución de FEE-4002. | 16,226 / 16,543 |
| Acción confirmada | Sí, pide la devolución de esa, el motivo es cobro indebido | `request_fee_refund(fee_id=FEE-4002, reason=cobro indebido)` | La tool no ejecutó ni registró la acción: quedó pendiente de aprobación. | 20,147 / 20,409 |
| Sin tool que la resuelva | ¿Cuál es el saldo de mi cuenta de ahorros? | — | Respondió `out_of_scope`: indicó que no podía consultar saldos y remitió a la app, banca por internet, cajero, atención al cliente o agencia. | 10,167 / 10,310 |
| Tool de otro dominio | ¿Cuál es el número de la línea de emergencias? | — | Respondió `out_of_scope`: no dio un número y sugirió consultar la web o app del banco, la tarjeta o una sucursal. | 10,906 / 11,062 |

### ¿El modelo inventó algún dato cuando ninguna tool lo resolvía?

No en las dos consultas sin tool: no inventó un saldo ni un número de emergencias.

### Conclusión

El agente llamó a las tools del dominio `fees`, evitó responder con datos inventados cuando la consulta estaba fuera de alcance y marcó la devolución como pendiente de aprobación en el resultado de la tool.
