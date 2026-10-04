const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../scripts/site.js'), 'utf8');

function page({ session = new Map(), storageBlocked = false, reduced = false, theme = 'dark' } = {}) {
  let now = 10000, nextId = 0;
  const timers = new Map();
  const element = () => ({
    textContent: '', handlers: {}, attrs: {},
    addEventListener(name, callback) { this.handlers[name] = callback; },
    setAttribute(name, value) { this.attrs[name] = value; },
  });
  const brand = element(), typed = element(), button = element(), icon = element(), label = element();
  button.querySelector = selector => selector === '[data-theme-icon]' ? icon : label;
  const document = {
    documentElement: { dataset: { theme } },
    querySelector: selector => ({ '.terminal-brand': brand, '[data-typewriter]': typed, '.theme-toggle': button })[selector],
    querySelectorAll: () => [],
  };
  const storage = map => ({
    getItem(key) { if (storageBlocked) throw Error('blocked'); return map.get(key); },
    setItem(key, value) { if (storageBlocked) throw Error('blocked'); map.set(key, value); },
  });
  let route;
  vm.runInNewContext(source, {
    document, Date: { now: () => now },
    window: { matchMedia: query => ({ matches: query.includes('reduced-motion') && reduced, addEventListener() {} }) },
    localStorage: storage(new Map()), sessionStorage: storage(session),
    location: { pathname: '/index.html', search: '?from=test', hash: '#contact' },
    history: { replaceState: (_, __, url) => { route = url; } },
    setTimeout: (fn, delay) => { timers.set(++nextId, { fn, at: now + delay }); return nextId; },
    clearTimeout: id => timers.delete(id),
  });
  const advance = milliseconds => {
    const end = now + milliseconds;
    while (true) {
      const entry = [...timers].filter(([, t]) => t.at <= end).sort((a, b) => a[1].at - b[1].at)[0];
      if (!entry) break;
      now = entry[1].at; timers.delete(entry[0]); entry[1].fn();
    }
    now = end;
  };
  return { brand, typed, button, icon, label, document, advance, route };
}

test('hover then focus does not restart typing; repeat entry respects cooldown', () => {
  const p = page();
  p.brand.handlers.mouseenter(); p.advance(95);
  assert.equal(p.typed.textContent, 'ho');
  p.brand.handlers.focus();
  assert.equal(p.typed.textContent, 'ho');
  p.advance(190);
  assert.equal(p.typed.textContent, 'home');
  p.brand.handlers.mouseleave(); p.brand.handlers.blur(); p.brand.handlers.mouseenter();
  assert.equal(p.typed.textContent, 'home');
  p.brand.handlers.mouseleave(); p.advance(1400); p.brand.handlers.mouseenter();
  assert.equal(p.typed.textContent, 'h');
});

test('click carries cooldown to the next page without a second animation', () => {
  const session = new Map(), first = page({ session });
  first.brand.handlers.mouseenter(); first.brand.handlers.click();
  const next = page({ session });
  next.brand.handlers.mouseenter();
  assert.equal(next.typed.textContent, 'home');
});

test('light mode offers Dark Mode and moon; next click offers Light Mode and sun', () => {
  const p = page({ theme: 'light', storageBlocked: true });
  assert.equal(p.label.textContent, 'Dark Mode'); assert.equal(p.icon.textContent, '☾');
  p.button.handlers.click();
  assert.equal(p.document.documentElement.dataset.theme, 'dark');
  assert.equal(p.button.attrs['aria-label'], 'Light Mode'); assert.equal(p.icon.textContent, '☀');
});

test('reduced motion and blocked storage still work; legacy home URL preserves query and hash', () => {
  const p = page({ reduced: true, storageBlocked: true });
  p.brand.handlers.focus();
  assert.equal(p.typed.textContent, 'home');
  assert.equal(p.route, '/?from=test#contact');
});
