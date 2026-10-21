/* GeoFo service worker: offline support for the installed app (PWA). */
const VERSION = "geofo-2.4.0";
const CORE = [
  "./", "./index.html", "./manifest.webmanifest", "./config.js",
  "./countries.json", "./borders.json", "./globe.json", "./cities.json", "./hydro.json", "./flags.json", "./questions.json",
  "./relief.jpg", "./etopo.jpg", "./sat.jpg", "./hillshade.jpg",
  "./icons/icon-192.png", "./icons/icon-512.png", "./icons/apple-touch-icon.png", "./icons/favicon-32.png",
];
// Cached on first use (CDN libraries, fonts, sharper map tiles, detailed borders)
const RUNTIME_HOSTS = ["cdnjs.cloudflare.com", "cdn.jsdelivr.net", "fonts.googleapis.com", "fonts.gstatic.com"];
// Always live, never cached (detailed maps, search, AI chat)
const LIVE = [/mapy\.com/, /mapy\.cz/, /nominatim\.openstreetmap\.org/, /\/api\//];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || LIVE.some(r => r.test(req.url))) return;
  const sameOrigin = url.origin === self.location.origin;
  if (!sameOrigin && !RUNTIME_HOSTS.includes(url.hostname)) return;

  // Pages: network first (fresh version), cached copy when offline
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put("./index.html", copy)); return r; })
      .catch(() => caches.match("./index.html")));
    return;
  }
  // Everything else: cache first, then network (and remember it)
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => {
    if (r && (r.ok || r.type === "opaque")) { const copy = r.clone(); caches.open(VERSION).then(c => c.put(req, copy)); }
    return r;
  })));
});
