# -*- coding: utf-8 -*-
"""Gera as páginas do site Doutor Impostos a partir de blocos compartilhados.

Uso (na raiz do repositório):  python _src/gerar_paginas.py

- Cria/atualiza as landing pages (medico-pj, equiparacao-hospitalar, trocar-de-contador,
  reforma-tributaria-medicos), /ig, /blog, /politica-de-privacidade, 404.html e sitemap.xml.
- Na index.html, substitui apenas o que está entre os marcadores <!-- @form:start/end -->
  e <!-- @footer:start/end -->, para o formulário e o rodapé ficarem iguais em todo o site.
A pasta _src é ignorada pelo GitHub Pages (Jekyll ignora pastas que começam com "_").
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://doutorimposto.com"
WA = "5581994034692"
WA_URL = f"https://wa.me/{WA}"
INSTAGRAM = "https://www.instagram.com/doutor_impostos/"
CNPJ = "58.848.633/0001-34"
EMAIL = "jardel.queiroz@qemcontabilidade.com"
# ▼ Preencha para exibir no rodapé (exigência do Código de Ética do Contador para publicidade).
RESPONSAVEL_TECNICO = ""   # ex.: "Jardel Queiroz"
CRC = ""                   # ex.: "CRC-PE 000000/O-0"
ANO = 2026
LASTMOD = "2026-09-29"


# ───────────────────────── blocos compartilhados ─────────────────────────
def head(title, desc, path, jsonld=(), extra="", default_source=None, robots=None):
    ds = f' data-default-source="{default_source[0]}" data-default-medium="{default_source[1]}"' if default_source else ""
    ld = "".join(
        f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>\n' for j in jsonld
    )
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR"{ds}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{rb}<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#0B1F3A">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Doutor Impostos">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B1F3A'/%3E%3Ctext x='32' y='44' font-family='Segoe UI,Arial' font-size='34' font-weight='800' text-anchor='middle' fill='%2322C55E'%3EDI%3C/text%3E%3C/svg%3E">
<script>document.documentElement.classList.add('js')</script>
<link rel="stylesheet" href="/assets/site.css">
{extra}{ld}<script src="/assets/di.js" defer></script>
</head>
<body>
"""


def nav(cta_href="#formulario"):
    return f"""<nav class="navbar">
  <div class="container navbar-inner">
    <a href="/" class="navbar-logo">Doutor<span> Impostos</span><span class="navbar-sub">Especialista na tributação da área médica</span></a>
    <div style="display:flex;align-items:center;gap:1rem">
      <div class="navbar-links">
        <a href="/medico-pj/">Médico PJ</a>
        <a href="/equiparacao-hospitalar/">Equiparação hospitalar</a>
        <a href="/reforma-tributaria-medicos/">Reforma tributária</a>
        <a href="/#calculadora">Calculadora</a>
      </div>
      <a href="{cta_href}" class="btn btn-green navbar-cta">Análise gratuita →</a>
    </div>
  </div>
</nav>
"""


def form_block(left_title="Descubra quanto você pode economizar em impostos.",
               left_text="Preencha o formulário. Nossa equipe entra em contato em até 1 dia útil com um diagnóstico personalizado para o seu perfil.",
               box_title="Solicite sua análise tributária"):
    return f"""<!-- @form:start (gerado por _src/gerar_paginas.py — edite lá) -->
<section class="form-section" id="formulario">
  <div class="container">
    <div class="form-wrap">
      <div class="form-left reveal">
        <div class="form-badge">Análise personalizada, gratuita e sem compromisso</div>
        <h2>{left_title}</h2>
        <p>{left_text}</p>
        <ul class="form-list">
          <li>Análise 100% gratuita</li>
          <li>Serve para quem é PF, PJ ou tem clínica</li>
          <li>Sem compromisso de contratação</li>
          <li>Retorno em até 1 dia útil pelo WhatsApp</li>
          <li>Sigilo total das informações</li>
        </ul>
      </div>
      <div class="form-right reveal">
        <div class="form-box">
          <p class="form-box-title">{box_title}</p>
          <div class="form-progress"><span id="formStepLabel">Etapa 1 de 2</span><div class="form-progress-track"><div class="form-progress-fill" id="formProgressFill"></div></div></div>
          <form id="leadForm" novalidate>
            <div class="form-step active" data-step="1">
              <div class="form-group"><label class="form-label" for="nome">Nome completo *</label><input class="form-input" type="text" id="nome" placeholder="Dr. João Silva" autocomplete="name"><span class="form-err" id="err-nome">Informe seu nome.</span></div>
              <div class="form-group"><label class="form-label" for="whatsapp">WhatsApp *</label><input class="form-input" type="tel" id="whatsapp" placeholder="(99) 99999-9999" inputmode="numeric" autocomplete="tel-national"><span class="form-err" id="err-whatsapp">Número inválido.</span></div>
              <div class="form-group"><label class="form-label" for="atuacao">Hoje você atua como *</label><select class="form-select" id="atuacao"><option value="">Selecione...</option><option>Pessoa física (plantões, RPA, carnê-leão)</option><option>Tenho PJ (CNPJ próprio)</option><option>Tenho clínica / consultório com equipe</option><option>Vou abrir minha empresa / recém-formado</option></select><span class="form-err" id="err-atuacao">Selecione uma opção.</span></div>
              <button type="button" class="form-submit" id="nextBtn">Continuar →</button>
            </div>
            <div class="form-step" data-step="2">
              <div class="form-row2">
                <div class="form-group"><label class="form-label" for="faturamento">Faturamento mensal *</label><select class="form-select" id="faturamento"><option value="">Selecione...</option><option>Até R$ 10.000</option><option>R$ 10.000 a R$ 30.000</option><option>R$ 30.000 a R$ 60.000</option><option>R$ 60.000 a R$ 100.000</option><option>Acima de R$ 100.000</option></select><span class="form-err" id="err-faturamento">Selecione.</span></div>
                <div class="form-group"><label class="form-label" for="especialidade">Especialidade</label><select class="form-select" id="especialidade"><option value="">Selecione...</option><option>Clínica médica / generalista</option><option>Anestesiologia</option><option>Cardiologia</option><option>Cirurgia geral</option><option>Cirurgia plástica</option><option>Dermatologia</option><option>Ginecologia e obstetrícia</option><option>Oftalmologia</option><option>Ortopedia</option><option>Pediatria</option><option>Psiquiatria</option><option>Radiologia / imagem</option><option>Odontologia</option><option>Outra</option></select></div>
              </div>
              <div class="form-group"><label class="form-label" for="regime">Regime tributário atual</label><select class="form-select" id="regime"><option value="">Selecione...</option><option>Não tenho CNPJ (pessoa física)</option><option>Simples Nacional</option><option>Lucro Presumido</option><option>Lucro Real</option><option>Não sei</option></select></div>
              <div class="form-group"><label class="form-label" for="email">E-mail <span class="form-hint">(opcional)</span></label><input class="form-input" type="email" id="email" placeholder="joao@clinica.com.br" inputmode="email" autocomplete="email"><span class="form-err" id="err-email">E-mail inválido.</span></div>
              <div class="form-group"><label class="form-label" for="mensagem">Sua principal dúvida <span class="form-hint">(opcional)</span></label><textarea class="form-textarea" id="mensagem" placeholder="Ex.: recebo plantões como PF e quero saber se compensa abrir PJ"></textarea></div>
              <label class="form-check"><input type="checkbox" id="lgpd"><span>Autorizo o contato pelo WhatsApp e concordo com a <a href="/politica-de-privacidade/" target="_blank">Política de Privacidade</a>.</span></label>
              <span class="form-err" id="err-lgpd">Precisamos da sua autorização para entrar em contato.</span>
              <div class="form-fail" id="formFail">Não conseguimos enviar agora. Tente de novo ou <a href="{WA_URL}" target="_blank" rel="noopener" data-loc="form-erro">fale direto no WhatsApp</a>.</div>
              <div class="form-actions"><button type="button" class="form-back" id="backBtn">← Voltar</button><button type="submit" class="form-submit" id="submitBtn">Solicitar análise gratuita →</button></div>
            </div>
            <p class="form-note">🔒 Seus dados são protegidos. Não compartilhamos com terceiros.</p>
          </form>
          <div class="success" id="successMsg">
            <div class="success-icon">✅</div>
            <h3>Solicitação enviada!</h3>
            <p>Nosso time vai analisar seu perfil e entrar em contato em até <strong>1 dia útil</strong> pelo WhatsApp informado. Em instantes você poderá sugerir horários para a conversa.</p>
            <a href="{WA_URL}" target="_blank" rel="noopener" class="success-wa" data-loc="form-sucesso">💬 Falar no WhatsApp agora</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
<!-- @form:end -->
"""


def footer():
    resp = ""
    if RESPONSAVEL_TECNICO and CRC:
        resp = f'<span>Responsável técnico: {RESPONSAVEL_TECNICO} — {CRC}</span>'
    return f"""<!-- @footer:start (gerado por _src/gerar_paginas.py — edite lá) -->
<footer class="footer" id="rodape">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand-col">
        <div class="footer-brand">Doutor<span> Impostos</span></div>
        <div class="footer-brand-sub">Especialista na tributação da área médica</div>
        <p class="footer-desc">Redução tributária legal e estratégica para médicos e clínicas em todo o Brasil.</p>
        <a href="{WA_URL}" target="_blank" rel="noopener" class="footer-wa">💬 Falar no WhatsApp</a>
      </div>
      <div class="footer-cols-wrap">
        <div class="footer-cols">
          <div>
            <div class="footer-col-title">Soluções</div>
            <a href="/medico-pj/" class="footer-link">Médico PF ou PJ</a>
            <a href="/equiparacao-hospitalar/" class="footer-link">Equiparação hospitalar</a>
            <a href="/trocar-de-contador/" class="footer-link">Trocar de contador</a>
            <a href="/reforma-tributaria-medicos/" class="footer-link">Reforma tributária</a>
            <a href="/#calculadora" class="footer-link">Calculadora</a>
            <a href="/blog/" class="footer-link">Conteúdos</a>
          </div>
          <div>
            <div class="footer-col-title">Contato</div>
            <a href="{WA_URL}" target="_blank" rel="noopener" class="footer-link">(81) 99403-4692</a>
            <a href="mailto:{EMAIL}" class="footer-link">{EMAIL}</a>
            <a href="{INSTAGRAM}" target="_blank" rel="noopener" class="footer-link">Instagram @doutor_impostos</a>
            <a href="/politica-de-privacidade/" class="footer-link">Política de privacidade</a>
            <div style="margin-top:.85rem;font-size:.8rem;line-height:1.7;color:rgba(255,255,255,.35)">Seg–Sex: 8h às 18h<br>Atendimento 100% digital, em todo o Brasil</div>
          </div>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© {ANO} Doutor Impostos. Todos os direitos reservados.</span>
      {resp}
      <span>CNPJ: {CNPJ}</span>
    </div>
  </div>
</footer>

<a class="wa-btn" href="{WA_URL}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp" data-loc="botao-flutuante">
  <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 2C6.477 2 2 6.477 2 12c0 1.821.487 3.53 1.338 5.006L2.038 22l5.109-1.295A9.953 9.953 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18a7.962 7.962 0 01-4.069-1.114l-.29-.173-3.033.768.797-2.966-.19-.304A7.962 7.962 0 014 12c0-4.411 3.589-8 8-8s8 3.589 8 8-3.589 8-8 8z"/></svg>
</a>
<!-- @footer:end -->
"""


def faq_section(items, title="Perguntas frequentes", tag="Dúvidas frequentes", gray=True):
    rows = "\n".join(
        f'      <div class="faq-item"><button class="faq-q">{q} <span class="faq-icon">+</span></button><div class="faq-a"><p>{a}</p></div></div>'
        for q, a in items
    )
    return f"""<section class="section{' section--gray' if gray else ''}" id="faq">
  <div class="container">
    <div class="sec-head reveal">
      <div class="tag">{tag}</div>
      <h2 class="h2">{title}</h2>
    </div>
    <div class="faq-list">
{rows}
    </div>
    <div class="center reveal" style="margin-top:2rem">
      <a href="#formulario" class="btn btn-green btn-full" style="max-width:380px;margin:0 auto;padding:1rem 1.5rem">Ainda tem dúvida? Fale com a gente →</a>
    </div>
  </div>
</section>
"""


def faq_jsonld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": strip(q),
                        "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items],
    }


ORG_JSONLD = {
    "@context": "https://schema.org", "@type": "AccountingService",
    "name": "Doutor Impostos", "url": SITE + "/", "image": SITE + "/img/og.jpg",
    "description": "Planejamento tributário e contabilidade especializada para médicos e clínicas em todo o Brasil.",
    "telephone": "+55-81-99403-4692", "areaServed": {"@type": "Country", "name": "Brasil"},
    "sameAs": [INSTAGRAM], "taxID": CNPJ,
}


def crumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


COMO = """<section class="section" id="como">
  <div class="container">
    <div class="sec-head reveal">
      <div class="tag">Como funciona</div>
      <h2 class="h2">3 passos para descobrir quanto você pode economizar</h2>
      <p class="lead" style="margin-top:.75rem">Leva 1 minuto para pedir. O diagnóstico é gratuito e sem compromisso.</p>
    </div>
    <div class="como-steps">
      <div class="como-step reveal"><div class="como-num">1</div><div><div class="como-title">Você preenche o formulário</div><p class="como-desc">Nome, WhatsApp e como você atua hoje. O resto a gente pergunta na conversa.</p></div></div>
      <div class="como-step reveal"><div class="como-num">2</div><div><div class="como-title">Analisamos o seu caso</div><p class="como-desc">Comparamos regimes, município, especialidade e forma de recebimento.</p></div></div>
      <div class="como-step reveal"><div class="como-num">3</div><div><div class="como-title">Você recebe o diagnóstico</div><p class="como-desc">Quanto dá para economizar, o caminho e o custo. Você decide se quer seguir.</p></div></div>
    </div>
  </div>
</section>
"""


def lp_hero(badge, h1, sub, bullets, cta="Quero minha análise gratuita →"):
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    return f"""<section class="hero">
  <div class="container">
    <div class="hero-inner">
      <div>
        <div class="hero-badge"><span class="hero-dot"></span>{badge}</div>
        <h1 class="hero-title">{h1}</h1>
        <p class="hero-sub">{sub}</p>
        <ul class="hero-list">{lis}</ul>
        <div class="hero-btns">
          <a href="#formulario" class="btn btn-green btn-full">{cta}</a>
          <a href="{WA_URL}" target="_blank" rel="noopener" class="btn btn-outline btn-full" data-loc="hero">💬 Tirar dúvida no WhatsApp</a>
        </div>
      </div>
      <div class="hero-photo">
        <div class="hero-photo-wrap">
          <picture><source srcset="/img/especialista.webp" type="image/webp"><img src="/img/especialista.jpg" alt="Especialista do Doutor Impostos" width="720" height="900" loading="eager" fetchpriority="high"></picture>
          <div class="hero-photo-tag"><span>Especialista em tributação médica</span><strong>Doutor Impostos</strong></div>
        </div>
      </div>
    </div>
  </div>
</section>
"""


def dores(tag, title, lead, items):
    cards = "\n".join(
        f'      <div class="dor-item reveal"><div class="dor-icon">{i}</div><div><div class="dor-title">{t}</div><p class="dor-desc">{d}</p></div></div>'
        for i, t, d in items
    )
    return f"""<section class="section section--gray" id="dor">
  <div class="container">
    <div class="sec-head reveal">
      <div class="tag">{tag}</div>
      <h2 class="h2">{title}</h2>
      <p class="lead" style="margin-top:.75rem">{lead}</p>
    </div>
    <div class="dor-grid">
{cards}
    </div>
  </div>
</section>
"""


def table_section(tag, title, lead, head_cols, rows, note, hl_row=None, sid="comparativo"):
    th = "".join(f"<th>{c}</th>" for c in head_cols)
    trs = "".join(
        ('<tr class="hl">' if i == hl_row else "<tr>") + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
        for i, r in enumerate(rows)
    )
    return f"""<section class="section" id="{sid}">
  <div class="container">
    <div class="sec-head reveal">
      <div class="tag">{tag}</div>
      <h2 class="h2">{title}</h2>
      <p class="lead" style="margin-top:.75rem">{lead}</p>
    </div>
    <div class="cmp-wrap reveal"><table class="cmp-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>
    <p class="cmp-note">{note}</p>
    <div class="center reveal" style="margin-top:1.75rem"><a href="#formulario" class="btn btn-green">Quero saber qual é o meu caso →</a></div>
  </div>
</section>
"""


def page(title, desc, path, body, jsonld=(), **kw):
    return head(title, desc, path, jsonld, **kw) + body + "\n</body>\n</html>\n"


def write(rel, content):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    print("gerado:", rel)


# ───────────────────────── landing pages ─────────────────────────
LPS = []

# 1) Médico PF → PJ
faq_pj = [
    ("Médico pode ser MEI?", "Não. A medicina é uma profissão regulamentada e não pode ser exercida como MEI. O caminho costuma ser uma sociedade limitada unipessoal (SLU) ou uma sociedade com outros médicos."),
    ("Preciso de sócio para abrir a empresa?", "Não. Desde 2019 é possível abrir uma sociedade limitada com um único sócio (SLU), sem capital mínimo e sem misturar o patrimônio pessoal com o da empresa."),
    ("A empresa precisa de registro no CRM?", "Sim. A pessoa jurídica que presta serviços médicos precisa de inscrição no CRM do estado, com um diretor técnico médico. A gente cuida desse passo junto com a abertura."),
    ("O que é o Fator R?", "É a regra do Simples Nacional que define se a atividade médica paga pelo Anexo III (a partir de 6%) ou pelo Anexo V (a partir de 15,5%). Quando a folha de pagamento, incluindo o pró-labore, chega a 28% do faturamento, a empresa fica no Anexo III. Planejar o pró-labore faz toda a diferença."),
    ("Simples Nacional ou Lucro Presumido: qual é melhor?", "Depende do faturamento, do município (ISS), de você ter ou não funcionários e dos tipos de serviço. Abaixo de certo faturamento o Simples com Fator R costuma ganhar. Acima disso, o Presumido costuma compensar. Por isso a análise é individual."),
    ("Posso continuar recebendo parte como pessoa física?", "Pode, e às vezes faz sentido. Na análise simulamos os cenários (só PF, só PJ ou misto) e mostramos o que sai mais barato para você."),
]
LPS.append(dict(
    path="/medico-pj/", file="medico-pj/index.html", crumb="Médico PF ou PJ",
    title="Médico PF ou PJ? Quanto você paga a mais recebendo como pessoa física | Doutor Impostos",
    desc="Plantões, RPA e carnê-leão podem chegar a 27,5% de IR. Veja quando abrir PJ compensa para o médico e peça uma análise gratuita.",
    body=nav() + lp_hero(
        "Para médicos que recebem como pessoa física",
        "Ainda recebe como pessoa física? Você pode estar pagando <em>muito mais imposto</em> do que precisa.",
        "Plantões por RPA e consultas no carnê-leão entram na tabela progressiva do IR, que chega a 27,5%. Com um CNPJ bem estruturado, a carga sobre o faturamento costuma ficar entre 6% e 16%, conforme o regime e o município.",
        ["Comparamos PF × Simples × Lucro Presumido no seu caso", "Cuidamos da abertura, do CRM e do Fator R", "Diagnóstico gratuito, sem compromisso"],
    ) + dores(
        "Você se identifica?", "Sinais de que está na hora de avaliar a PJ",
        "Se um destes cenários é o seu, vale fazer a conta com calma.",
        [("🧾", "Recebe plantões por RPA", "E vê até 27,5% de IR retido na fonte, mais o INSS descontado em cada pagamento."),
         ("📅", "Paga carnê-leão todo mês", "Sobre as consultas particulares, na mesma tabela progressiva do IR."),
         ("🏥", "O hospital pediu CNPJ", "Cada vez mais hospitais e clínicas só contratam médicos por pessoa jurídica."),
         ("🤔", "Não sabe qual regime escolher", "Simples com Fator R, Lucro Presumido, equiparação hospitalar... cada um tem regras próprias."),
         ("💸", "Medo de ter mais custo", "Contador, taxas e CRM custam. A análise mostra se a economia paga tudo isso com folga."),
         ("🎓", "Recém-formado ou em residência", "Quem começa já estruturado evita anos pagando imposto a mais.")],
    ) + table_section(
        "Comparativo", "Quanto o médico paga em cada formato",
        "Faixas típicas de carga tributária sobre o faturamento. O número exato depende do seu município e do seu perfil.",
        ["Formato", "Carga típica", "Observação"],
        [["Pessoa física (RPA / carnê-leão)", "Até 27,5% de IR + INSS", "Tabela progressiva: quanto mais ganha, maior a alíquota"],
         ["PJ no Simples (Anexo III, Fator R)", "A partir de 6%", "Exige pró-labore de pelo menos 28% do faturamento"],
         ["PJ no Simples (Anexo V)", "A partir de 15,5%", "Quando o Fator R não é atingido"],
         ["PJ no Lucro Presumido", "Cerca de 13,3% a 16,3%", "IRPJ + CSLL + PIS + Cofins + ISS (2% a 5%)"],
         ["PJ com equiparação hospitalar", "Cerca de 8% a 11%", "Só para receitas de serviços hospitalares elegíveis"]],
        "Valores de referência para 2026, antes de pró-labore e distribuição de lucros. Não substituem a análise individual.",
        hl_row=1,
    ) + COMO + form_block(
        "Descubra se abrir PJ compensa no seu caso.",
        "Conte como você recebe hoje. Em até 1 dia útil respondemos pelo WhatsApp com a comparação PF × PJ para o seu perfil.",
    ) + faq_section(faq_pj, "Dúvidas de quem está pensando em abrir PJ") + footer(),
    faq=faq_pj,
))

# 2) Equiparação hospitalar
faq_eq = [
    ("Consultas também entram na equiparação?", "Não. A base reduzida vale só para a receita de serviços hospitalares, como procedimentos, cirurgias, exames e terapias. As consultas continuam na base de 32%. Por isso a separação correta das receitas é essencial."),
    ("Minha clínica precisa ser um hospital?", "Não. A clínica não precisa ter internação. O STJ firmou que o que conta é a natureza do serviço prestado. A lei também exige que a empresa seja uma sociedade empresária e cumpra as normas da Anvisa."),
    ("Clínica no Simples Nacional pode usar?", "Não. A equiparação vale para empresas no Lucro Presumido. Muitas vezes a análise mostra que sair do Simples e ir para o Presumido com equiparação é o que dá a maior economia."),
    ("Tem risco de autuação?", "Com a documentação certa o risco é baixo: sociedade empresária, alvará sanitário, receitas separadas e notas fiscais corretas. O diagnóstico verifica exatamente esses pontos antes de qualquer mudança."),
    ("Dá para recuperar o que paguei a mais?", "Em muitos casos, sim. Se a clínica já cumpria os requisitos e pagou sem a equiparação, é possível avaliar a recuperação dos valores dos últimos 5 anos. A análise é caso a caso."),
    ("Quais especialidades costumam se enquadrar?", "Clínicas com procedimentos e cirurgias ambulatoriais, diagnóstico por imagem, oftalmologia, dermatologia com procedimentos, ortopedia, endoscopia, oncologia, laboratórios de análises clínicas e anatomia patológica, entre outras."),
]
LPS.append(dict(
    path="/equiparacao-hospitalar/", file="equiparacao-hospitalar/index.html", crumb="Equiparação hospitalar",
    title="Equiparação hospitalar: clínica pagando menos IRPJ e CSLL | Doutor Impostos",
    desc="Clínicas que fazem procedimentos podem reduzir a base do IRPJ de 32% para 8% e da CSLL de 32% para 12%. Veja os requisitos e peça uma análise gratuita.",
    body=nav() + lp_hero(
        "Para clínicas que fazem procedimentos e exames",
        "Sua clínica faz procedimentos? Ela pode pagar <em>até 75% menos IRPJ</em>.",
        "A equiparação hospitalar reduz a base de cálculo do IRPJ de 32% para 8% e da CSLL de 32% para 12% sobre a receita de serviços hospitalares. Está prevista na Lei 9.249/95 e é reconhecida pelo STJ, mas tem requisitos que muitas clínicas não sabem cumprir.",
        ["Verificamos se a sua clínica se enquadra", "Ajustamos contrato social, alvará e notas", "Avaliamos a recuperação dos últimos 5 anos"],
        cta="Quero saber se minha clínica se enquadra →",
    ) + dores(
        "Requisitos", "O que a clínica precisa ter",
        "É aqui que a maioria perde o benefício: não por não ter direito, mas por não estar organizada para ele.",
        [("🏢", "Sociedade empresária", "O contrato social e o registro precisam estar no formato certo. Sociedade simples não se enquadra."),
         ("📋", "Normas da Anvisa", "Alvará sanitário e estrutura compatíveis com os serviços prestados."),
         ("🩺", "Serviços hospitalares", "Procedimentos, cirurgias, exames e terapias. Consultas não entram."),
         ("🧮", "Receitas separadas", "As notas e a contabilidade precisam separar o que é consulta do que é procedimento."),
         ("📑", "Lucro Presumido", "O benefício existe no Lucro Presumido, não no Simples Nacional."),
         ("⏪", "Histórico dos últimos 5 anos", "Se a clínica já cumpria os requisitos, pode haver valores a recuperar.")],
    ) + table_section(
        "Na prática", "Tributos federais sobre a receita de procedimentos",
        "Comparação no Lucro Presumido, sem e com a equiparação hospitalar.",
        ["Tributo", "Sem equiparação", "Com equiparação"],
        [["IRPJ (15% sobre a base)", "4,80%", "1,20%"],
         ["CSLL (9% sobre a base)", "2,88%", "1,08%"],
         ["PIS + Cofins", "3,65%", "3,65%"],
         ["Total federal", "11,33%", "5,93%"],
         ["+ ISS do município", "2% a 5%", "2% a 5%"]],
        "Não inclui o adicional de 10% do IRPJ sobre a base que passar de R$ 20 mil por mês. Valores de referência. A economia real depende da proporção entre procedimentos e consultas.",
        hl_row=3,
    ) + COMO + form_block(
        "Descubra se a sua clínica pode usar a equiparação hospitalar.",
        "Conte o perfil da clínica. Verificamos os requisitos, estimamos a economia mensal e avaliamos se há valores a recuperar.",
        "Análise de equiparação hospitalar",
    ) + faq_section(faq_eq, "Dúvidas sobre equiparação hospitalar") + footer(),
    faq=faq_eq,
))

# 3) Trocar de contador
faq_tc = [
    ("É complicado trocar de contador?", "Não. Você comunica o contador atual conforme o prazo do contrato (normalmente 30 dias) e nós cuidamos do resto: pedimos os documentos, conferimos o histórico e assumimos sem interromper as suas obrigações."),
    ("Vou perder meu histórico?", "Não. O contador anterior é obrigado a entregar a documentação da empresa na transição. Nós recebemos, revisamos e apontamos o que precisa ser corrigido."),
    ("Preciso trocar para fazer a análise?", "Não. O diagnóstico é independente e gratuito. Se preferir, você pode levar o resultado para o seu contador atual."),
    ("E se encontrarem erros do contador anterior?", "Mostramos o que encontramos e o impacto de cada ponto. Muitas vezes há imposto pago a mais que pode ser recuperado."),
    ("Vocês atendem o meu estado?", "Sim. O atendimento é 100% digital, em todo o Brasil, com acompanhamento pelo WhatsApp."),
]
LPS.append(dict(
    path="/trocar-de-contador/", file="trocar-de-contador/index.html", crumb="Trocar de contador",
    title="Contador para médicos: troque para uma contabilidade que reduz impostos | Doutor Impostos",
    desc="Seu contador só manda guia? Contabilidade especializada em médicos, com revisão tributária e troca sem dor de cabeça. Peça uma análise gratuita.",
    body=nav() + lp_hero(
        "Para médicos que já têm CNPJ",
        "Seu contador só manda a guia? Médico precisa de contabilidade que <em>pensa em imposto</em>.",
        "Se ninguém revisa o seu regime há mais de um ano, é provável que você esteja pagando mais do que precisa. Revisamos a sua estrutura de graça e, se quiser trocar, cuidamos da transição.",
        ["Revisão do regime, do pró-labore e da distribuição de lucros", "Transição do contador atual sem você se preocupar", "Atendimento pelo WhatsApp, em todo o Brasil"],
    ) + dores(
        "Sinais de alerta", "Seu contador atual faz isso?",
        "Se a resposta for não para a maioria, vale uma segunda opinião.",
        [("📆", "Revisa o regime todo ano", "O melhor regime muda conforme o faturamento cresce."),
         ("🧮", "Planeja o pró-labore", "O pró-labore define o Fator R no Simples e o INSS que você paga."),
         ("🏥", "Conhece a equiparação hospitalar", "Se você faz procedimentos, isso pode reduzir bastante o IRPJ e a CSLL."),
         ("📣", "Avisa sobre mudanças na lei", "Reforma tributária e a nova tributação de dividendos já estão valendo em 2026."),
         ("⚡", "Responde rápido", "Médico não tem tempo de esperar dias por uma resposta simples."),
         ("📊", "Explica o que você paga", "Você deveria entender cada guia, não só pagar.")],
    ) + """<section class="section" id="transicao">
  <div class="container">
    <div class="sec-head reveal"><div class="tag">Como é a troca</div><h2 class="h2">Você não precisa se preocupar com a burocracia</h2></div>
    <div class="timeline reveal">
      <div class="tl-item now"><div class="tl-year">Passo 1</div><div><div class="tl-title">Diagnóstico gratuito</div><p class="tl-desc">Analisamos a sua estrutura atual e mostramos quanto dá para economizar.</p></div></div>
      <div class="tl-item"><div class="tl-year">Passo 2</div><div><div class="tl-title">Proposta por escrito</div><p class="tl-desc">Escopo, honorário e o que muda. Você decide com calma.</p></div></div>
      <div class="tl-item"><div class="tl-year">Passo 3</div><div><div class="tl-title">Transição</div><p class="tl-desc">Você avisa o contador atual. Nós pedimos os documentos e conferimos o histórico.</p></div></div>
      <div class="tl-item"><div class="tl-year">Passo 4</div><div><div class="tl-title">Nova estrutura</div><p class="tl-desc">Aplicamos o regime e o pró-labore certos a partir da competência seguinte.</p></div></div>
    </div>
  </div>
</section>
""" + form_block(
        "Peça uma segunda opinião sobre os seus impostos.",
        "Diagnóstico gratuito da sua estrutura atual. Se não houver oportunidade de economia, a gente te fala com sinceridade.",
    ) + faq_section(faq_tc, "Dúvidas sobre trocar de contador") + footer(),
    faq=faq_tc,
))

# 4) Reforma tributária
faq_rt = [
    ("Em 2026 eu já pago IBS e CBS?", "2026 é um ano de teste: as notas fiscais passam a destacar CBS (0,9%) e IBS (0,1%), mas quem cumpre as obrigações acessórias fica dispensado do recolhimento. A cobrança efetiva da CBS começa em 2027."),
    ("A saúde vai pagar menos na reforma?", "Os serviços de saúde listados na LC 214/2025 têm redução de 60% nas alíquotas de IBS e CBS. Profissões regulamentadas, como a medicina, também têm uma redução de 30% em algumas situações. Qual se aplica depende do serviço e da estrutura da empresa."),
    ("O que muda nos dividendos?", "Pela Lei 15.270/2025, a partir de 2026 os lucros acima de R$ 50 mil por mês pagos por uma mesma empresa a uma pessoa física têm retenção de 10% de IR. Quem tem renda anual acima de R$ 600 mil passa a ter um IR mínimo. Existe um redutor para evitar tributação excessiva, mas ele exige planejamento."),
    ("O ISS fixo das sociedades uniprofissionais acaba?", "O ISS será substituído gradualmente pelo IBS entre 2029 e 2032. Com isso, o regime de ISS fixo por profissional tende a deixar de existir. Quem depende dele precisa planejar a transição."),
    ("Preciso fazer alguma coisa agora?", "Sim: revisar a forma de retirada dos lucros (pró-labore × dividendos) por causa da nova tributação, conferir se as notas já destacam IBS e CBS corretamente e simular o impacto da transição no seu regime."),
]
LPS.append(dict(
    path="/reforma-tributaria-medicos/", file="reforma-tributaria-medicos/index.html", crumb="Reforma tributária para médicos",
    title="Reforma tributária e dividendos: o que muda para o médico em 2026 e 2027 | Doutor Impostos",
    desc="IBS, CBS, redução de 60% para a saúde e a nova tributação de dividendos acima de R$ 50 mil por mês. Entenda o impacto no médico PJ e na clínica.",
    body=nav() + lp_hero(
        "Atualizado para 2026",
        "Reforma tributária e nova regra dos dividendos: <em>o que muda no bolso do médico</em>.",
        "2026 é o ano de teste do IBS e da CBS e o primeiro ano da retenção de IR sobre dividendos acima de R$ 50 mil por mês. Quem se planejar agora atravessa a transição pagando menos.",
        ["Simulamos o impacto da reforma no seu regime", "Revisamos pró-labore × distribuição de lucros", "Diagnóstico gratuito, sem compromisso"],
        cta="Quero simular o impacto no meu caso →",
    ) + """<section class="section section--gray" id="linha-do-tempo">
  <div class="container">
    <div class="sec-head reveal"><div class="tag">Linha do tempo</div><h2 class="h2">O que acontece em cada ano</h2><p class="lead" style="margin-top:.75rem">Principais marcos para médicos e clínicas (EC 132/2023, LC 214/2025 e Lei 15.270/2025).</p></div>
    <div class="timeline reveal">
      <div class="tl-item now"><div class="tl-year">2026</div><div><div class="tl-title">Ano de teste do IBS e da CBS + IR sobre dividendos</div><p class="tl-desc">As notas destacam CBS de 0,9% e IBS de 0,1%, com dispensa de recolhimento para quem cumpre as obrigações. Lucros acima de R$ 50 mil por mês por empresa passam a ter retenção de 10% de IR, e rendas acima de R$ 600 mil por ano têm IR mínimo.</p></div></div>
      <div class="tl-item"><div class="tl-year">2027</div><div><div class="tl-title">A CBS começa a valer, PIS e Cofins acabam</div><p class="tl-desc">A CBS federal substitui PIS e Cofins. Serviços de saúde têm redução de 60% na alíquota.</p></div></div>
      <div class="tl-item"><div class="tl-year">2029–32</div><div><div class="tl-title">O ISS vai sendo trocado pelo IBS</div><p class="tl-desc">O ISS cai gradualmente e o IBS sobe no lugar. O ISS fixo das sociedades uniprofissionais tende a acabar.</p></div></div>
      <div class="tl-item"><div class="tl-year">2033</div><div><div class="tl-title">Novo sistema completo</div><p class="tl-desc">Só IBS e CBS sobre o consumo (mais o Imposto Seletivo, que não afeta serviços médicos).</p></div></div>
    </div>
    <div class="prose"><div class="callout">Informações gerais, com base na legislação vigente em setembro de 2026. As regras ainda recebem regulamentação. <a href="/blog/reforma-tributaria-clinicas-medicas.html">Leia o artigo completo sobre a reforma para clínicas →</a></div></div>
  </div>
</section>
""" + dores(
        "Pontos de atenção", "Onde o médico pode perder dinheiro na transição",
        "Não é só a alíquota: a forma de receber e de retirar os lucros também muda o resultado.",
        [("💰", "Retirada de lucros", "Distribuições grandes concentradas num mês podem cair na retenção de 10%. Planejar o calendário de retiradas faz diferença."),
         ("🧾", "Notas fiscais", "Notas sem o destaque correto de IBS e CBS podem gerar problemas de conformidade já em 2026."),
         ("🏥", "Redução de 60% para a saúde", "Vale para os serviços listados na lei. Enquadrar corretamente cada receita é o que garante o benefício."),
         ("🤝", "Sociedades uniprofissionais", "Quem paga ISS fixo hoje precisa simular como fica quando o IBS substituir o ISS."),
         ("📊", "Escolha do regime", "Simples, Presumido ou Real: o regime ideal pode mudar com a reforma."),
         ("🏦", "Planos de saúde e convênios", "Mudanças na cadeia podem afetar os repasses e os contratos com as operadoras.")],
    ) + form_block(
        "Simule o impacto da reforma no seu caso.",
        "Mostramos como a reforma e a nova regra dos dividendos afetam a sua estrutura atual, e o que ajustar agora.",
    ) + faq_section(faq_rt, "Dúvidas sobre a reforma tributária") + footer(),
    faq=faq_rt,
))

for lp in LPS:
    write(lp["file"], page(lp["title"], lp["desc"], lp["path"], lp["body"],
                           [ORG_JSONLD, crumbs(lp["crumb"], lp["path"]), faq_jsonld(lp["faq"])]))

# ───────────────────────── /ig (link na bio) ─────────────────────────
ig_body = f"""<main class="ig-page">
  <div class="ig-wrap">
    <div class="ig-head">
      <picture><source srcset="/img/especialista.webp" type="image/webp"><img class="ig-avatar" src="/img/especialista.jpg" alt="Doutor Impostos" width="112" height="112"></picture>
      <div class="ig-name">Doutor<span> Impostos</span></div>
      <p class="ig-bio">Você cuida dos pacientes. Eu cuido dos seus impostos.<br>Planejamento tributário para médicos e clínicas.</p>
    </div>
    <div class="ig-links">
      <a class="ig-link primary" href="#formulario"><span class="ig-link-icon">📋</span><span><span class="ig-link-title">Quero meu diagnóstico gratuito</span><span class="ig-link-sub" style="display:block">Descubra quanto você pode economizar</span></span></a>
      <a class="ig-link" href="/#calculadora"><span class="ig-link-icon">🧮</span><span><span class="ig-link-title">Calculadora de impostos</span><span class="ig-link-sub" style="display:block">Compare os regimes em segundos</span></span></a>
      <a class="ig-link wa" href="{WA_URL}" target="_blank" rel="noopener" data-loc="ig-links"><span class="ig-link-icon">💬</span><span><span class="ig-link-title">Falar no WhatsApp</span><span class="ig-link-sub" style="display:block">Tire uma dúvida rápida</span></span></a>
    </div>
    <div class="ig-section-title">Qual é o seu caso?</div>
    <div class="ig-links">
      <a class="ig-link" href="/medico-pj/"><span class="ig-link-icon">🧾</span><span><span class="ig-link-title">Recebo como pessoa física</span><span class="ig-link-sub" style="display:block">Plantões, RPA, carnê-leão: vale abrir PJ?</span></span></a>
      <a class="ig-link" href="/equiparacao-hospitalar/"><span class="ig-link-icon">🏥</span><span><span class="ig-link-title">Tenho clínica com procedimentos</span><span class="ig-link-sub" style="display:block">Equiparação hospitalar: até 75% menos IRPJ</span></span></a>
      <a class="ig-link" href="/trocar-de-contador/"><span class="ig-link-icon">🔄</span><span><span class="ig-link-title">Já sou PJ e quero uma segunda opinião</span><span class="ig-link-sub" style="display:block">Revisão gratuita da sua estrutura</span></span></a>
      <a class="ig-link" href="/reforma-tributaria-medicos/"><span class="ig-link-icon">📣</span><span><span class="ig-link-title">Reforma tributária e dividendos</span><span class="ig-link-sub" style="display:block">O que muda para o médico em 2026 e 2027</span></span></a>
    </div>
  </div>
</main>
""" + form_block(
    "Veio do Instagram? Peça sua análise gratuita.",
    "Responda 2 perguntas rápidas. Em até 1 dia útil você recebe no WhatsApp o diagnóstico do seu caso.",
) + footer()
write("ig/index.html", page(
    "Doutor Impostos — Links", "Diagnóstico tributário gratuito para médicos, calculadora de impostos e conteúdos do @doutor_impostos.",
    "/ig/", ig_body, [ORG_JSONLD], default_source=("instagram", "bio"), robots="noindex, follow"))

# ───────────────────────── blog ─────────────────────────
blog_body = nav("/#formulario") + """<section class="page-hero"><div class="container"><div class="tag" style="background:rgba(34,197,94,.15);color:#22C55E">Conteúdos</div><h1>Impostos para médicos, sem juridiquês</h1><p>Artigos e guias sobre regime tributário, PJ médica, equiparação hospitalar e reforma tributária.</p></div></section>
<section class="section section--gray"><div class="container">
  <div class="post-list">
    <a class="post-card" href="/blog/reforma-tributaria-clinicas-medicas.html"><div class="tag">Artigo</div><h2>Reforma tributária para clínicas médicas: o que muda em 2026</h2><p>IBS, CBS, a redução de 60% para a saúde e o que fazer agora.</p></a>
    <a class="post-card" href="/reforma-tributaria-medicos/"><div class="tag">Guia</div><h2>Reforma tributária e dividendos: o que muda no bolso do médico</h2><p>Linha do tempo 2026–2033 e a nova retenção de IR sobre lucros acima de R$ 50 mil por mês.</p></a>
    <a class="post-card" href="/medico-pj/"><div class="tag">Guia</div><h2>Médico PF ou PJ: quanto você paga em cada formato</h2><p>Comparativo entre RPA, carnê-leão, Simples com Fator R e Lucro Presumido.</p></a>
    <a class="post-card" href="/equiparacao-hospitalar/"><div class="tag">Guia</div><h2>Equiparação hospitalar: requisitos e economia</h2><p>Como clínicas com procedimentos reduzem a base do IRPJ de 32% para 8%.</p></a>
    <a class="post-card" href="/trocar-de-contador/"><div class="tag">Guia</div><h2>Sinais de que é hora de trocar de contador</h2><p>O que uma contabilidade médica deveria fazer por você e como é a transição.</p></a>
  </div>
</div></section>
""" + footer()
write("blog/index.html", page(
    "Conteúdos sobre impostos para médicos | Doutor Impostos",
    "Artigos e guias sobre tributação médica: PF × PJ, equiparação hospitalar, reforma tributária e dividendos.",
    "/blog/", blog_body, [ORG_JSONLD]))

# ───────────────────────── política de privacidade ─────────────────────────
priv_body = nav("/#formulario") + f"""<section class="page-hero"><div class="container"><h1>Política de Privacidade</h1><p>Última atualização: 29 de setembro de 2026</p></div></section>
<section class="section"><div class="container"><div class="prose">
<p>Esta política explica como o <strong>Doutor Impostos</strong> (CNPJ {CNPJ}) coleta, usa e protege os dados pessoais de quem visita este site ou pede uma análise tributária, conforme a Lei Geral de Proteção de Dados (Lei 13.709/2018, a LGPD).</p>
<h2>1. Quais dados coletamos</h2>
<ul>
<li><strong>Dados que você informa no formulário:</strong> nome, WhatsApp, e-mail (opcional), forma de atuação, especialidade, faixa de faturamento, regime tributário, mensagem e sugestões de horário para a conversa.</li>
<li><strong>Dados de navegação:</strong> páginas visitadas, origem do acesso (por exemplo, anúncio do Google ou Instagram, parâmetros UTM e identificadores de clique como gclid e fbclid), tipo de dispositivo e interações com o site, coletados por cookies e tecnologias semelhantes.</li>
</ul>
<h2>2. Para que usamos os dados</h2>
<ul>
<li>Entrar em contato pelo WhatsApp ou e-mail para fazer e apresentar a análise que você pediu (execução de procedimentos preliminares a um contrato, a seu pedido).</li>
<li>Medir quais canais e anúncios trazem contatos e melhorar o site e as campanhas (legítimo interesse).</li>
<li>Mostrar anúncios do Doutor Impostos para quem já visitou o site, no Google, Instagram e Facebook (legítimo interesse, com a opção de recusa descrita no item 5).</li>
<li>Cumprir obrigações legais e regulatórias.</li>
</ul>
<h2>3. Com quem compartilhamos</h2>
<p>Não vendemos seus dados. Eles são tratados por fornecedores que nos ajudam a operar o site, sempre para as finalidades acima: <strong>Formspree</strong> (recebimento do formulário), <strong>Google</strong> (Google Analytics, Google Ads e Google Tag Manager), <strong>Meta</strong> (Instagram e Facebook), <strong>GitHub</strong> (hospedagem do site) e o <strong>WhatsApp</strong>. Alguns desses fornecedores podem armazenar dados fora do Brasil, com as garantias exigidas pela LGPD.</p>
<h2>4. Por quanto tempo guardamos</h2>
<p>Os dados de contato são guardados enquanto durar a relação comercial ou por até 2 anos após o último contato, se não houver contratação. Depois disso são excluídos, a menos que uma obrigação legal exija guardá-los por mais tempo.</p>
<h2>5. Cookies</h2>
<p>Usamos cookies para medir o site e as campanhas e para mostrar anúncios a quem já nos visitou. Você pode bloquear ou apagar os cookies nas configurações do seu navegador e ajustar suas preferências de anúncios em <a href="https://adssettings.google.com" target="_blank" rel="noopener">adssettings.google.com</a> e nas configurações de anúncios do Instagram e do Facebook.</p>
<h2>6. Seus direitos</h2>
<p>Você pode pedir a qualquer momento: confirmação de que tratamos seus dados, acesso, correção, anonimização ou exclusão, portabilidade, informação sobre o compartilhamento e a revogação do consentimento. Basta falar com a gente pelo WhatsApp <a href="{WA_URL}" target="_blank" rel="noopener">(81) 99403-4692</a> ou pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>7. Segurança</h2>
<p>Adotamos medidas técnicas e organizacionais para proteger os dados contra acesso não autorizado, perda ou uso indevido. As informações tributárias que você compartilha na análise são tratadas com sigilo profissional.</p>
<h2>8. Alterações</h2>
<p>Esta política pode ser atualizada. A data no topo da página mostra a versão em vigor.</p>
</div></div></section>
""" + footer()
write("politica-de-privacidade/index.html", page(
    "Política de Privacidade | Doutor Impostos", "Como o Doutor Impostos coleta, usa e protege seus dados pessoais, conforme a LGPD.",
    "/politica-de-privacidade/", priv_body, []))

# ───────────────────────── 404 ─────────────────────────
nf_body = nav("/#formulario") + """<section class="page-hero" style="min-height:70vh"><div class="container"><h1>Página não encontrada</h1><p>O endereço pode ter mudado. Estes caminhos podem ajudar:</p>
<div class="hero-btns" style="margin-top:1.5rem;max-width:420px"><a href="/" class="btn btn-green btn-full">Ir para a página inicial</a><a href="/#calculadora" class="btn btn-outline btn-full">Abrir a calculadora</a><a href="/blog/" class="btn btn-outline btn-full">Ver conteúdos</a></div></div></section>
""" + footer()
write("404.html", page("Página não encontrada | Doutor Impostos", "Página não encontrada.", "/404.html", nf_body, [], robots="noindex"))

# ───────────────────────── index.html: sincroniza form e rodapé ─────────────────────────
idx = ROOT / "index.html"
src = idx.read_text(encoding="utf-8")
for name, block in (("form", form_block()), ("footer", footer())):
    pat = re.compile(r"<!-- @%s:start.*?<!-- @%s:end -->\n?" % (name, name), re.S)
    if not pat.search(src):
        raise SystemExit(f"marcador @{name} não encontrado na index.html")
    src = pat.sub(lambda m: block, src, count=1)
# FAQ da home → JSON-LD (lido do próprio HTML, para nunca divergir)
pairs = re.findall(r'<button class="faq-q">(.*?) <span class="faq-icon">\+</span></button><div class="faq-a"><p>(.*?)</p>', src)
ld = ('<!-- @faqld:start -->\n<script type="application/ld+json">'
      + json.dumps(faq_jsonld(pairs), ensure_ascii=False) + '</script>\n<!-- @faqld:end -->\n')
src = re.sub(r"<!-- @faqld:start -->.*?<!-- @faqld:end -->\n?", lambda m: ld, src, count=1, flags=re.S)
idx.write_text(src, encoding="utf-8", newline="\n")
print("sincronizado: index.html (form + rodapé)")

# ───────────────────────── sitemap ─────────────────────────
urls = [("/", "1.0"), ("/medico-pj/", "0.9"), ("/equiparacao-hospitalar/", "0.9"), ("/trocar-de-contador/", "0.8"),
        ("/reforma-tributaria-medicos/", "0.8"), ("/blog/", "0.6"), ("/blog/reforma-tributaria-clinicas-medicas.html", "0.7"),
        ("/politica-de-privacidade/", "0.2")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{SITE}{u}</loc><lastmod>{LASTMOD}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n"
write("sitemap.xml", sm)
