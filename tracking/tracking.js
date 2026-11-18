/* Geopoint Leads lead tracking.
 * The site has no forms of its own. Its two lead actions are:
 *   - "Get Started"  -> geopoint.leadportal.com (partner signup)
 *   - "Schedule intro call" -> HighLevel booking widget (geopoint-leads-intro)
 * A click on either is sent as a lead to GA4 (generate_lead), Meta (Lead) and Clarity (tag).
 * Page views on in-app route changes are sent to Meta (GA4 enhanced measurement handles its own).
 */
(function () {
  function lead(method, url) {
    try { window.gtag && gtag('event', 'generate_lead', { method: method, link_url: url, page_path: location.pathname }); } catch (e) {}
    try { window.fbq && fbq('track', 'Lead', { content_name: method }); } catch (e) {}
    try { window.clarity && clarity('set', 'lead', method); clarity && clarity('event', 'lead_' + method); } catch (e) {}
  }

  function methodFor(el) {
    var href = (el.getAttribute && el.getAttribute('href')) || '';
    var text = (el.textContent || '').trim().toLowerCase();
    if (/leadportal\.com/i.test(href) || /get started/.test(text)) return 'partner_signup';
    if (/leadconnectorhq\.com\/widget\/bookings|msgsndr|\/booking/i.test(href) || /schedule.*call|book.*call/.test(text)) return 'intro_call';
    return null;
  }

  document.addEventListener('click', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('a,button') : null;
    if (!el) return;
    var m = methodFor(el);
    if (m) lead(m, el.getAttribute('href') || '');
  }, true);

  // HighLevel booking widget confirms bookings via postMessage when embedded.
  window.addEventListener('message', function (ev) {
    try {
      var d = typeof ev.data === 'string' ? ev.data : JSON.stringify(ev.data || '');
      if (/leadconnectorhq|msgsndr/.test(ev.origin) && /booked|appointment|form-submit|submitted/i.test(d)) lead('intro_call_booked', ev.origin);
    } catch (e) {}
  });

  // SPA route changes -> Meta PageView
  var last = location.pathname;
  function onRoute() {
    if (location.pathname === last) return;
    last = location.pathname;
    try { window.fbq && fbq('track', 'PageView'); } catch (e) {}
  }
  ['pushState', 'replaceState'].forEach(function (k) {
    var orig = history[k];
    history[k] = function () { var r = orig.apply(this, arguments); setTimeout(onRoute, 0); return r; };
  });
  window.addEventListener('popstate', onRoute);
})();
