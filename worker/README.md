# Worker

Lightweight maintenance worker untuk tools-service. Stdlib-only Python,
tidak butuh dependency eksternal.

## Tugas saat ini

- **`cleanup-outputs`** — sweep file di `/storage/outputs/` yang lebih tua dari `OUTPUT_TTL_HOURS`. Tidak menyentuh `avatars/` atau `uploads/`.

## Env

| Variable | Default | Keterangan |
|---|---|---|
| `STORAGE_DIR` | `/storage` | Root volume bersama dengan backend |
| `OUTPUT_DIR_NAME` | `outputs` | Subfolder yang akan disapu |
| `OUTPUT_TTL_HOURS` | `24` | File lebih tua dari ini akan dihapus |
| `SWEEP_INTERVAL_MINUTES` | `15` | Frekuensi sweep |
| `LOG_LEVEL` | `INFO` | DEBUG \| INFO \| WARNING \| ERROR |

## Run langsung (dev)

```bash
cd worker
STORAGE_DIR=../storage OUTPUT_TTL_HOURS=1 SWEEP_INTERVAL_MINUTES=1 \
  python -m worker.main
```

## Menambah job baru

1. Bikin `worker/tasks/<job>.py` dengan function `run()`.
2. Daftarkan di `worker/main.py`:

   ```python
   jobs = [
       Job("cleanup-outputs", cleanup.run, sweep_interval_min * 60),
       Job("my-job", my_job.run, 60 * 60),  # tiap 1 jam
   ]
   ```

## Build & jalankan via compose

Dijalankan otomatis saat `docker compose up` dari root `tools-service/`.

```bash
docker compose up -d worker
docker compose logs -f worker
```
