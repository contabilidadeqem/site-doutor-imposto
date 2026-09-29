/* Doutor Impostos — rastreamento, atribuição de origem, WhatsApp e formulário de lead.
   Usado por todas as páginas. Configure o ID do Google Tag Manager abaixo. */
(function () {
  'use strict';

  var CONFIG = {
    // ▼ Troque pelo ID do contêiner do Google Tag Manager (ex.: GTM-AB12CD3).
    //   GA4, Google Ads e Meta Pixel são configurados DENTRO do GTM — não aqui.
    gtmId: 'GTM-XXXXXXX',
    formEndpoint: 'https://formspree.io/f/mykbrqqr',
    whatsapp: '5581994034692',
    agendamentoUrl: '/agendamento.html'
  };
  window.DI_CONFIG = CONFIG;

  /* ───────────── dataLayer / GTM ───────────── */
  window.dataLayer = window.dataLayer || [];
  function track(event, params) {
    var o = { event: event };
    if (params) for (var k in params) if (Object.prototype.hasOwnProperty.call(params, k)) o[k] = params[k];
    window.dataLayer.push(o);
  }
  window.diTrack = track;

  if (/^GTM-[A-Z0-9]+$/.test(CONFIG.gtmId) && CONFIG.gtmId !== 'GTM-XXXXXXX') {
    window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtm.js?id=' + CONFIG.gtmId;
    document.head.appendChild(g);
  }

  /* ───────────── Atribuição (UTM / GCLID / FBCLID) ─────────────
     di_ft = primeiro contato, di_lt = último contato com origem identificada. */
  var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'fbclid'];
  function sGet(k) { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }
  function sSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  function detectTouch() {
    var qs = new URLSearchParams(location.search), t = {}, found = false;
    KEYS.forEach(function (k) { var v = qs.get(k); if (v) { t[k] = v.slice(0, 200); found = true; } });
    if (!found) {
      var ds = document.documentElement.dataset;
      var ref = '';
      try { ref = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) {}
      if (ref && ref.replace(/^www\./, '') !== location.hostname.replace(/^www\./, '')) {
        t.utm_source = ref.replace(/^(www|l|lm|m)\./, '');
        t.utm_medium = /google\.|bing\.|yahoo\.|duckduckgo\./.test(ref) ? 'organic'
          : /instagram\.|facebook\.|fb\.|linkedin\.|youtube\.|t\.co$/.test(ref) ? 'social' : 'referral';
        found = true;
      } else if (ds.defaultSource) {
        // Páginas como /ig definem uma origem padrão (o app do Instagram costuma não enviar referrer).
        t.utm_source = ds.defaultSource;
        t.utm_medium = ds.defaultMedium || '';
        found = true;
      }
    }
    if (!found) return null;
    t.landing_page = location.pathname;
    t.ts = new Date().toISOString();
    return t;
  }
  var touch = detectTouch();
  if (touch) { if (!sGet('di_ft')) sSet('di_ft', touch); sSet('di_lt', touch); }
  else if (!sGet('di_ft')) sSet('di_ft', { utm_source: '(direct)', utm_medium: '(none)', landing_page: location.pathname, ts: new Date().toISOString() });

  function attribution() {
    var out = {}, ft = sGet('di_ft') || {}, lt = sGet('di_lt') || ft;
    KEYS.concat(['landing_page']).forEach(function (k) {
      if (lt[k]) out[k] = lt[k];
      if (ft[k]) out['primeiro_' + k] = ft[k];
    });
    out.pagina_conversao = location.pathname;
    out.referrer = document.referrer || '';
    return out;
  }
  window.diAttribution = attribution;

  /* ───────────── WhatsApp: rastreia clique + mensagem com origem ───────────── */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (!a) return;
    var sec = a.getAttribute('data-loc') || (a.closest('section,footer,nav') || {}).id || a.className || 'pagina';
    track('whatsapp_click', { link_location: String(sec).slice(0, 60), page_path: location.pathname });
    if (a.href.indexOf('text=') === -1) {
      var lt = sGet('di_lt') || {};
      var origem = lt.utm_source ? ' (origem: ' + lt.utm_source + (lt.utm_campaign ? ' / ' + lt.utm_campaign : '') + ')' : '';
      a.href = 'https://wa.me/' + CONFIG.whatsapp + '?text=' +
        encodeURIComponent('Olá! Vim pelo site do Doutor Impostos e quero entender como pagar menos imposto.' + origem);
    }
  }, true);

  /* ───────────── UI comum ───────────── */
  var nav = document.querySelector('.navbar');
  if (nav) window.addEventListener('scroll', function () {
    nav.style.boxShadow = window.scrollY > 60 ? '0 4px 16px rgba(0,0,0,.2)' : 'none';
  }, { passive: true });

  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = this.getAttribute('href');
      if (id.length < 2) return;
      var t = document.querySelector(id);
      if (t) { e.preventDefault(); window.scrollTo({ top: t.getBoundingClientRect().top + window.scrollY - 68, behavior: 'smooth' }); }
    });
  });

  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en, i) {
        if (en.isIntersecting) { setTimeout(function () { en.target.classList.add('visible'); }, i * 70); obs.unobserve(en.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { obs.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('visible'); });
  }

  document.querySelectorAll('.faq-q').forEach(function (btn) {
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () {
      var item = btn.parentElement, open = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (el) {
        el.classList.remove('open');
        el.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
      });
      if (!open) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  /* ───────────── Formulário de lead (2 etapas) ───────────── */
  var form = document.getElementById('leadForm');
  if (!form) return;

  function $(id) { return document.getElementById(id); }
  function val(id) { var el = $(id); return el ? el.value.trim() : ''; }

  var wa = $('whatsapp');
  wa.addEventListener('input', function () {
    var v = wa.value.replace(/\D/g, '').slice(0, 11);
    if (v.length > 7) v = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
    else if (v.length > 2) v = '(' + v.slice(0, 2) + ') ' + v.slice(2);
    else if (v.length > 0) v = '(' + v;
    wa.value = v;
  });

  var started = false;
  form.addEventListener('focusin', function () {
    if (started) return;
    started = true;
    track('form_start', { page_path: location.pathname });
  });

  function setF(id, valid) {
    var el = $(id), err = $('err-' + id);
    if (el) el.classList.toggle('err', !valid);
    if (err) err.classList.toggle('show', !valid);
    return valid;
  }
  function focusFirstError() {
    var f = form.querySelector('.form-step.active .err');
    if (f) { f.scrollIntoView({ behavior: 'smooth', block: 'center' }); if (f.focus) f.focus({ preventScroll: true }); }
  }

  function validateStep1() {
    return [
      setF('nome', val('nome').length >= 3),
      setF('whatsapp', /^\(\d{2}\)\s\d{4,5}-\d{4}$/.test(val('whatsapp'))),
      setF('atuacao', val('atuacao') !== '')
    ].every(Boolean);
  }
  function validateStep2() {
    var email = val('email');
    var lgpd = $('lgpd').checked;
    $('lgpd').closest('.form-check').classList.toggle('err', !lgpd);
    $('err-lgpd').classList.toggle('show', !lgpd);
    return [
      setF('faturamento', val('faturamento') !== ''),
      setF('email', email === '' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)),
      lgpd
    ].every(Boolean);
  }

  function goStep(n) {
    form.querySelectorAll('.form-step').forEach(function (s) { s.classList.toggle('active', s.getAttribute('data-step') === String(n)); });
    $('formStepLabel').textContent = 'Etapa ' + n + ' de 2';
    $('formProgressFill').style.width = n === 1 ? '50%' : '100%';
    var first = form.querySelector('.form-step.active select, .form-step.active input');
    if (first && n === 2) first.focus({ preventScroll: true });
  }

  $('nextBtn').addEventListener('click', function () {
    if (!validateStep1()) { focusFirstError(); return; }
    track('form_step_1', { page_path: location.pathname, lead_atuacao: val('atuacao') });
    goStep(2);
  });
  $('backBtn').addEventListener('click', function () { goStep(1); });
  // Enter na etapa 1 avança em vez de enviar
  form.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && form.querySelector('.form-step[data-step="1"].active')) {
      e.preventDefault(); $('nextBtn').click();
    }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (form.querySelector('.form-step[data-step="1"].active')) { $('nextBtn').click(); return; }
    if (!validateStep2()) { focusFirstError(); return; }

    var btn = $('submitBtn'), fail = $('formFail'), label = btn.textContent;
    btn.disabled = true; btn.textContent = 'Enviando...'; fail.classList.remove('show');

    var lead = {
      nome: val('nome'), whatsapp: val('whatsapp'), atuacao: val('atuacao'),
      especialidade: val('especialidade'), faturamento: val('faturamento'), regime: val('regime'),
      email: val('email'), mensagem: val('mensagem') || '(não informada)', consentimento_lgpd: 'sim'
    };
    var attr = attribution();
    var payload = { _subject: 'Novo lead — Doutor Impostos (' + (attr.utm_source || 'direto') + ')' };
    if (lead.email) payload._replyto = lead.email;
    for (var k in lead) payload[k] = lead[k];
    for (var a in attr) payload[a] = attr[a];

    fetch(CONFIG.formEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      var digits = lead.whatsapp.replace(/\D/g, '');
      track('generate_lead', {
        page_path: location.pathname,
        lead_atuacao: lead.atuacao, lead_faturamento: lead.faturamento,
        lead_especialidade: lead.especialidade, lead_regime: lead.regime,
        lead_source: attr.utm_source || '(direct)',
        // Para conversões otimizadas do Google Ads (o GTM envia com hash). Não mande isto para o GA4.
        user_data: { email: lead.email || undefined, phone_number: digits ? '+55' + digits : undefined }
      });
      try { sessionStorage.setItem('doutorImpostosLead', JSON.stringify(payload)); } catch (err) {}
      form.style.display = 'none';
      $('successMsg').classList.add('show');
      setTimeout(function () { window.location.href = CONFIG.agendamentoUrl; }, 4000);
    }).catch(function () {
      btn.disabled = false; btn.textContent = label;
      fail.classList.add('show');
      track('form_error', { page_path: location.pathname });
    });
  });
})();
