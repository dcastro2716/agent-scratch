# Resultados de pruebas

## Mediciones mini

| Mensaje | Intención | latency_ms | prompt_tokens | completion_tokens |
|---|---|---:|---:|---:|
| Hola, me llamo Julio | greeting | 6587 | 382 | 196 |
| ¿Cuánto cobran por retirar en un cajero de otro banco? | product_question | 7253 | 455 | 515 |
| Quiero ver las comisiones que me cobraron este mes | data_query | 8766 | 590 | 826 |
| Quiero que me devuelvan una comisión cobrada dos veces | sensitive_action | 5744 | 717 | 459 |
| ¿A cuánto está el dólar hoy? | out_of_scope | 4906 | 855 | 329 |

## Mediciones nano

| Mensaje | Intención | latency_ms | prompt_tokens | completion_tokens |
|---|---|---:|---:|---:|
| Hola, me llamo Julio | greeting | 5205 | 382 | 372 |
| ¿Cuánto cobran por retirar en un cajero de otro banco? | product_question | 6451 | 439 | 1043 |
| Quiero ver las comisiones que me cobraron este mes | data_query | 6086 | 521 | 944 |
| Quiero que me devuelvan una comisión cobrada dos veces | sensitive_action | 10432 | 637 | 1278 |
| ¿A cuánto está el dólar hoy? | out_of_scope | 5719 | 762 | 924 |
