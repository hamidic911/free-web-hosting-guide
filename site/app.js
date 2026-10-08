document.addEventListener('DOMContentLoaded', () => {
  const body = document.querySelector('#servicesBody');
  const search = document.querySelector('#searchInput');
  const status = document.querySelector('#resultStatus');
  if (!body || !search) return;

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
          const haystack = [
            service.name, service.category, service.free_class,
            service.card_requirement, service.commercial_policy,
            service.commercial_note, service.hard_limit,
            service.best_for, service.brilliant_feature
          ].join(' ').toLowerCase();
          if (q && !haystack.includes(q)) continue;

          const row = document.createElement('tr');
          const cells = [
            service.name,
            service.category,
            service.free_class,
            service.card_requirement,
            service.commercial_policy,
            service.sleeps ? 'Yes' : 'No',
            service.production_ready ? 'Yes' : 'No',
            service.hard_limit
          ];
          cells.forEach((value, index) => {
            const cell = document.createElement('td');
            if (index === 0) {
              const strong = document.createElement('strong');
              strong.textContent = value;
              cell.appendChild(strong);
            } else {
              cell.textContent = value;
            }
            row.appendChild(cell);
          });

          const sourceCell = document.createElement('td');
          const link = document.createElement('a');
          link.href = service.official_source;
          link.target = '_blank';
          link.rel = 'noopener';
          link.textContent = 'Official';
          sourceCell.appendChild(link);
          row.appendChild(sourceCell);
          body.appendChild(row);
          count += 1;
        }
        if (status) status.textContent = `${count} of ${services.length} services shown`;
      };

      search.addEventListener('input', render);
      render();
    } catch (error) {
      body.innerHTML = '<tr><td colspan="9">Unable to load services.json. Check the deployed data artifact.</td></tr>';
      if (status) status.textContent = 'Data load failed';
      console.error(error);
    }
  };

  load();
});
