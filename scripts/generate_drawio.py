#!/usr/bin/env python3
"""Generate an editable multi-page draw.io file (native Azure icons) from a JSON spec.

Usage:  python generate_drawio.py spec.json output.drawio

Icons use draw.io's built-in library (img/lib/azure2/...), so the file renders in
app.diagrams.net, draw.io desktop and the VS Code draw.io extension, and every
shape stays fully editable.

Spec shape (see assets/kb-rag-default.json):
  {"pages": [{"name", "title", "width", "height",
              "lanes": [{"id","label","x","y","w","h","style"}],
              "nodes": [{"id","label","icon","x","y"}],
              "edges": [{"from","to","label","dashed","color","exit":[x,y],"entry":[x,y],"via":[[x,y],..]}],
              "notes": {"x","y","w","h","text"}}]}
Edges may start/end at a lane id (lane-to-lane flows keep diagrams clean).
"""
import json
import sys
import xml.dom.minidom as md
from xml.sax.saxutils import escape

B = "img/lib/azure2/"
ICONS = {  # verified against github.com/jgraph/drawio (dev) img/lib/azure2
    "app_service": "app_services/App_Services.svg",
    "apim": "app_services/API_Management_Services.svg",
    "ai_search": "app_services/Search_Services.svg",
    "openai": "ai_machine_learning/Azure_OpenAI.svg",
    "doc_intelligence": "ai_machine_learning/Form_Recognizers.svg",
    "bot_service": "ai_machine_learning/Bot_Services.svg",
    "ai_foundry": "ai_machine_learning/AI_Studio.svg",
    "content_safety": "ai_machine_learning/Content_Safety.svg",
    "ai_services": "ai_machine_learning/Cognitive_Services.svg",
    "key_vault": "security/Key_Vaults.svg",
    "cosmos_db": "databases/Azure_Cosmos_DB.svg",
    "redis": "databases/Cache_Redis.svg",
    "storage": "storage/Storage_Accounts.svg",
    "function_app": "compute/Function_Apps.svg",
    "service_bus": "integration/Service_Bus.svg",
    "event_grid": "integration/Event_Grid_Topics.svg",
    "logic_app": "integration/Logic_Apps.svg",
    "monitor": "management_governance/Monitor.svg",
    "log_analytics": "management_governance/Log_Analytics_Workspaces.svg",
    "app_insights": "devops/Application_Insights.svg",
    "front_door": "networking/Front_Doors.svg",
    "vnet": "networking/Virtual_Networks.svg",
    "private_endpoint": "networking/Private_Endpoint.svg",
    "waf": "networking/Web_Application_Firewall_Policies_WAF.svg",
    "app_gateway": "networking/Application_Gateways.svg",
    "entra_id": "identity/Azure_Active_Directory.svg",
    "synapse": "analytics/Azure_Synapse_Analytics.svg",
}
GENERIC = {  # non-Azure items drawn as coloured boxes: (fill, stroke)
    "user": ("#F2F2F2", "#7F7F7F"),
    "teams": ("#E8E9F8", "#5059C9"),
    "whatsapp": ("#E3F7E9", "#25D366"),
    "spo": ("#DCEEFB", "#0078D4"),
    "power_automate": ("#F5E6F7", "#742774"),
    "approver": ("#FFF4CE", "#C19C00"),
    "reject": ("#FDE7E9", "#D13438"),
    "generic": ("#FFFFFF", "#505050"),
}
LANES = {  # (fill, stroke)
    "ext": ("#FAFAFA", "#A6A6A6"),
    "edge": ("#FFF8F0", "#CA5010"),
    "vnet": ("#F3F9FD", "#0078D4"),
    "m365": ("#F7FAFC", "#106EBE"),
    "ops": ("#F6F6F6", "#605E5C"),
}


def lbl(t):
    """Escape text and turn \\n into <br> for html=1 labels."""
    return "&lt;br&gt;".join(escape(p) for p in t.split("\n"))


def build_page(page):
    out = []
    out.append(
        f'<mxCell id="title" value="{lbl(page["title"])}" style="text;html=1;fontSize=18;'
        f'fontStyle=1;align=left;verticalAlign=middle;" vertex="1" parent="1">'
        f'<mxGeometry x="20" y="8" width="1000" height="32" as="geometry"/></mxCell>'
    )
    for l in page.get("lanes", []):
        fill, stroke = LANES[l.get("style", "ext")]
        out.append(
            f'<mxCell id="{l["id"]}" value="{lbl(l["label"])}" style="rounded=0;html=1;'
            f'verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;fontStyle=1;fontSize=12;'
            f'fontColor={stroke};fillColor={fill};strokeColor={stroke};dashed=1;dashPattern=6 4;" '
            f'vertex="1" parent="1"><mxGeometry x="{l["x"]}" y="{l["y"]}" width="{l["w"]}" '
            f'height="{l["h"]}" as="geometry"/></mxCell>'
        )
    for nd in page.get("nodes", []):
        icon = nd["icon"]
        if icon in ICONS:
            style = ("image;aspect=fixed;html=1;points=[];align=center;fontSize=11;"
                     f"image={B}{ICONS[icon]};verticalLabelPosition=bottom;verticalAlign=top;")
            w = h = 48
        else:
            fill, stroke = GENERIC[icon]
            style = (f"rounded=1;html=1;arcSize=18;fontSize=11;fillColor={fill};"
                     f"strokeColor={stroke};strokeWidth=2;")
            w, h = 130, 48
        out.append(
            f'<mxCell id="{nd["id"]}" value="{lbl(nd["label"])}" style="{style}" vertex="1" '
            f'parent="1"><mxGeometry x="{nd["x"]}" y="{nd["y"]}" width="{w}" height="{h}" '
            f'as="geometry"/></mxCell>'
        )
    for i, e in enumerate(page.get("edges", [])):
        style = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;endArrow=block;"
                 "endFill=1;fontSize=10;labelBackgroundColor=#FFFFFF;"
                 f'strokeColor={e.get("color", "#505050")};strokeWidth=1.5;')
        if e.get("dashed"):
            style += "dashed=1;"
        for key in ("exit", "entry"):
            if key in e:
                style += f"{key}X={e[key][0]};{key}Y={e[key][1]};{key}Dx=0;{key}Dy=0;"
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in e.get("via", []))
        arr = f'<Array as="points">{pts}</Array>' if pts else ""
        out.append(
            f'<mxCell id="e{i}" value="{lbl(e.get("label", ""))}" style="{style}" edge="1" '
            f'parent="1" source="{e["from"]}" target="{e["to"]}">'
            f'<mxGeometry relative="1" as="geometry">{arr}</mxGeometry></mxCell>'
        )
    nt = page.get("notes")
    if nt:
        out.append(
            f'<mxCell id="notes" value="{lbl(nt["text"])}" style="text;html=1;whiteSpace=wrap;'
            f'align=left;verticalAlign=top;fontSize=11;fillColor=#FFFBE6;strokeColor=#C19C00;'
            f'spacing=8;" vertex="1" parent="1"><mxGeometry x="{nt["x"]}" y="{nt["y"]}" '
            f'width="{nt["w"]}" height="{nt["h"]}" as="geometry"/></mxCell>'
        )

    ids = [l["id"] for l in page.get("lanes", [])] + [n["id"] for n in page.get("nodes", [])]
    assert len(ids) == len(set(ids)), f"duplicate ids on page {page['name']}"
    for nd in page.get("nodes", []):
        assert nd["icon"] in ICONS or nd["icon"] in GENERIC, f"unknown icon {nd['icon']!r}"
    for e in page.get("edges", []):
        for k in ("from", "to"):
            assert e[k] in ids, f"edge references unknown id {e[k]!r} on page {page['name']}"

    return (
        f'<diagram name="{escape(page["name"])}" id="{page["name"].replace(" ", "_")}">'
        f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
        f'connect="1" arrows="1" fold="1" page="1" pageScale="1" '
        f'pageWidth="{page.get("width", 1400)}" pageHeight="{page.get("height", 900)}" '
        f'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        f'{"".join(out)}</root></mxGraphModel></diagram>'
    )


def main(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    xml = '<mxfile host="app.diagrams.net">' + "".join(build_page(p) for p in spec["pages"]) + "</mxfile>"
    md.parseString(xml)  # fail loudly if not well-formed
    open(out_path, "w", encoding="utf-8").write(xml)
    print(f"wrote {out_path} ({len(spec['pages'])} pages)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
