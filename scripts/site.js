(() => {
  if (location.pathname.endsWith('/index.html')) {
    history.replaceState(null, '', location.pathname.slice(0, -10) + location.search + location.hash);
  }
  const themeButton = document.querySelector('.theme-toggle');
  const themePreference = window.matchMedia('(prefers-color-scheme: light)');
  let explicitTheme = false;
  try { explicitTheme = ['light', 'dark'].includes(localStorage.getItem('portfolio-theme')); } catch {}
  const setTheme = theme => {
    document.documentElement.dataset.theme = theme;
    if (themeButton) {
      const next = theme === 'light' ? 'Dark Mode' : 'Light Mode';
      themeButton.setAttribute('aria-label', next);
      themeButton.querySelector('[data-theme-icon]').textContent = theme === 'light' ? '☾' : '☀';
      themeButton.querySelector('[data-theme-label]').textContent = next;
    }
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
  const cooldown = 1400;
  let lastTrigger = 0;
  try { lastTrigger = Number(sessionStorage.getItem('portfolio-home-animation')) || 0; } catch {}
  let timer, animating = false, hovered = false, focused = false;
  function rememberTrigger() {
    lastTrigger = Date.now();
    try { sessionStorage.setItem('portfolio-home-animation', String(lastTrigger)); } catch {}
  }
  function reset() {
    if (hovered || focused) return;
    clearTimeout(timer);
    animating = false;
    if (typed) typed.textContent = '';
  }
  function typeHome() {
    if (!typed || animating) return;
    // Hover followed by focus, or arrival after clicking, should not restart typing.
    if (reducedMotion.matches || Date.now() - lastTrigger < cooldown) {
      typed.textContent = 'home';
      return;
    }
    rememberTrigger();
    animating = true;
    let index = 0;
    const tick = () => {
      typed.textContent = 'home'.slice(0, ++index);
      if (index < 4) timer = setTimeout(tick, 95);
      else animating = false;
    };
    tick();
  }
  brand?.addEventListener('mouseenter', () => { hovered = true; typeHome(); });
  brand?.addEventListener('focus', () => { focused = true; typeHome(); });
  brand?.addEventListener('mouseleave', () => { hovered = false; reset(); });
  brand?.addEventListener('blur', () => { focused = false; reset(); });
  brand?.addEventListener('click', () => {
    rememberTrigger();
    clearTimeout(timer);
    animating = false;
    if (typed) typed.textContent = 'home';
  });

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
