# Tools Service

Self-hosted web tools (PDF merge, split, image-to-PDF, dll) berbasis microservices.
Satu perintah untuk menjalankan stack lengkap.

## Stack

| Service | Stack | Port (host) |
|---|---|---|
| **frontend** | SvelteKit 2 + Svelte 5 + pnpm + adapter-node | 3000 |
| **backend** | FastAPI + SQLAlchemy + JWT (bcrypt) | 8000 |
| **worker** | Python stdlib scheduler — cleanup outputs | — |
| **postgres** | postgres:16-alpine | 55432 |

Frontend nge-proxy `/api/*` ke backend lewat docker network — browser tidak butuh CORS.
Backend & worker share volume `./storage` (uploads, outputs, avatars).

## Struktur

```
tools-service/
├── docker-compose.yml          # orchestrator
├── .env / .env.example          # shared config (JWT, ports, TTL)
├── storage/                     # persisted: avatars/, outputs/, uploads/
├── backend/                     # FastAPI
├── frontend/                    # SvelteKit
└── worker/                      # cleanup scheduler
```

## Prasyarat

- Docker + Docker Compose (Docker Desktop, atau engine native + WSL2)
- Tidak perlu install Python, Node, atau Postgres di host

## Quick start

```bash
# 1. Salin env template (kalau .env belum ada)
cp .env.example .env

# 2. Build & start semua service
docker compose up -d --build

# 3. Tunggu ~20 detik sampai healthy, lalu bikin user pertama
docker compose exec backend python -m app.cli create-user admin password123

# 4. Buka di browser
# http://localhost:3000
```

Login dengan kredensial yang baru dibuat.

## Endpoints

### Auth (publik)
- `POST /api/auth/login` — `{username, password}` → `{access_token}`

### Profile (butuh JWT)
- `GET /api/profile/me`
- `POST /api/profile/avatar` (multipart `file`)
- `GET /api/profile/avatar/{user_id}` — publik (untuk `<img src>`)
- `POST /api/profile/change-password`

### Tools — PDF (butuh JWT)
- `POST /api/tools/pdf/merge` — multipart `files[]` (≥2 PDF)
- `POST /api/tools/pdf/split` — `file`, `start_page`, `end_page`
- `POST /api/tools/pdf/image-to-pdf` — multipart `files[]` (JPEG/PNG/WebP)

Dokumentasi otomatis di **http://localhost:8000/docs**.

## Manajemen

```bash
# Status & logs
docker compose ps
docker compose logs -f backend
docker compose logs -f worker

# Stop tanpa hapus data
docker compose down

# Stop + hapus database (⚠️ destructive)
docker compose down -v

# Rebuild satu service
docker compose up -d --build frontend

# CLI backend
docker compose exec backend python -m app.cli create-user <user> <pass>
docker compose exec backend python -m app.cli reset-password <user> <pass>
```

## Konfigurasi (`.env`)

| Variable | Default | Keterangan |
|---|---|---|
| `POSTGRES_USER/PASSWORD/DB` | pdftools | Kredensial Postgres |
| `POSTGRES_PORT` | 55432 | Port host (container internal tetap 5432) |
| `BACKEND_PORT` | 8000 | |
| `FRONTEND_PORT` | 3000 | |
| `JWT_SECRET` | (random) | Wajib diganti di production |
| `JWT_EXPIRE_MINUTES` | 60 | |
| `CORS_ORIGINS` | localhost:3000 | Comma-separated |
| `OUTPUT_TTL_HOURS` | 24 | TTL file di `storage/outputs/` |
| `SWEEP_INTERVAL_MINUTES` | 15 | Frekuensi worker sweep |
| `LOG_LEVEL` | INFO | Worker log level |

## Menambah tool baru

1. **Backend** — bikin business logic di `backend/app/services/<kategori>.py`,
   lalu router di `backend/app/api/tools/<kategori>.py`. Daftarkan di
   `backend/app/api/tools/__init__.py`:
   ```python
   router.include_router(image_router, prefix="/image", tags=["Tools: Image"])
   ```
   Auth otomatis berlaku karena dipasang di aggregator `/api/tools`.

2. **Frontend** — bikin route `frontend/src/routes/tools/<kategori>/<slug>/+page.svelte`
   pakai `ToolShell` + `Dropzone` untuk konsistensi UI.

3. **Worker** (opsional) — kalau perlu scheduled job, bikin
   `worker/tasks/<job>.py` dengan function `run()` dan daftarkan di `worker/main.py`.

## Catatan WSL2

Kalau pakai WSL2 dan `localhost:3000` dari browser Windows timeout, kemungkinan
networking mode-nya bukan mirrored. Fix di `C:\Users\<user>\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
```

Lalu `wsl --shutdown` di PowerShell, buka WSL lagi, dan `docker compose up -d`.
Workaround sementara: pakai IP WSL (`hostname -I`) di browser.

## Catatan keamanan

- `JWT_SECRET` di `.env.example` adalah placeholder — generate ulang untuk production.
- Tidak ada endpoint registrasi publik. User dibuat lewat CLI backend.
- `storage/outputs/` di-sweep otomatis oleh worker. Avatars tidak pernah dihapus.

## Lisensi

Belum ditentukan.
