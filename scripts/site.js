(() => {
  const themeButton = document.querySelector('.theme-toggle');
  const themePreference = window.matchMedia('(prefers-color-scheme: light)');
  let explicitTheme = false;
  try { explicitTheme = ['light', 'dark'].includes(localStorage.getItem('portfolio-theme')); } catch {}
  const setTheme = theme => {
    document.documentElement.dataset.theme = theme;
    themeButton?.setAttribute('aria-pressed', String(theme === 'light'));
  };
  if (themeButton) {
    themeButton.hidden = false;
    setTheme(document.documentElement.dataset.theme || (themePreference.matches ? 'light' : 'dark'));
    themeButton.addEventListener('click', () => {
      const theme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      explicitTheme = true;
      setTheme(theme);
      try { localStorage.setItem('portfolio-theme', theme); } catch {}
    });
    themePreference.addEventListener('change', event => {
      if (!explicitTheme) setTheme(event.matches ? 'light' : 'dark');
    });
  }
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const brand = document.querySelector('.terminal-brand');
  const typed = document.querySelector('[data-typewriter]');
  let timer;
  function reset() { clearTimeout(timer); if (typed) typed.textContent = ''; }
  function typeHome() {
    reset();
    if (!typed) return;
    if (reducedMotion.matches) { typed.textContent = 'home'; return; }
    let index = 0;
    const tick = () => {
      typed.textContent = 'home'.slice(0, ++index);
      if (index < 4) timer = setTimeout(tick, 95);
    };
    tick();
  }
  brand?.addEventListener('mouseenter', typeHome);
  brand?.addEventListener('focus', typeHome);
  brand?.addEventListener('mouseleave', () => { if (document.activeElement !== brand) reset(); });
  brand?.addEventListener('blur', reset);

  const search = document.querySelector('#search');
  const platform = document.querySelector('#platform');
  if (search && platform) {
    document.querySelector('.filters').hidden = false;
    const cards = [...document.querySelectorAll('[data-post]')];
    const params = new URLSearchParams(location.search);
    search.value = params.get('q') || '';
    platform.value = params.get('platform') || '';
    if (platform.selectedIndex < 0) platform.value = '';
    const filter = () => {
      const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
      let count = 0;
      cards.forEach(card => {
        const haystack = (card.textContent + ' ' + card.dataset.platform).toLowerCase();
        card.hidden = !terms.every(term => haystack.includes(term)) || (platform.value !== '' && card.dataset.platform !== platform.value);
        if (!card.hidden) count++;
      });
      document.querySelector('#result-count').textContent = `${count} ${count === 1 ? 'entry' : 'entries'}`;
      document.querySelector('#no-results').hidden = count !== 0;
      const query = new URLSearchParams();
      if (search.value) query.set('q', search.value);
      if (platform.value) query.set('platform', platform.value);
      history.replaceState(null, '', location.pathname + (query.size ? '?' + query : '') + location.hash);
    };
    search.addEventListener('input', filter);
    platform.addEventListener('change', filter);
    document.querySelector('#clear-filters').addEventListener('click', () => { search.value = ''; platform.value = ''; filter(); search.focus(); });
    filter();
  }
  document.querySelectorAll('.article-body pre').forEach(pre => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-code';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code to clipboard');
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(pre.querySelector('code').textContent);
        button.textContent = 'Copied';
      } catch { button.textContent = 'Select code to copy'; }
      setTimeout(() => { button.textContent = 'Copy'; }, 2000);
    });
    pre.append(button);
  });
})();
