document.addEventListener('DOMContentLoaded', () => {
  const body = document.querySelector('#servicesBody');
  const mobileBody = document.querySelector('#mobileServicesBody');
  const search = document.querySelector('#searchInput');
  const status = document.querySelector('#resultStatus');
  const themeToggle = document.querySelector('#themeToggle');
  const architectureSelect = document.querySelector('#architectureSelect');
  const recommendationArea = document.querySelector('#recommendationArea');
  const filterButtons = [...document.querySelectorAll('[data-filter]')];

  const iconMoon = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5 8.5 8.5 0 1 0 20.5 14.5Z"/></svg>';
  const iconSun = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="3.5"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"/></svg>';
  const setTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('fwg-theme', theme); } catch (_) {}
    if (themeToggle) themeToggle.innerHTML = `${theme === 'dark' ? iconSun : iconMoon}<span>${theme === 'dark' ? 'Light mode' : 'Dark mode'}</span>`;
  };
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('fwg-theme'); } catch (_) {}
  setTheme(savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
  if (themeToggle) themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));

  const policyClass = (value) => value === 'Allowed' ? 'ok' : value === 'Restricted' ? 'trap' : 'trap';
  const cardLabel = (value) => value === 'Required' ? 'Required' : value === 'Conditional' ? 'Conditional' : 'No';
  const cardAlert = (value) => value === 'Required' || value === 'Conditional';
  const sleepText = (service) => service.sleeps ? 'Yes' : 'No';
  const productionText = (service) => service.production_ready ? 'Yes' : 'No';
  const hasTrap = (service) => cardAlert(service.card_requirement) || service.commercial_policy !== 'Allowed' || service.sleeps || !service.production_ready || (service.reclaim_policy && service.reclaim_policy.toLowerCase() !== 'none' && service.reclaim_policy.toLowerCase() !== 'none stated.');

  const conditionMarkup = (service) => {
    const rows = [
      ['Card', cardLabel(service.card_requirement), cardAlert(service.card_requirement)],
      ['Commercial', service.commercial_policy, service.commercial_policy !== 'Allowed'],
      ['Sleeps', sleepText(service), service.sleeps],
      ['Production', productionText(service), !service.production_ready]
    ];
    return rows.map(([label, value, alert]) => `<div class="condition-line${alert ? ' alert' : ''}"><span class="condition-dot"></span><span>${label}: <strong>${value}</strong></span></div>`).join('');
  };

  const conditionBadges = (service) => {
    const items = [
      ['Card', cardLabel(service.card_requirement), cardAlert(service.card_requirement)],
      ['Commercial', service.commercial_policy, service.commercial_policy !== 'Allowed'],
      ['Sleeps', sleepText(service), service.sleeps],
      ['Production', productionText(service), !service.production_ready]
    ];
    return items.map(([label, value, alert]) => `<div class="mobile-condition${alert ? ' alert' : ''}">${label}: <strong>${value}</strong></div>`).join('');
  };

  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const recommendationMap = {
    wordpress: ['infinityfree','byet-host','heliohost'],
    api: ['cloudflare-workers','gcp-cloud-run','deno-deploy'],
    nextjs: ['vercel-hobby','netlify','cloudflare-pages'],
    database: ['neon','supabase','turso'],
    ai: ['hugging-face-spaces','streamlit-community-cloud','google-colab'],
    docker: ['gcp-cloud-run','koyeb','render'],
    static: ['cloudflare-pages','github-pages','firebase-hosting'],
    storage: ['cloudflare-r2','backblaze-b2'],
    vps: ['oracle-cloud','google-cloud'],
    docs: ['github-pages','read-the-docs','gitlab-pages'],
    nocode: ['bubble']
  };

  const renderRecommendations = (services) => {
    if (!recommendationArea || !architectureSelect) return;
    const ids = recommendationMap[architectureSelect.value] || [];
    const selected = ids.map(id => services.find(s => s.id === id)).filter(Boolean);
    recommendationArea.replaceChildren();
    for (const service of selected.slice(0, 3)) {
      const card = document.createElement('article');
      card.className = `condition-card${hasTrap(service) ? ' has-trap' : ''}`;
      card.innerHTML = `
        <div class="condition-top"><h3>${esc(service.name)}</h3><span class="micro">${esc(service.last_verified)}</span></div>
        <div class="limit">${esc(service.hard_limit)}</div>
        <div class="conditions">${conditionMarkup(service)}</div>
        <a class="source-link" href="${esc(service.official_source)}" target="_blank" rel="noopener">Official source ↗</a>`;
      recommendationArea.appendChild(card);
    }
  };

  const load = async () => {
    try {
      const response = await fetch('services.json', {cache:'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const services = Array.isArray(data.services) ? data.services : [];
      if (architectureSelect) architectureSelect.addEventListener('change', () => renderRecommendations(services));
      renderRecommendations(services);

      const render = () => {
        const q = (search?.value || '').trim().toLowerCase();
        const activeFilters = new Set(filterButtons.filter(b => b.classList.contains('active')).map(b => b.dataset.filter));
        const matches = services.filter(service => {
          const haystack = [service.name,service.category,service.free_class,service.card_requirement,service.commercial_policy,service.commercial_note,service.hard_limit,service.best_for,service.brilliant_feature].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) return false;
          if (activeFilters.has('no-card') && service.card_requirement !== 'Not required') return false;
          if (activeFilters.has('no-sleep') && service.sleeps) return false;
          if (activeFilters.has('commercial') && service.commercial_policy !== 'Allowed') return false;
          return true;
        });
        if (body) {
          body.replaceChildren();
          for (const service of matches) {
            const row = document.createElement('tr');
            const policy = `<span class="badge ${policyClass(service.commercial_policy)}">${esc(service.commercial_policy)}</span>`;
            const conditions = `<div class="conditions">${conditionMarkup(service)}</div>`;
            row.innerHTML = `
              <td><div class="service-name">${esc(service.name)}<small>${esc(service.category)}</small></div></td>
              <td><span class="badge blue">${esc(service.free_class)}</span></td>
              <td>${policy}</td>
              <td><span class="badge ${cardAlert(service.card_requirement) ? 'trap' : 'ok'}">${esc(cardLabel(service.card_requirement))}</span></td>
              <td>${conditions}</td>
              <td class="limit">${esc(service.hard_limit)}</td>
              <td><span class="micro">${esc(service.last_verified)}</span></td>
              <td><a class="source-link" href="${esc(service.official_source)}" target="_blank" rel="noopener">Official ↗</a></td>`;
            body.appendChild(row);
          }
        }
        if (mobileBody) {
          mobileBody.replaceChildren();
          for (const service of matches) {
            const article = document.createElement('article');
            article.className = `mobile-card${hasTrap(service) ? ' has-trap' : ''}`;
            article.innerHTML = `
              <div class="mobile-head"><div><div class="mobile-name">${esc(service.name)}</div><div class="mobile-category">${esc(service.category)} · ${esc(service.free_class)}</div></div><span class="micro">${esc(service.last_verified)}</span></div>
              <div class="mobile-limit">${esc(service.hard_limit)}</div>
              <div class="mobile-conditions">${conditionBadges(service)}</div>
              <a class="mobile-source" href="${esc(service.official_source)}" target="_blank" rel="noopener">Official source ↗</a>`;
            mobileBody.appendChild(article);
          }
        }
        if (status) status.textContent = `${matches.length} of ${services.length} services shown`;
      };
      search?.addEventListener('input', render);
      filterButtons.forEach(button => button.addEventListener('click', () => { button.classList.toggle('active'); render(); }));
      render();
    } catch (error) {
      if (body) body.innerHTML = '<tr><td colspan="8">Unable to load services.json. Check the deployed data artifact.</td></tr>';
      if (status) status.textContent = 'Data load failed';
      console.error(error);
    }
  };
  load();
});
