# Studymon Family — Railway preparation

**DRAFT: not safe to make public yet.** Missing generated data, first-run security onboarding and backups must be resolved before deployment.

## Architecture
One PWA starts at `/family` with parent and kid options. Original `/parent` and `/` pages remain, reusing their existing APIs. FastAPI runs inside a Railway Docker service, with SQLite on one persistent volume. Use one service replica.

## Railway settings (do not deploy yet)
- Attach a persistent volume mounted at `/data`.
- Set `PKM_SQLITE_FILE=/data/pkm.sqlite3`.
- Set `PKM_JWT_SECRET` to a unique random string with at least 32 characters.
- Set `PKM_PARENT_PASSWORD` to a unique password with at least 12 characters. It is applied ONLY when initializing a new database.
- Dockerfile is at repository root. PORT is automatically supplied by Railway.

The startup script requires `assets/out/00_schema.sql`, which the upstream repository does NOT include. Read `ASSETS_GUIDE.md` and generate the game data before trying to start. Do not publish unlicensed Pokemon assets. The first-run student PIN and placeholder parent identifier from upstream still need redesign; the app must not be made public before that work.

Startup initializes the database only when missing and preserves an existing database; do NOT run the upstream reset scripts on real family data. Take regular private backups of `/data/pkm.sqlite3` (including its WAL state through a proper SQLite backup procedure). Do not use multiple replicas.

## Remaining launch blockers
- Finish build assets/data pipeline with clear third-party licensing treatment.
- Secure parent and kid first-run provisioning, eliminate default PIN and placeholder accounts, rate-limit login attempts.
- Review device-token auth, frontend token handling, API authorization and PWA behaviors.
- Test first boot, role logins, tasks, battle flows and persistence after restart on disposable database.
- Backups and recovery drill; HTTPS and domain test on Railway.

Never merge or deploy this draft solely on the basis of static file checks.
