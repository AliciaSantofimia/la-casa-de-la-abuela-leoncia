/**
 * Prepara el deploy estático e inyecta la URL absoluta en metadatos OG/Twitter.
 * Cuando exista dominio propio, solo habrá que actualizar NEXT_PUBLIC_SITE_URL.
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const dist = path.join(root, "dist");

function resolveSiteUrl() {
  let siteUrl = (process.env.NEXT_PUBLIC_SITE_URL || "").trim();

  if (!siteUrl && process.env.VERCEL_PROJECT_PRODUCTION_URL) {
    siteUrl = process.env.VERCEL_PROJECT_PRODUCTION_URL.trim();
  }

  if (!siteUrl && process.env.VERCEL_URL) {
    siteUrl = process.env.VERCEL_URL.trim();
  }

  if (!siteUrl) return "";

  if (!/^https?:\/\//i.test(siteUrl)) {
    siteUrl = `https://${siteUrl}`;
  }

  return siteUrl.replace(/\/$/, "");
}

function copyRecursive(src, dest) {
  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    for (const entry of fs.readdirSync(src)) {
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
    return;
  }
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

const siteUrl = resolveSiteUrl();
const publicOg = path.join(root, "public", "og-casa-leoncia.png");

if (!fs.existsSync(publicOg)) {
  console.error("Falta public/og-casa-leoncia.png");
  process.exit(1);
}

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });

const files = ["index.html", "styles.css", "script.js"];
for (const file of files) {
  copyRecursive(path.join(root, file), path.join(dist, file));
}

copyRecursive(path.join(root, "images"), path.join(dist, "images"));
fs.copyFileSync(publicOg, path.join(dist, "og-casa-leoncia.png"));

const indexPath = path.join(dist, "index.html");
let html = fs.readFileSync(indexPath, "utf8");

if (!html.includes("__SITE_URL__")) {
  console.warn("No se encontró el marcador __SITE_URL__ en index.html");
}

html = html.split("__SITE_URL__").join(siteUrl);
fs.writeFileSync(indexPath, html);

if (!siteUrl) {
  console.warn(
    "SITE_URL vacío. Define NEXT_PUBLIC_SITE_URL en Vercel (ej. https://tu-proyecto.vercel.app)."
  );
} else {
  console.log(`Metadatos inyectados con SITE_URL=${siteUrl}`);
}
