document.addEventListener('DOMContentLoaded', () => {
  const body = document.querySelector('#servicesBody');
  const search = document.querySelector('#searchInput');
  const status = document.querySelector('#resultStatus');
  const themeToggle = document.querySelector('#themeToggle');

  const setTheme = (theme) => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('fwg-theme', theme); } catch (_) {}
    if (themeToggle) themeToggle.textContent = theme === 'dark' ? '☀️ Light mode' : '🌙 Dark mode';
  };
  let savedTheme = null;
  try { savedTheme = localStorage.getItem('fwg-theme'); } catch (_) {}
  const preferredTheme = savedTheme || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  setTheme(preferredTheme);
  if (themeToggle) themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));

  const policyClass = (value) => value === 'Allowed' ? 'success' : value === 'Restricted' ? 'warning' : 'danger';
  const cardLabel = (value) => value === 'Required' ? 'Card required' : value === 'Conditional' ? 'Card conditional' : 'No card';

  const load = async () => {
    try {
      const response = await fetch('services.json', {cache: 'no-store'});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const services = Array.isArray(data.services) ? data.services : [];
      const render = () => {
        const q = (search.value || '').trim().toLowerCase();
        body.replaceChildren();
        let count = 0;
        for (const service of services) {
          const haystack = [service.name, service.category, service.free_class, service.card_requirement, service.commercial_policy, service.commercial_note, service.hard_limit, service.best_for, service.brilliant_feature].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) continue;
          const row = document.createElement('tr');
          const cells = [
            {value: service.name, type: 'name'},
            {value: service.category},
            {value: service.free_class, type: 'badge'},
            {value: cardLabel(service.card_requirement), type: 'card'},
            {value: service.commercial_policy, type: 'policy'},
            {value: service.sleeps ? 'Yes' : 'No', type: 'bool'},
            {value: service.production_ready ? 'Yes' : 'No', type: 'bool'},
            {value: service.hard_limit}
          ];
          cells.forEach(({value, type}) => {
            const cell = document.createElement('td');
            if (type === 'name') { const strong = document.createElement('strong'); strong.textContent = value; cell.appendChild(strong); }
            else if (type === 'badge' || type === 'card') { const badge = document.createElement('span'); badge.className = 'badge'; badge.textContent = value; cell.appendChild(badge); }
            else if (type === 'policy') { const badge = document.createElement('span'); badge.className = `badge policy-${policyClass(value)}`; badge.textContent = value; cell.appendChild(badge); }
            else if (type === 'bool') { cell.textContent = value; cell.className = value === 'Yes' ? 'status-yes' : 'status-no'; }
            else cell.textContent = value;
            row.appendChild(cell);
          });
          const sourceCell = document.createElement('td');
          const link = document.createElement('a'); link.href = service.official_source; link.target = '_blank'; link.rel = 'noopener'; link.textContent = 'Official ↗';
          sourceCell.appendChild(link); row.appendChild(sourceCell); body.appendChild(row); count += 1;
        }
        if (status) status.textContent = `${count} of ${services.length} services shown`;
      };
      search.addEventListener('input', render); render();
    } catch (error) {
      body.innerHTML = '<tr><td colspan="9">Unable to load services.json. Check the deployed data artifact.</td></tr>';
      if (status) status.textContent = 'Data load failed'; console.error(error);
    }
  };
  load();
});
