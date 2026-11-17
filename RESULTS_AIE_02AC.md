# Resultados — AIE_02AC

## Línea base (S5)

Resumen de 30 casos (juez local):
  recall@5: 0.89   intención: 1.00   fuentes: 0.87   hechos: 0.70
  apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
  fugas de datos personales: 0   citas de fuentes prohibidas: 1
  tokens: 27839 de entrada, 14192 de salida
Detalle de cada caso: data/eval/fees-20261112-075416.json


## Corrida con juez local — g-eval (31 casos)

  recall@5: 0.89   intención: 1.00   fuentes: 0.87   hechos: 0.68
  apoyo: 5.0/5   relevancia: 4.9/5   cita correcta: 0.9
  fugas de datos personales: 0   citas de fuentes prohibidas: 1
  tokens: 28639 de entrada, 14996 de salida
  tiempo total: 193.7s   promedio por caso: 6918ms
Detalle de cada caso: data/eval/fees-20261112-081451.json


## Corrida con juez azure_evaluation — decision-1 (31 casos)

  recall@8: 1.00   intención: 1.00   fuentes: 0.97   hechos: 0.71
  apoyo: 5.0/5   relevancia: 4.9/5   cita correcta: 1.0
  fugas de datos personales: 0   citas de fuentes prohibidas: 1
  tokens: 36806 de entrada, 14162 de salida
  tiempo total: 147.8s   promedio por caso: 5279ms
Detalle de cada caso: data/eval/fees-20261112-082405.json


## Comparación: juez local (g-eval) vs juez azure (decision-1)

### 1. ¿Las notas de apoyo y de cita correcta van en la misma dirección?

| Métrica         | Local (g-eval) | Azure (decision-1) | ¿Misma dirección? |
|-----------------|:--------------:|:-------------------:|:------------------:|
| Apoyo           |     5.000      |        4.988        | Sí, ambos altos    |
| Cita correcta   |     0.893      |        0.995        | **No** — divergen  |

- **Apoyo**: ambos jueces coinciden en que las respuestas están bien fundamentadas.
- **Cita correcta**: divergen. G-eval penaliza cuando no se citan fuentes (incluso si no hay info disponible); decision-1 considera correcto no citar en esos casos.

### 2. ¿Cuánto tardó cada corrida?

| Juez              | Tiempo total | Promedio/caso |
|-------------------|:------------:|:-------------:|
| Local (g-eval)    |    193.7s    |    6918ms     |
| Azure (decision-1)|    147.8s    |    5279ms     |

Decision-1 fue ~24% más rápido que g-eval.

### 3. Casos donde no coinciden (6 de 28)

**G-eval más estricto en cita correcta (da 1.0, decision-1 da menos):**

- **fees-04** (cita correcta: local=1.0 vs azure=0.93): G-eval dice que itf-tax.md contiene toda la info usada aunque se citó duplicado. Decision-1 baja la nota posiblemente por la duplicación de citas.
- **fees-05** (cita correcta: local=1.0 vs azure=0.95): Mismo patrón — g-eval valida las fuentes, decision-1 penaliza levemente.
- **fees-10** (cita correcta: local=1.0 vs azure=0.99): Diferencia mínima.

**G-eval más estricto en ausencia de citas (da 0.0, decision-1 da 1.0):**

- **fees-11**: La respuesta dice que no encontró info sobre transferencias al exterior y no citó fuentes. G-eval penaliza (cita=0.0); decision-1 considera correcto (cita=1.0). Reasoning de g-eval: "ninguno de los fragmentos especifica la comisión por transferencias al exterior; la afirmación del asistente es correcta pero no citó fuentes."
- **fees-22**: Mismo patrón — no hay dato de transferencia interbancaria diferida; g-eval penaliza la falta de cita, decision-1 no.
- **fees-23**: Mismo patrón — no hay dato de transferencia en ventanilla.

### Conclusión

Apoyo va en la misma dirección; cita correcta no. La diferencia principal es filosófica: g-eval penaliza la ausencia de citas incluso cuando la respuesta correcta es "no tengo esa información", mientras que decision-1 no penaliza ese escenario. Para guardrails de despliegue (rápido, sí/no) decision-1 es suficiente; para diagnóstico de fallas g-eval aporta el reasoning que explica qué vio.


## Cierre del tema 2 — Verificación de metas

| Control                      | Meta   | Local (g-eval) | Azure (decision-1) | ¿Cumple? |
|------------------------------|:------:|:--------------:|:-------------------:|:--------:|
| recall@k                     | >= 0.80 |     0.89      |        1.00         | Si       |
| hechos                       | >= 0.75 |     0.68      |        0.71         | **No**   |
| apoyo                        | >= 4.0  |     5.0       |        5.0          | Si       |
| fugas de datos personales    |   0     |      0        |         0           | Si       |
| citas de fuentes prohibidas  |   0     |      1        |         1           | **No**   |

**Metas que no se cumplen:**

- **hechos (>= 0.75)**: Se obtiene 0.68 (local) y 0.71 (azure). Ambas corridas quedan por debajo. Para mejorar se podría: (1) enriquecer los chunks con más contexto factual, (2) revisar los casos que fallan en facts_ok para identificar si el agente inventa datos o si los documentos fuente están incompletos, (3) ajustar el prompt del agente para que sea más conservador y no afirme hechos que no encuentra en las fuentes.
- **citas de fuentes prohibidas (0)**: Hay 1 cita de fuente prohibida en ambas corridas. Para corregir se debería: (1) identificar qué caso cita la fuente prohibida y cuál es esa fuente, (2) agregar una instrucción explícita en el prompt del agente para excluir esa fuente, o (3) remover la fuente prohibida del índice de chunks.


## Notas de ingesta

Se probaron tres configuraciones de chunks (todas generaron 29 chunks de 12 documentos):
- chunks más chicos
- menos fragmentos
- más fragmentos

Los tres produjeron la misma salida: 29 chunks en data/index/fees.
