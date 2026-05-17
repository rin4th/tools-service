# Tools Service Backend

FastAPI backend untuk web tools (PDF, dll) dengan auth (JWT) dan profile sederhana.

Struktur dirancang supaya gampang ditambah tools baru: setiap kategori tool jadi router terpisah di bawah `/api/tools/`.

## Setup

1. Salin env:

   ```bash
   cp .env.example .env
   ```

   Lalu ubah `JWT_SECRET` jadi nilai acak yang panjang.

2. Jalankan Postgres (dari folder root `tools-service/`):

   ```bash
   docker compose up -d postgres
   ```

3. Install dependency dan jalankan API:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

4. Buat user pertama:

   ```bash
   python -m app.cli create-user admin password123
   ```

API berjalan di `http://127.0.0.1:8000` dan dokumentasi otomatis di `/docs`.

## Struktur project

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py            # /api/auth/*
│   │   ├── profile.py         # /api/profile/*
│   │   └── tools/             # /api/tools/*
│   │       ├── __init__.py    # aggregator router
│   │       └── pdf.py         # /api/tools/pdf/*
│   ├── services/              # business logic, reusable
│   │   ├── pdf.py
│   │   └── uploads.py
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── security.py
├── .env.example
└── requirements.txt
```

## Endpoints

Auth:
- `POST /api/auth/login` — body `{ "username": "...", "password": "..." }` mengembalikan JWT.

Profile (butuh `Authorization: Bearer <token>`):
- `GET /api/profile/me`
- `POST /api/profile/avatar` (multipart `file`)
- `GET /api/profile/avatar/{user_id}`
- `POST /api/profile/change-password` body `{ "current_password": "...", "new_password": "..." }`

Tools (semua butuh `Authorization: Bearer <token>`) — PDF:
- `POST /api/tools/pdf/merge`
- `POST /api/tools/pdf/split`
- `POST /api/tools/pdf/image-to-pdf`

## Menambah tool baru

Contoh nambah kategori `image` (resize, convert, dll):

1. Bikin `app/services/image.py` — taruh business logic murni di sini (tidak menyentuh FastAPI).
2. Bikin `app/api/tools/image.py` — router yang panggil service.
3. Daftarkan di `app/api/tools/__init__.py`:

   ```python
   from app.api.tools.image import router as image_router
   router.include_router(image_router, prefix="/image", tags=["Tools: Image"])
   ```

Endpoint baru otomatis muncul di `/api/tools/image/*`.

## Catatan

- Database dibuat otomatis saat startup melalui `Base.metadata.create_all`.
- Avatar disimpan di `tools-service/storage/avatars`.
- File output PDF di `tools-service/storage/outputs`.
- File output belum dibersihkan otomatis. Akan ditambah TTL/cleanup terjadwal di iterasi berikutnya.
