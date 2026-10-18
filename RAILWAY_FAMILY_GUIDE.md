# Studymon Family — Railway preparation

**DRAFT: not safe to make public yet.** Missing generated data, first-run security onboarding and backups must be resolved before deployment.

## Architecture
One PWA starts at `/family` with parent and kid options. Original `/parent` and `/` pages remain, reusing their existing APIs. FastAPI runs inside a Railway Docker service, with SQLite on one persistent volume. Use one service replica.

## Railway settings (do not deploy yet)
- Attach a persistent volume mounted at `/data`.
- Set `PKM_SQLITE_FILE=/data/pkm.sqlite3`.
- Set `PKM_JWT_SECRET` to a unique random string with at least 32 characters.
- Set `PKM_PARENT_ID` to a private parent login identifier (not the upstream default).
- Set `PKM_CHILD_PIN` to a unique 4–8 digit PIN (not 1234/0000/1111).
- Set `PKM_PARENT_PASSWORD` to a unique password with at least 12 characters. It is applied ONLY when initializing a new database.
- Dockerfile is at repository root. PORT is automatically supplied by Railway.

The startup script requires `assets/out/00_schema.sql`, which the upstream repository does NOT include. Read `ASSETS_GUIDE.md` and generate the game data before trying to start. Do not publish unlicensed Pokemon assets. Cloud first-run parent identifier and child PIN now require explicit private environment variables. Login rate limiting, end-to-end security audit, game-data generation, and backup recovery tests are still required before public release.

Startup initializes the database only when missing and preserves an existing database; do NOT run the upstream reset scripts on real family data. Take regular private backups of `/data/pkm.sqlite3` (including its WAL state through a proper SQLite backup procedure). Do not use multiple replicas.

## Verified source-code blocker
The current fork does **not** contain `assets/build_import.py` referenced by `ASSETS_GUIDE.md`. The repository's `assets/` directory contains only `README.md`. A legitimate replacement data generator or externally provided generated SQL files are required before initial deployment. Do not assume the original setup guide can run as written.

## Remaining launch blockers
- Finish build assets/data pipeline with clear third-party licensing treatment.
- Secure parent and kid first-run provisioning, eliminate default PIN and placeholder accounts, rate-limit login attempts.
- Review device-token auth, frontend token handling, API authorization and PWA behaviors.
- Test first boot, role logins, tasks, battle flows and persistence after restart on disposable database.
- Backups and recovery drill; HTTPS and domain test on Railway.

Never merge or deploy this draft solely on the basis of static file checks.
