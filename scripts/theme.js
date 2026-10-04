// Apply the saved preference before styles paint; storage may be unavailable.
(() => {
  let saved;
  try { saved = localStorage.getItem('portfolio-theme'); } catch {}
  const system = window.matchMedia('(prefers-color-scheme: light)');
  document.documentElement.dataset.theme = ['light', 'dark'].includes(saved)
    ? saved : (system.matches ? 'light' : 'dark');
})();
