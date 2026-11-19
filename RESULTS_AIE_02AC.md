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

Nota: chunks 800 produce los mismos 29 chunks que chunks 1500 (todos los documentos son < 677 chars). La variación en hechos es no-determinismo del modelo.
Todas las corridas: intención=1.00, fugas de datos personales=0, citas de fuentes prohibidas=1.


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

