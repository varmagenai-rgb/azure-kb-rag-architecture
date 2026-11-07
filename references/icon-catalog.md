# Icon catalog

Azure icons (native draw.io library, verified to exist). Use the key in a node's `icon` field.

| key | draw.io image path |
|---|---|
| `app_service` | `img/lib/azure2/app_services/App_Services.svg` |
| `apim` | `img/lib/azure2/app_services/API_Management_Services.svg` |
| `ai_search` | `img/lib/azure2/app_services/Search_Services.svg` |
| `openai` | `img/lib/azure2/ai_machine_learning/Azure_OpenAI.svg` |
| `doc_intelligence` | `img/lib/azure2/ai_machine_learning/Form_Recognizers.svg` |
| `bot_service` | `img/lib/azure2/ai_machine_learning/Bot_Services.svg` |
| `ai_foundry` | `img/lib/azure2/ai_machine_learning/AI_Studio.svg` |
| `content_safety` | `img/lib/azure2/ai_machine_learning/Content_Safety.svg` |
| `ai_services` | `img/lib/azure2/ai_machine_learning/Cognitive_Services.svg` |
| `key_vault` | `img/lib/azure2/security/Key_Vaults.svg` |
| `cosmos_db` | `img/lib/azure2/databases/Azure_Cosmos_DB.svg` |
| `redis` | `img/lib/azure2/databases/Cache_Redis.svg` |
| `storage` | `img/lib/azure2/storage/Storage_Accounts.svg` |
| `function_app` | `img/lib/azure2/compute/Function_Apps.svg` |
| `service_bus` | `img/lib/azure2/integration/Service_Bus.svg` |
| `event_grid` | `img/lib/azure2/integration/Event_Grid_Topics.svg` |
| `logic_app` | `img/lib/azure2/integration/Logic_Apps.svg` |
| `monitor` | `img/lib/azure2/management_governance/Monitor.svg` |
| `log_analytics` | `img/lib/azure2/management_governance/Log_Analytics_Workspaces.svg` |
| `app_insights` | `img/lib/azure2/devops/Application_Insights.svg` |
| `front_door` | `img/lib/azure2/networking/Front_Doors.svg` |
| `vnet` | `img/lib/azure2/networking/Virtual_Networks.svg` |
| `private_endpoint` | `img/lib/azure2/networking/Private_Endpoint.svg` |
| `waf` | `img/lib/azure2/networking/Web_Application_Firewall_Policies_WAF.svg` |
| `app_gateway` | `img/lib/azure2/networking/Application_Gateways.svg` |
| `entra_id` | `img/lib/azure2/identity/Azure_Active_Directory.svg` |
| `synapse` | `img/lib/azure2/analytics/Azure_Synapse_Analytics.svg` |

Non-Azure items (no Azure icon exists):

| key | rendering |
|---|---|
| `user` | coloured box (#7F7F7F) |
| `teams` | coloured box (#5059C9) |
| `whatsapp` | coloured box (#25D366) |
| `spo` | coloured box (#0078D4) |
| `power_automate` | coloured box (#742774) |
| `approver` | coloured box (#C19C00) |
| `reject` | coloured box (#D13438) |
| `generic` | coloured box (#505050) |

Adding an icon: confirm the file exists at `src/main/webapp/img/lib/azure2/<folder>/<File>.svg` in the jgraph/drawio repo, then add it to `ICONS` in `scripts/generate_drawio.py`.
