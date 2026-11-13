## Línea base (S5)

Dominio `fees`, equipo 01. Búsqueda en Qdrant local y juez G-Eval:

    Resumen de 30 casos (juez local):
      recall@5: 0.89   intención: 1.00   fuentes: 0.90   hechos: 0.41
      apoyo: 4.9/5   relevancia: 4.9/5   cita correcta: 1.0
      fugas de datos personales: 0   citas de fuentes prohibidas: 0
      tokens: 27771 de entrada, 48132 de salida

Detalle por caso: `data/eval/fees-20261110-215125.json`

### Mi caso del golden set - Preguntas:

- **Pregunta (`fees-AIE37JG`).** ¿Cuánto cuesta pedir una copia del voucher de una operación?
- **Por qué lo elegí.** Los 30 casos base no cubren este servicio. La pregunta comprueba si el agente encuentra y cita la tarifa exacta de la tabla de servicios adicionales.
- **Cómo le fue al agente.** Recuperó `additional-services-fees.docx`. Respondió «cinco soles por voucher». El importe coincide con el tarifario.

### Resultado de mis cinco casos - Juez Local:

    Resumen de 5 casos (juez local):
      recall@5: 0.80   intención: 1.00   fuentes: 0.80   hechos: 0.20
      apoyo: 4.6/5   relevancia: 5.0/5   cita correcta: 0.8
      fugas de datos personales: 0   citas de fuentes prohibidas: 0
      tokens: 5081 de entrada, 4625 de salida

Reporte de la corrida previa a la asignación de IDs únicos: `data/eval/fees-20261110-233230.json`.

### Resultado de juez azure_evaluation:

Resumen de 35 casos (juez azure_evaluation):
  recall@8: 1.00   intención: 0.97   fuentes: 0.97   hechos: 0.56
  apoyo: 5.0/5   relevancia: 4.8/5   cita correcta: 1.0
  fugas de datos personales: 0   citas de fuentes prohibidas: 0
  tokens: 41759 de entrada, 43381 de salida

Reporte de la corrida previa a la asignación de IDs únicos: `data/eval/fees-20261112-092615.json`.

## Antes y después (S5)

Las corridas usan los mismos 30 casos base de `fees`, Qdrant local, el chat `gpt-5-nano` y el juez G-Eval con `gpt-5-mini`. Cada prueba cambia una variable respecto de la línea base.

| Prueba | Recall | Hechos | Apoyo | Tokens de entrada | Citas prohibidas |
|---|---:|---:|---:|---:|---:|
| Línea base, top-k 5 y fragmentos de hasta 1500 caracteres | 0.89 | 0.41 | 4.9/5 | 27 771 | 0 |
| Top-k 8 | 0.93 | 0.52 | 4.9/5 | 35 670 | 0 |
| Top-k 3 | 0.89 | 0.52 | 5.0/5 | 22 668 | 1 |
| Fragmentos de hasta 800 caracteres, top-k 5 | 0.89 | 0.48 | 5.0/5 | 27 955 | 0 |

- **Top-k 8.** Recuperó el tarifario esperado en `fees-22`. `fees-11` y `fees-23` siguieron sin recuperarlo. El consumo subió en 7 899 tokens de entrada (+28.4 %). Reporte `data/eval/fees-20261111-001305.json`.
- **Top-k 3.** Conservó el recall de la línea base y consumió 5 103 tokens de entrada menos (−18.4 %). Registró una cita prohibida en `fees-25`. Reporte `data/eval/fees-20261111-001954.json`.
- **Límite de 800 caracteres.** Generó los mismos 29 fragmentos en texto y metadatos que el límite de 1500. El más largo mide 677 caracteres. Se regeneraron los embeddings, así que la diferencia de puntuación entre corridas no demuestra un efecto del tamaño de los fragmentos. Reporte `data/paso10-chunks-800/eval/fees-20261111-003053.json`.

**Configuración elegida.** Se guardó `SEARCH_TOP_K=8` en `.env` y se mantuvo `INGEST_CHUNK_MAX_CHARS=1500`. En Qdrant, top-k 8 dio el mayor recall (0.93), llegó a 0.52 en hechos y registró 0 citas prohibidas y 0 fugas. El control de hechos sigue por debajo de la meta de 0.75.

```zsh
KNOWLEDGE_BASE=local uv run eval --limit 30
```

La comparación con el reranker de Azure AI Search queda pendiente por el error HTTP 402 de cuota semántica observado en el paso 9 y 12.
