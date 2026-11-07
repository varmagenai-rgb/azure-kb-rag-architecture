# KB / RAG on Azure: gap-review checklist

Verify current service names and limits via Microsoft Learn before reporting. Score each item: Met / Partial / Missing / N/A.

## Contents
1. Identity and access
2. Ingestion
3. Retrieval quality
4. AI gateway and resilience
5. Safety and compliance
6. Network and secrets
7. Observability and evaluation
8. Cost
9. Channels

## 1. Identity and access
- Entra ID SSO for web and Teams; tokens validated in FastAPI (not only at the front end).
- **Security trimming**: every chunk carries allowed Entra group IDs / user IDs; every search is filtered by the signed-in user's groups (on-behalf-of flow). Missing this can leak SharePoint content.
- Managed identities between services; no API keys in app settings.

## 2. Ingestion
- Event-driven (queue / Event Grid) rather than a blind cron job; add a nightly reconcile as a safety net.
- Idempotent processing keyed on document ID + version + content hash.
- Retries, dead-letter queue, and an alert on DLQ depth.
- Update and delete sync: old chunks removed when a document is replaced or deleted.
- Approval gate honoured: only approved files are indexed; rejected files never enter the pipeline.
- Layout-aware extraction (Document Intelligence layout to Markdown), chunk by headings with overlap, metadata on each chunk (title, page, URL, version, ACL).

## 3. Retrieval quality
- Hybrid search (keyword + vector) with semantic ranker; top-k and re-rank threshold configurable.
- Query decomposition / rewriting for multi-part questions.
- Citations returned with each answer; "I don't know" path when grounding is weak.
- Embedding model and dimensions fixed per index; re-index plan for model changes.

## 4. AI gateway and resilience
- APIM in front of Azure OpenAI: token-per-minute limits per user/app, circuit breaker, fallback to a lower-cost deployment, load balancing across deployments or regions.
- Semantic caching for repeated questions.
- Timeouts, retries with backoff, and a graceful degraded response.

## 5. Safety and compliance
- PII detection/redaction before and after the LLM; logs never contain raw PII.
- Content safety and prompt-injection protection (documents are untrusted input).
- Data residency, retention, and audit requirements documented.

## 6. Network and secrets
- Private endpoints for OpenAI, AI Search, Storage, Key Vault; App Service VNet integration.
- Front Door + WAF as the public entry point.
- Secrets in Key Vault; RBAC least privilege.

## 7. Observability and evaluation
- Application Insights + Log Analytics: latency per stage, token counts per user/request, throttling (429) rate, DLQ depth.
- Golden question set with groundedness / relevance metrics, run before each release.
- Feedback signal (thumbs up/down) stored for tuning.

## 8. Cost
- LLM calls per request counted (answer + validation + decomposition + embeddings).
- Cache hit-rate assumption stated; fallback-model share stated.
- AI Search tier and replicas/partitions sized for document count and QPS.

## 9. Channels
- Teams via Azure Bot Service; WhatsApp via a supported provider (Azure Communication Services or a third party). Confirm message pricing, template rules, and compliance before committing.
