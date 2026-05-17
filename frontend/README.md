# Atelier Tools — Frontend

SvelteKit frontend untuk tools-service. Aesthetic: editorial workshop (cream paper, deep ink, oxblood accent), Fraunces serif + IBM Plex.

## Stack

- **SvelteKit 2** (Svelte 5 dengan runes)
- **pnpm** sebagai package manager (via corepack)
- `@sveltejs/adapter-node` — output dijalankan oleh Node 20

## Pages

- `/` — landing
- `/login` — JWT login
- `/profile` — avatar + change password
- `/tools/pdf/merge`, `/split`, `/image-to-pdf` — PDF tools

## Dev (di luar Docker)

```bash
# aktifkan pnpm via corepack (sekali setup di mesin)
corepack enable

cp .env.example .env
pnpm install
pnpm dev   # http://localhost:3000, proxy /api ke localhost:8000
```

## Production / Docker

Image multi-stage `node:20-alpine` + pnpm 9. Saat dijalankan dari root `docker-compose.yml`, frontend nge-proxy `/api/*` ke service `backend` lewat `BACKEND_URL` (default `http://backend:8000`) — lihat `src/hooks.server.js`.

```bash
# dari root tools-service/
docker compose up -d --build
```

Buka `http://localhost:3000`.

## Catatan

- `pnpm-lock.yaml` di-commit untuk reproducible builds. Dockerfile pakai `--frozen-lockfile` kalau lockfile sudah ada.
- Versi pnpm di-pin lewat `packageManager` di `package.json` — corepack akan otomatis pakai versi yang sama.
