# La Casa de la Abuela Leoncia

Landing editorial para compartir la historia y el potencial de la casa.

## Ver en local

```bash
npx --yes serve .
```

## Vista previa al compartir (WhatsApp, etc.)

1. Coloca la imagen social en `public/og-casa-leoncia.png` (ya hay una por defecto; puedes sustituirla).
2. En Vercel → Settings → Environment Variables, añade:

   - **Name:** `NEXT_PUBLIC_SITE_URL`
   - **Value:** `https://tu-proyecto.vercel.app` (la URL pública que te dé Vercel, sin barra final)

3. Cuando tengas dominio propio, solo cambia esa variable.

El build (`npm run build`) genera `dist/` con la URL absoluta inyectada en los metadatos Open Graph y Twitter Card.
