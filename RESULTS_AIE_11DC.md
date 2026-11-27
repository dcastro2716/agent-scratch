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

## Sesión 9 — Despliegue en Azure

Equipo: `team-01`. Dominio: `fees`.

| Comprobación | Resultado |
|---|---|
| Tests en el contenedor (paso 3) | <pre><code>docker build -f devops/Dockerfile --target test -t agent:test . <br>[+] Building 25.8s (19/19) FINISHED                                                                                                                                                    docker:desktop-linux<br>=> [internal] load build definition from Dockerfile                                                                                                                                                   0.0s<br>=> => transferring dockerfile: 2.93kB                                                                                                                                                                 0.0s<br>=> resolve image config for docker-image://docker.io/docker/dockerfile:1                                                                                                                              2.3s<br>=> [auth] docker/dockerfile:pull token for registry-1.docker.io                                                                                                                                       0.0s<br>=> docker-image://docker.io/docker/dockerfile:1@sha256:572cebbc2b15e6f84c077742952674889cb63cd5e9b80abdffcbe587b6f19183                                                                               1.3s<br>=> => resolve docker.io/docker/dockerfile:1@sha256:572cebbc2b15e6f84c077742952674889cb63cd5e9b80abdffcbe587b6f19183                                                                                   0.0s<br>=> => sha256:d767384bcc0f67e87fc678874f8ec62ddb408aeeb26def25b05e6be08c790ed7 13.93MB / 13.93MB                                                                                                       1.2s<br>=> => extracting sha256:d767384bcc0f67e87fc678874f8ec62ddb408aeeb26def25b05e6be08c790ed7                                                                                                              0.1s<br>=> [internal] load metadata for docker.io/library/python:3.12-alpine                                                                                                                                  1.6s<br>=> [auth] library/python:pull token for registry-1.docker.io                                                                                                                                          0.0s<br>=> [base 1/3] FROM docker.io/library/python:3.12-alpine@sha256:c5ba3deef00c7758561a0f03c26f44f10589263d40e732b8748e0d1f38f6dd89                                                                       1.7s<br>=> => resolve docker.io/library/python:3.12-alpine@sha256:c5ba3deef00c7758561a0f03c26f44f10589263d40e732b8748e0d1f38f6dd89                                                                            0.0s<br>=> => sha256:8ab1992027dfd42035e1028c42f93c50180a2b01b89a2645899d7c9299fcdd5c 251B / 251B                                                                                                             0.2s<br>=> => sha256:9cee687b648e8e2f38b10079e58e752f383ebe19bea21c5a6657a29703a336f8 13.92MB / 13.92MB                                                                                                       1.3s<br>=> => sha256:6d356b48c1c56cccd22e48f043c1e8ac8d79ef86f9e625b548c82014803b7830 415.54kB / 415.54kB                                                                                                     0.8s<br>=> => sha256:b90627b8f4292fd3cb63f0f27f0b11c37f04ba88ef3b78d4948ea0ace18c85e9 4.19MB / 4.19MB                                                                                                         1.3s<br>=> => extracting sha256:b90627b8f4292fd3cb63f0f27f0b11c37f04ba88ef3b78d4948ea0ace18c85e9                                                                                                              0.1s<br>=> => extracting sha256:6d356b48c1c56cccd22e48f043c1e8ac8d79ef86f9e625b548c82014803b7830                                                                                                              0.1s<br>=> => extracting sha256:9cee687b648e8e2f38b10079e58e752f383ebe19bea21c5a6657a29703a336f8                                                                                                              0.2s<br>=> => extracting sha256:8ab1992027dfd42035e1028c42f93c50180a2b01b89a2645899d7c9299fcdd5c                                                                                                              0.0s<br>=> [internal] load build context                                                                                                                                                                      0.0s<br>=> => transferring context: 440.48kB                                                                                                                                                                  0.0s<br>=> [base 2/3] RUN pip install --no-cache-dir --disable-pip-version-check uv==0.11.28                                                                                                                  4.5s<br>=> [base 3/3] WORKDIR /app                                                                                                                                                                            0.0s <br>=> [builder 1/5] COPY pyproject.toml uv.lock ./                                                                                                                                                       0.0s <br>=> [builder 2/5] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-dev --no-install-project                                                                                     6.7s <br>=> [builder 3/5] COPY README.md ./                                                                                                                                                                    0.0s <br>=> [builder 4/5] COPY src ./src                                                                                                                                                                       0.0s <br>=> [builder 5/5] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-dev --no-editable                                                                                            0.3s <br>=> [test 1/3] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --frozen --no-editable                                                                                                        0.6s <br>=> [test 2/3] COPY tests ./tests                                                                                                                                                                      0.0s <br>=> [test 3/3] COPY dev ./dev                                                                                                                                                                          0.0s <br>=> exporting to image                                                                                                                                                                                 6.6s <br>=> => exporting layers                                                                                                                                                                                4.6s <br>=> => exporting manifest sha256:3c4d02fa5e97302b70933d36b826ee63e644230471b70f9f244071edb8ed87ce                                                                                                      0.0s <br>=> => exporting config sha256:01b5c8ef8a5de2bd7b860d31e78e8b17e4ef60287a4419103edd01c5956f567c                                                                                                        0.0s <br>=> => exporting attestation manifest sha256:3580a26d62c3e52dd54ee5682ae43b02646f66dc1bf7c4b275e93b8cd721779c                                                                                          0.0s<br>=> => exporting manifest list sha256:c26a79f28df66cc5372d76bcea95ed870adb98d3d24aa5ffd56f27c1d355865e                                                                                                 0.0s<br>=> => naming to docker.io/library/agent:test                                                                                                                                                          0.0s<br>=> => unpacking to docker.io/library/agent:test                                                                                                                                                       1.9s<br>dcastro@Diegos-MacBook-Air agent-scratch % docker run --rm agent:test<br>........................................................................ [ 50%]<br>............................sssss....................................... [100%]<br>139 passed, 5 skipped in 3.03s<br></code></pre>|
| Acción aprobada después de reiniciar `uvicorn` (paso 2, Cosmos DB) | <pre><code>Tú: Sí, pide la devolución de esa, el motivo es cobro indebido<br>→ request_fee_refund(fee_id=FEE-4002, reason=cobro indebido)<br>NO SE EJECUTA, pendiente de aprobación: {"status": "pendiente_aprobacion", "action_id": "call-3e7264a8", "detail": "Acción sensible: no se ejecutó ni se registró todavía. Dile al cliente que la pedist<br>Agente [sensitive_action]: He registrado la solicitud de devolución de FEE-4002 (Mantenimiento de cuenta) por motivo “cobro indebido”. Quedó pendiente de aprobación por un asesor; la respuesta puede tardar hasta 15 días hábiles y, si procede, el abono se hará en 2 días hábiles. No puedo pedir otra devolución hasta que el asesor decida esta. ¿Desea algo más?<br>Fuentes:<br>[1] fee-refund-policy.docx · Política de devolución de comisiones > Cómo se solicita<br>[2] fee-refund-policy.docx · Política de devolución de comisiones > Plazos<br>[3] fee-refund-policy.docx · Política de devolución de comisiones > Cuándo se devuelve una comisión<br>(primer texto en 16955 ms, respuesta completa en 18207 ms, 5043 tokens de entrada, 1760 de salida)<br>Asesor: ¿apruebas request_fee_refund(fee_id=FEE-4002, reason=cobro indebido)? [s/n]: </code></pre><pre><code>INFO agent.application.chat_service: trayectoria 8714a78a-1d44-4ea1-80b4-a0bc8c3c04d3: request_fee_refund pending_approval → respuesta sensitive_action<br>^CINFO:     Shutting down<br>INFO:     Waiting for application shutdown.<br>INFO:     Application shutdown complete.<br>INFO:     Finished server process [56005]<br>INFO:     Stopping reloader process [56003]<br>dcastro@Diegos-MacBook-Air agent-scratch % uv run uvicorn agent.infrastructure.bootstrap:create_app --factory --reload<br>INFO:     Will watch for changes in these directories: ['/Users/dcastro/Workspaces/nttdata/session2.1/agent-scratch']<br>INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)<br>INFO:     Started reloader process [56406] using WatchFiles<br>INFO agent.infrastructure.bootstrap: Foundry auth provider: entra_id<br>INFO agent.infrastructure.bootstrap: Foundry auth provider: entra_id<br>INFO agent.infrastructure.bootstrap: Knowledge base: azure_search · https://srch-workshop-jsu3.search.windows.net (índice idx-team-01) · 29 chunks<br>INFO agent.infrastructure.bootstrap: Conversation store: Cosmos DB workshop/team-01<br>INFO httpx2: HTTP Request: POST https://ca-mcp-server.icybush-2ea2dfc1.eastus2.azurecontainerapps.io/mcp "HTTP/1.1 200 OK"<br>INFO httpx2: HTTP Request: POST https://ca-mcp-server.icybush-2ea2dfc1.eastus2.azurecontainerapps.io/mcp "HTTP/1.1 200 OK"<br>INFO agent.infrastructure.bootstrap: MCP: https://ca-mcp-server.icybush-2ea2dfc1.eastus2.azurecontainerapps.io/mcp · 3 tools: get_transactions, get_charged_fees, request_fee_refund<br>INFO agent.infrastructure.bootstrap: Agent runtime: agent_framework<br>INFO agent.infrastructure.bootstrap: Foundry auth provider: entra_id<br>INFO:     Started server process [56408]<br>INFO:     Waiting for application startup.<br>INFO:     Application startup complete.<br>INFO httpx2: HTTP Request: POST https://ca-mcp-server.icybush-2ea2dfc1.eastus2.azurecontainerapps.io/mcp "HTTP/1.1 200 OK"<br>INFO httpx2: HTTP Request: POST https://ca-mcp-server.icybush-2ea2dfc1.eastus2.azurecontainerapps.io/mcp "HTTP/1.1 200 OK"<br>INFO httpx2: HTTP Request: POST https://ca-mcp-server.icybush-2ea2dfc1.eastus2.azurecontainerapps.io/mcp "HTTP/1.1 200 OK"<br>INFO agent.application.chat_service: trayectoria 8714a78a-1d44-4ea1-80b4-a0bc8c3c04d3: decisión del asesor → request_fee_refund ok<br></code></pre><pre><code>s<br>resultado: {"id": "RFD-9001", "fee_id": "FEE-4002", "status": "registered", "reason": "cobro indebido"}<br>Agente [sensitive_action]: Su solicitud de devolución de FEE-4002 fue registrada con ID RFD-9001 y motivo “cobro indebido”. La solicitud está registrada para que el banco la procese; no se ha aplicado aún.</code></pre>|
| Imagen desplegada (`team-01/agent:59bd28d590f70ff00eda207410527248b1520aa7`) | <pre><code>Run az extension add --name containerapp --upgrade --only-show-errors<br>az extension add --name containerapp --upgrade --only-show-errors<br>az containerapp update -n "&#36;CONTAINER_APP" -g "&#36;RESOURCE_GROUP" --image "&#36;IMAGE" \<br>--query "properties.latestRevisionName" -o tsv<br>shell: /usr/bin/bash -e {0}<br>env:<br>ACR_LOGIN_SERVER: acrworkshopjsu3.azurecr.io<br>RESOURCE_GROUP: rg-team-01<br>CONTAINER_APP: ca-agent-chat-01<br>DOMAIN: fees<br>IMAGE: acrworkshopjsu3.azurecr.io/team-01/agent:59bd28d590f70ff00eda207410527248b1520aa7<br>WARNING: The behavior of this command has been altered by the following extension: containerapp<br>/ Running ..<br>| Running ..<br>\ Running ..<br>- Running ..<br>/ Running ..<br>| Running ..<br>\ Running ..<br>ca-agent-chat-01--0000002<br></code></pre> |
| Revisión activa y duración del job `deploy` | <pre><code class="language-bash">Run rev=&#36;(az containerapp show -n "&#36;CONTAINER_APP" -g <br>"&#36;RESOURCE_GROUP" --query "properties.latestRevisionName" -o tsv)<br>  rev=&#36;(az containerapp show -n "&#36;CONTAINER_APP" -g "&#36;RESOURCE_GROUP" --query "properties.latestRevisionName" -o tsv)<br>  for i in &#36;(seq 1 18); do<br>    state=&#36;(az containerapp revision show -n "&#36;CONTAINER_APP" -g "&#36;RESOURCE_GROUP" --revision "&#36;rev" \<br>      --query "properties.runningState" -o tsv)<br>    echo "$rev: $state"<br>    case "&#36;state" in<br>      Running&#42;) exit 0 ;;<br>      &#42;Failed&#42;) echo "::error::La revisión no arrancó: revisa los logs de $CONTAINER_APP."; exit 1 ;;<br>    esac<br>    sleep 10<br>  done<br>  echo "::error::La revisión $rev no llegó a Running en 3 minutos (estado: $state)."<br>  exit 1<br>  shell: /usr/bin/bash -e {0}<br>  env:<br>    ACR_LOGIN_SERVER: acrworkshopjsu3.azurecr.io<br>    RESOURCE_GROUP: rg-team-01<br>    CONTAINER_APP: ca-agent-chat-01<br>    DOMAIN: fees<br>    IMAGE: acrworkshopjsu3.azurecr.io/team-01/agent:59bd28d590f70ff00eda207410527248b1520aa7<br>WARNING: The behavior of this command has been altered by the following extension: containerapp<br>ca-agent-chat-01--0000002: Activating<br>ca-agent-chat-01--0000002: Activating<br>ca-agent-chat-01--0000002: Activating<br>ca-agent-chat-01--0000002: Activating<br>ca-agent-chat-01--0000002: Activating<br>ca-agent-chat-01--0000002: RunningAtMaxScale<br></code></pre> deploy: 2m 34s |
| `/health` del agente desplegado | Agente en https://ca-agent-chat-01.icybush-2ea2dfc1.eastus2.azurecontainerapps.io: ok |
| Respuesta con `Fuentes:` contra Azure (y su tiempo en ms) | <pre><code>Fuentes:<br>   [1] fees-faq.md · Preguntas frecuentes sobre comisiones > ¿Cuánto cobran por retirar en un cajero de otro banco?<br>   [2] atm-network.html · Cajeros y red de atención > Cajeros de otros bancos<br>   [3] savings-accounts-fees.html · Tarifario de cuentas de ahorro > Comisiones por cuenta<br>  (primer texto en 7832 ms, respuesta completa en 7969 ms, 1658 tokens de entrada, 686 de salida)<br></code></pre> |
| Acción aprobada contra Azure, con su `resultado:` | <pre><code>Asesor: ¿apruebas request_fee_refund(fee_id=FEE-4002, reason=cobro indebido)? [s/n]: s<br><br>    resultado: {"id": "RFD-9001", "fee_id": "FEE-4002", "status": "registered", "reason": "cobro indebido"}<br>  Agente [sensitive_action]: La solicitud de devolución quedó registrada (ID RFD-9001) para la comisión FEE-4002 por «cobro indebido». La solicitud está registrada para que el banco la procese; no se ha aplicado el reembolso.<br></code></pre> |

### Qué pone Azure y qué pone la imagen

APPLICATIONINSIGHTS_CONNECTION_STRING
AZURE_CLIENT_ID
AZURE_OPENAI_ENDPOINT
COSMOS_CONTAINER
COSMOS_DATABASE
COSMOS_ENDPOINT
FOUNDRY_PROJECT_ENDPOINT
KEY_VAULT_URI
MCP_SCOPE
MCP_URL
SEARCH_ENDPOINT
SEARCH_INDEX
TEAM_ID

### Problemas que encontraste y cómo los resolviste

el client_id que esta en el archivo adjunto del laboratorio tenia un valor incorrecto. Tuve que entrar a entra id y buscar el usuario correcto.
Hubo conflicto en el merge con main por PRs incorrectos, por lo que se tuvo que corregir a mano el código.

### Conclusión

Tiempos de versión local
(primer texto en 26402 ms, respuesta completa en 27526 ms, 4014 tokens de entrada, 2789 de salida)
(primer texto en 16955 ms, respuesta completa en 18207 ms, 5043 tokens de entrada, 1760 de salida)

Tiempos de versión Azure
(primer texto en 21602 ms, respuesta completa en 21737 ms, 4913 tokens de entrada, 2527 de salida)
(primer texto en 16084 ms, respuesta completa en 16292 ms, 5542 tokens de entrada, 1690 de salida)

La versión en Azure es mas rápida en responder que la versión local, incluyen el hecho que la versión de azure está de manera remota. Vemos también que gasta mas token de entrada pero menos de salida, esto puede ser porque al tener memoria persistente tiene mayor historia.

Aparte de eso, el proceso de despliegue es identico al de cualquier otra aplicación, no hay diferencias por ser una aplicación de IA.

## Sesión 10 — Trazas por turno y dashboard

Equipo: `team-01`. App Insights: `appi-team-01`. Los cuatro casos contra el agente desplegado (paso 8).

| Caso | `operation_Id` | Latencia (ms) | Tokens de entrada | Tokens de salida | Tools | Error | Observaciones |
|---|---|---|---|---|---|---|---|
| Saludo | 9b5ee91ca2ef35fdb0733eebf05a7418 | 4840 | 1782 | 121 | ninguna | ninguno | el mensaje de salida consume pocos tokens, posiblemente ya estaba en cache |
| Consulta con retrieval | 94f1ec137e6ec3bf56bed793d7e3041d | 7900 | 1880 | 759 | ninguna | ninguno | se obseerva que detectó el intent como pregunta del dominio |
| Llamada a tool | 4980048a2cc9327e920b12e637bcced5 | 52962 | 3984 | 1798 | get_charged_fees:error | no muestra error incluso cuando el tool dio error | los tokens de respuesta son elevados porque no cachea la respuesta del api. Aparecen multiples registros, debido a cada paso. Se observa que la llamada a la tools se llevó casi todo el tiempo|
| Error controlado | 6d7cb64ee1290acc2f2faeb22c415fcd | 187 | - | - | - | not_found | no hubo consumo de tokens ya que era una operación inválida y el mismo código lo puede reconocer. |

En **Observaciones**, una línea: lo que llamó la atención de la traza (qué se llevó el tiempo, la dependencia que falló, si el
error permite ubicar el turno). En **Tools**, `—` si el turno no llamó ninguna.

### Lo que dice el workbook

| Panel | Lo que viste |
|---|---|
| Latencia p95 por intención | dataquery:52537 product_question:12890 greetings:10831|
| Tokens por turno | get_charged_fees:37911 |
| Dónde se va el tiempo de un turno | MCP: Total 65 p95 26, Foundry Chat total 46 p95 6, otro total 8 p95 1, CosmosDB total 4 p95 0.1, Foundy embeddings total 3 p95 1, AI Search total 1 p95 0.1. Se observa que la mayor parte del tiempo se va en el MCP, en la invocación de las tools.  |
| Tools con error | chat.decision not_found 00000000-0000-0000-0000-000000000000 3bb2d240a6e0fc3293345701b1a8b353 |

### ¿Qué optimizarías primero y por qué?

- Reducir timeout de llamada de tools que sean consultivas.
- Agregar un try en las tools o CB
- Incluiria el error de la tools en la trazabilidad
- Aumentar las intancias de la tools para mejorara tiempos (si esta en aks por ejemplo) o mejorar el cold start (si esta en aks o en functions). 

### Conclusión

Insights nos ayuda a saber el comportamiendo del agente y poder detectar puntos donde esta habiendo error antes de que la incidencia escale a más. Sin embargo, eso no esto, sino tambín sirve para multiples cosas como optimizar las respuestas del agente, reducir costos y mejorar la experiencia del usuario.