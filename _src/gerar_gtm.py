# -*- coding: utf-8 -*-
"""Gera _src/gtm-doutor-impostos.json para importar no Google Tag Manager
(Administrador → Importar contêiner → Mesclar → Renomear conflitantes).

Depois de importar, edite apenas as 4 variáveis "CONST - ..." com os seus IDs.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "gtm-doutor-impostos.json"
ALL_PAGES = "2147479553"       # acionador nativo "All Pages"
INIT_ALL = "2147479573"        # acionador nativo "Initialization - All Pages"

_ids = iter(range(1, 1000))
def nid():
    return str(next(_ids))

def T(key, value):             # parâmetro de texto
    return {"type": "TEMPLATE", "key": key, "value": value}

def B(key, value):
    return {"type": "BOOLEAN", "key": key, "value": "true" if value else "false"}

base = {"accountId": "0", "containerId": "0"}

# ── variáveis ──
variables = []
def const(name, value):
    variables.append({**base, "variableId": nid(), "name": name, "type": "c", "parameter": [T("value", value)]})
def dlv(path):
    variables.append({**base, "variableId": nid(), "name": "DLV - " + path, "type": "v",
                      "parameter": [{"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
                                    B("setDefaultValue", False), T("name", path)]})

const("CONST - GA4 ID", "G-D6YJZ0Q2N7")
const("CONST - Google Ads ID", "000000000")
const("CONST - Google Ads Rotulo Lead", "XXXXXXXXXXX")
const("CONST - Meta Pixel ID", "000000000000000")
for p in ["lead_atuacao", "lead_faturamento", "lead_especialidade", "lead_source", "link_location",
          "page_path", "faturamento_mensal", "regime_atual"]:
    dlv(p)

# ── acionadores ──
triggers, trig_id = [], {}
for ev in ["generate_lead", "whatsapp_click", "calculator_use", "form_step_1", "agendamento_enviado"]:
    tid = nid()
    trig_id[ev] = tid
    triggers.append({**base, "triggerId": tid, "name": "Evento - " + ev, "type": "CUSTOM_EVENT",
                     "customEventFilter": [{"type": "EQUALS", "parameter": [T("arg0", "{{_event}}"), T("arg1", ev)]}]})

# ── tags ──
tags = []
def tag(name, ttype, params, firing):
    tags.append({**base, "tagId": nid(), "name": name, "type": ttype, "parameter": params,
                 "firingTriggerId": firing, "tagFiringOption": "ONCE_PER_EVENT"})

tag("GA4 - Google tag", "googtag", [T("tagId", "{{CONST - GA4 ID}}")], [INIT_ALL])

def ga4_event(ev, params):
    rows = [{"type": "MAP", "map": [T("parameter", k), T("parameterValue", "{{DLV - %s}}" % k)]} for k in params]
    p = [T("eventName", ev), T("measurementIdOverride", "{{CONST - GA4 ID}}")]
    if rows:
        p.append({"type": "LIST", "key": "eventSettingsTable", "list": rows})
    tag("GA4 - " + ev, "gaawe", p, [trig_id[ev]])

ga4_event("generate_lead", ["lead_atuacao", "lead_faturamento", "lead_especialidade", "lead_source", "page_path"])
ga4_event("whatsapp_click", ["link_location", "page_path"])
ga4_event("calculator_use", ["faturamento_mensal", "regime_atual"])
ga4_event("form_step_1", ["lead_atuacao", "page_path"])
ga4_event("agendamento_enviado", ["lead_atuacao"])

tag("Google Ads - Vinculador de conversões", "gclidw", [], [ALL_PAGES])
tag("Google Ads - Conversão Lead", "awct",
    [T("conversionId", "{{CONST - Google Ads ID}}"), T("conversionLabel", "{{CONST - Google Ads Rotulo Lead}}")],
    [trig_id["generate_lead"]])
tag("Google Ads - Remarketing", "sp", [T("conversionId", "{{CONST - Google Ads ID}}")], [ALL_PAGES])

PIXEL_BASE = """<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{{CONST - Meta Pixel ID}}');
fbq('track', 'PageView');
</script>"""
def html_tag(name, code, firing):
    tag(name, "html", [T("html", code), B("supportDocumentWrite", False)], firing)

html_tag("Meta - Pixel base", PIXEL_BASE, [ALL_PAGES])
html_tag("Meta - Lead", "<script>window.fbq && fbq('track', 'Lead');</script>", [trig_id["generate_lead"]])
html_tag("Meta - Contato WhatsApp", "<script>window.fbq && fbq('track', 'Contact');</script>", [trig_id["whatsapp_click"]])
html_tag("Meta - Agendamento", "<script>window.fbq && fbq('track', 'Schedule');</script>", [trig_id["agendamento_enviado"]])

container = {
    "exportFormatVersion": 2,
    "exportTime": "2026-09-29 00:00:00",
    "containerVersion": {
        "path": "accounts/0/containers/0/versions/0", **base, "containerVersionId": "0",
        "container": {"path": "accounts/0/containers/0", **base, "name": "doutorimposto.com",
                      "publicId": "GTM-5TKSXZFF", "usageContext": ["WEB"]},
        "tag": tags, "trigger": triggers, "variable": variables,
    },
}
OUT.write_text(json.dumps(container, ensure_ascii=False, indent=2), encoding="utf-8")
print("gerado:", OUT, f"({len(tags)} tags, {len(triggers)} acionadores, {len(variables)} variáveis)")

# Versão só com GA4 (para importar antes de existirem as contas de Google Ads e Meta)
ga4 = json.loads(json.dumps(container))
cv = ga4["containerVersion"]
cv["tag"] = [t for t in cv["tag"] if t["name"].startswith("GA4 - ")]
cv["variable"] = [v for v in cv["variable"] if not (v["name"].startswith("CONST - ") and v["name"] != "CONST - GA4 ID")]
OUT_GA4 = OUT.with_name("gtm-somente-ga4.json")
OUT_GA4.write_text(json.dumps(ga4, ensure_ascii=False, indent=2), encoding="utf-8")
print("gerado:", OUT_GA4, f"({len(cv['tag'])} tags)")
