# Resultados de pruebas

## Mediciones

| Mensaje | Intención | latency_ms | prompt_tokens | completion_tokens |
|---|---|---:|---:|---:|
| Hola, me llamo Julio | greeting | 5123 | 382 | 198 |
| ¿Cuánto cobran por retirar en un cajero de otro banco? | product_question | 7376 | 389 | 427 |
| Quiero ver las comisiones que me cobraron este mes | data_query | 23318 | 500 | 763 |
| Quiero que me devuelvan una comisión cobrada dos veces | sensitive_action | 38458 | 628 | 776 |
| ¿A cuánto está el dólar hoy? | out_of_scope | 4490 | 763 | 332 |

