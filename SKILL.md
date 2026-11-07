---
name: azure-kb-rag-architecture
description: Design and diagram knowledge-base / RAG chatbot architectures on Microsoft Azure (Angular or Node.js front end, Teams and WhatsApp channels, FastAPI on App Service, Entra ID SSO, Azure OpenAI, Azure AI Search, APIM AI gateway, SharePoint plus Power Automate approval ingestion, Document Intelligence). Make sure to use this skill whenever the user asks for an architecture diagram, solution design, HLD, component list, or best-practice review for a chatbot, RAG pipeline, knowledge assistant, document Q&A, or Azure AI application, even if they only say "draw the architecture" or "design the solution". Produces an editable draw.io file with native Azure icons plus a best-practice gap review.
---

# Azure Knowledge-Base / RAG Architecture

Default pattern for this user's projects. Adapt it to each brief; do not apply it blindly.

## Workflow

1. **Confirm the brief.** Collect only what is missing: users and concurrency, channels (web, Teams, WhatsApp), document volume and formats, sensitivity (PII, compliance), latency target, budget, region. If the user gave a brief, extract answers from it instead of re-asking.
2. **Check current guidance.** If a Microsoft Learn MCP connector is available, search it for the Azure Architecture Center RAG guidance and the Well-Architected Framework for AI workloads. Otherwise use web search. Service names, SKUs, model names and preview status change often, so never rely on memory for them.
3. **Choose the pattern.** Start from `assets/kb-rag-default.json`. Copy it and edit: remove channels that are not needed, add or swap services (for example Cosmos DB for chat history, Container Apps instead of App Service). Keep lane structure: channels, edge, application tier, AI gateway, AI and search, identity and operations.
4. **Generate the diagram.**
   ```
   python scripts/generate_drawio.py <spec.json> /mnt/user-data/outputs/<name>.drawio
   ```
   Icon keys are listed in `references/icon-catalog.md`. Non-Azure items (SharePoint, Power Automate, Teams, WhatsApp) are drawn as coloured boxes because they have no Azure icon. If a service needs an icon that is not in the catalog, check that the path exists under `img/lib/azure2/` in the jgraph/drawio repo before adding it to `ICONS` in the script.
5. **Run the gap review.** Walk through `references/kb-rag-checklist.md` and report which items the design satisfies, which are missing, and the risk of each gap. Put the result in the reply as a short table, not a long essay.
6. **Hand off.** Present the `.drawio` file. Mention that it opens in app.diagrams.net, draw.io desktop, or the VS Code draw.io extension, and that every shape is editable. List assumptions made and open questions. Offer the cost estimate as the next step (infrastructure plus tokens).

## Rules

- Diagram labels: service name on line one, role on line two. Keep labels to three lines.
- Always show trust boundaries (public edge, VNet, private endpoints) and the identity flow.
- Always show both flows: the query flow and the ingestion pipeline, as separate pages.
- Never hard-code prices, quotas or model availability. Look them up at the time of the request.
- Flag assumptions that affect cost or compliance (region, data residency, model deployment type, WhatsApp provider).
- When the user's design differs from the checklist, say so plainly and explain the trade-off; do not silently "fix" their choices.

## Output expectations

- `<name>.drawio` with one page per flow.
- A reply containing: pattern summary (3 to 5 lines), gap-review table, assumptions, next step.
