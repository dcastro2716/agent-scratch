Línea base (S5)

Resumen de 30 casos (juez local):
  recall@5: 0.89   intención: 1.00   fuentes: 0.87   hechos: 0.70
  apoyo: 5.0/5   relevancia: 5.0/5   cita correcta: 1.0
  fugas de datos personales: 0   citas de fuentes prohibidas: 1
  tokens: 27839 de entrada, 14192 de salida
Detalle de cada caso: C:\Users\acong_vzysd7t\labs\agent-scratch\data\eval\fees-20261112-075416.json


Resumen de 31 casos (juez local):
  recall@5: 0.89   intención: 1.00   fuentes: 0.87   hechos: 0.68
  apoyo: 5.0/5   relevancia: 4.9/5   cita correcta: 0.9
  fugas de datos personales: 0   citas de fuentes prohibidas: 1
  tokens: 28639 de entrada, 14996 de salida
Detalle de cada caso: C:\Users\acong_vzysd7t\labs\agent-scratch\data\eval\fees-20261112-081451.json


chunks más chicos
INFO agent.infrastructure.bootstrap: Foundry auth provider: entra_id
INFO azure.identity._credentials.environment: No environment configuration found.
INFO azure.identity._credentials.managed_identity: ManagedIdentityCredential will use IMDS
INFO azure.core.pipeline.policies.http_logging_policy: Request URL: 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=REDACTED'
Request method: 'GET'
Request headers:
    'x-ms-client-request-id': '372073a5-de9b-11f1-8c59-c03c59915bdf'
    'User-Agent': 'azsdk-python-identity/1.26.0 Python/3.12.10 (Windows-11-10.0.26200-SP0)'
No body was attached to the request
INFO azure.identity._credentials.chained: DefaultAzureCredential acquired a token from AzureCliCredential
INFO httpx2: HTTP Request: POST https://aif-workshop-jsu3.services.ai.azure.com/openai/v1/embeddings "HTTP/1.1 200 OK"
INFO httpx2: HTTP Request: POST https://aif-workshop-jsu3.services.ai.azure.com/openai/v1/embeddings "HTTP/1.1 200 OK"
   2  additional-services-fees.docx
   3  atm-network.html
   3  credit-cards-fees.pdf
   3  fee-refund-policy.docx
   4  fees-faq.md
   4  fees-glossary.md
   1  internal-notice-parking.md
   3  itf-tax.md
   2  savings-accounts-fees.html
   1  transfer-fees-2024.csv
   1  transfer-fees.csv
   2  undue-charges-cases.pdf
29 chunks de 12 documentos -> C:\Users\acong_vzysd7t\labs\agent-scratch\data\chunks\fees.json
PS C:\Users\acong_vzysd7t\labs\agent-scratch> uv run ingest publish
29 chunks en C:\Users\acong_vzysd7t\labs\agent-scratch\data\index\fees


menos fragmentos
INFO agent.infrastructure.bootstrap: Foundry auth provider: entra_id
INFO azure.identity._credentials.environment: No environment configuration found.
INFO azure.identity._credentials.managed_identity: ManagedIdentityCredential will use IMDS
INFO azure.core.pipeline.policies.http_logging_policy: Request URL: 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=REDACTED'
Request method: 'GET'
Request headers:
    'x-ms-client-request-id': '6015b534-de9b-11f1-8f2a-c03c59915bdf'
    'User-Agent': 'azsdk-python-identity/1.26.0 Python/3.12.10 (Windows-11-10.0.26200-SP0)'
No body was attached to the request
INFO azure.identity._credentials.chained: DefaultAzureCredential acquired a token from AzureCliCredential
INFO httpx2: HTTP Request: POST https://aif-workshop-jsu3.services.ai.azure.com/openai/v1/embeddings "HTTP/1.1 200 OK"
INFO httpx2: HTTP Request: POST https://aif-workshop-jsu3.services.ai.azure.com/openai/v1/embeddings "HTTP/1.1 200 OK"
   2  additional-services-fees.docx
   3  atm-network.html
   3  credit-cards-fees.pdf
   3  fee-refund-policy.docx
   4  fees-faq.md
   4  fees-glossary.md
   1  internal-notice-parking.md
   3  itf-tax.md
   2  savings-accounts-fees.html
   1  transfer-fees-2024.csv
   1  transfer-fees.csv
   2  undue-charges-cases.pdf
29 chunks de 12 documentos -> C:\Users\acong_vzysd7t\labs\agent-scratch\data\chunks\fees.json
PS C:\Users\acong_vzysd7t\labs\agent-scratch> uv run ingest publish
29 chunks en C:\Users\acong_vzysd7t\labs\agent-scratch\data\index\fees



más fragmentos
INFO agent.infrastructure.bootstrap: Foundry auth provider: entra_id
INFO azure.identity._credentials.environment: No environment configuration found.
INFO azure.identity._credentials.managed_identity: ManagedIdentityCredential will use IMDS
INFO azure.core.pipeline.policies.http_logging_policy: Request URL: 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=REDACTED'
Request method: 'GET'
Request headers:
    'x-ms-client-request-id': '77ddef67-de9b-11f1-b828-c03c59915bdf'
    'User-Agent': 'azsdk-python-identity/1.26.0 Python/3.12.10 (Windows-11-10.0.26200-SP0)'
No body was attached to the request
INFO azure.identity._credentials.chained: DefaultAzureCredential acquired a token from AzureCliCredential
INFO httpx2: HTTP Request: POST https://aif-workshop-jsu3.services.ai.azure.com/openai/v1/embeddings "HTTP/1.1 200 OK"
INFO httpx2: HTTP Request: POST https://aif-workshop-jsu3.services.ai.azure.com/openai/v1/embeddings "HTTP/1.1 200 OK"
   2  additional-services-fees.docx
   3  atm-network.html
   3  credit-cards-fees.pdf
   3  fee-refund-policy.docx
   4  fees-faq.md
   4  fees-glossary.md
   1  internal-notice-parking.md
   3  itf-tax.md
   2  savings-accounts-fees.html
   1  transfer-fees-2024.csv
   1  transfer-fees.csv
   2  undue-charges-cases.pdf
29 chunks de 12 documentos -> C:\Users\acong_vzysd7t\labs\agent-scratch\data\chunks\fees.json
PS C:\Users\acong_vzysd7t\labs\agent-scratch> uv run ingest publish
29 chunks en C:\Users\acong_vzysd7t\labs\agent-scratch\data\index\fees


Resumen de 31 casos (juez azure_evaluation):
  recall@8: 1.00   intención: 1.00   fuentes: 0.97   hechos: 0.71
  apoyo: 5.0/5   relevancia: 4.9/5   cita correcta: 1.0
  fugas de datos personales: 0   citas de fuentes prohibidas: 1
  tokens: 36806 de entrada, 14162 de salida
Detalle de cada caso: C:\Users\acong_vzysd7t\labs\agent-scratch\data\eval\fees-20261112-082405.json