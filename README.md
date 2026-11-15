# TokenDex

A cartoon-style Hugging Face model explorer and local hardware planner. Browse popular models, compare approximate memory and speed, and inspect model lineage and descriptions.

## Serving structure

```text
.
├── app.py                      # Flask: serves the app and health checks
├── static/index.html           # Complete frontend, styles, and browser logic
├── requirements.txt            # Flask and Gunicorn
├── start-render.sh             # Production server entry point
├── Dockerfile                  # Python container, running as a non-root user
├── render.yaml                 # Render Docker Blueprint
├── compose.yaml                # Local Docker setup
├── .env.example                # Optional local port settings
└── scripts/build-site-static.py # Optional export for the original hosted Site
```

There is no Caddy or Nginx configuration. Docker and Render both run `start-render.sh`, which starts Gunicorn serving `app:app`. Flask serves `static/index.html` at `/`, static assets under `/static/`, and `ok` at `/healthz`. There is no separate frontend development server or frontend build step.

## Run with Docker

```sh
docker compose up --build
```

Open <http://localhost:8080>. Test health:

```sh
curl --fail http://localhost:8080/healthz
```

Stop with `docker compose down`. Optional local port overrides are in `.env.example`; copy it to `.env` if needed.

Without Compose:

```sh
docker build -t tokendex .
docker run --rm -p 8080:10000 tokendex
```

## Run with Python

On macOS or Linux:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
sh start-render.sh
```

Open <http://localhost:10000>. `PORT` defaults to `10000`; `WEB_CONCURRENCY` defaults to 2 workers and `GUNICORN_THREADS` to 4 threads. Gunicorn's production server is used by the startup script. On Windows, use Docker or WSL for Gunicorn.

## Deploy to Render

1. Push this repository to GitHub, GitLab, or Bitbucket. Keep `static/index.html` tracked.
2. In Render, select **New → Blueprint** and connect your repository.
3. Render reads `render.yaml`, builds the root `Dockerfile`, and creates the `tokendex` Docker web service.
4. Review the plan and apply the Blueprint. The configuration requests the Free plan, subject to account limits and availability.
5. Open the Render URL and verify `/healthz` returns `ok`.

For a manually created Render Web Service, select **Docker**, repository root as Root Directory, `./Dockerfile` as Dockerfile Path, and `/healthz` as Health Check Path. Leave Docker Command empty: the Dockerfile runs `sh ./start-render.sh`. Do not set a separate frontend start command.

The server listens on `0.0.0.0:$PORT`, defaulting to `10000`. Render handles public HTTPS. No persistent disk, database, Hugging Face token, or second service is required.

## Browser behavior

Hardware detection runs in the visitor’s browser. WebGPU and WebGL can expose an adapter name. Phones, managed browsers and insecure origins may expose only the platform or approximate system RAM. On Apple M chips, available browser RAM seeds a provisional memory budget. Other devices show approximate system RAM separately from GPU memory. Recognized presets label nominal bandwidth as an estimate. For example, Apple lists [200 GB/s for M2 Pro](https://www.apple.com/uk/business/docs/site/Whats_New_for_Business.pdf). Missing fields accept manual input, and scanning again preserves edits made on the page.

The browser calls public Hugging Face APIs directly for popular models, search, configurations, metadata, and descriptions. Those requests depend on the visitor's network, provider access controls, CORS policies, and rate limits. A starter collection remains usable if the live catalog is unavailable. All panels and controls use the bundled Space Grotesk variable font. Its SIL Open Font License is included under `static/fonts/`. The device scan runs automatically on page load and shows the browser-reported logical processor count when available.

Speed predictions are heuristics, not measured benchmarks. Mixture-of-experts models receive rough full-weight memory estimates but no invented speed or bandwidth targets. Model context limit comes from the model configuration; the context dropdown selects the workload being estimated. Check the model's original license and documentation before use.

## Editing

Edit the canonical frontend at `static/index.html`. Python serving logic is in `app.py`. Changes require a redeploy or a local Docker rebuild.

The original hosted Site additionally uses `.openai/hosting.json` and a generated `dist/` static export. These are not required for Render, and `dist/` is ignored by Git. To refresh that export, run `python scripts/build-site-static.py`.

The Docker build context includes only Python server files, requirements, and `static/`. Git internals, deployment metadata, and local environment files are excluded. No extra visitor authentication is configured; private access rules from the original ChatGPT Site do not transfer to a separate Render deployment.

## Validation

Flask route checks and an actual `start-render.sh` / Gunicorn startup passed, including health checks, static assets, HEAD requests, no-cache HTML, private-path protection, and custom PORT binding on all interfaces. Docker is not installed in the preparation environment, so the final image build must be verified with the Docker commands above.

References: [Flask with Gunicorn](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/), [Render Docker](https://render.com/docs/docker), [Render Blueprints](https://render.com/docs/blueprint-spec).
