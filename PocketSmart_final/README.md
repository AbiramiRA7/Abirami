# PocketSmart AI

A complete FastAPI + Jinja2 budget recommendation assistant implementing the project documentation's Home, Party and Jewelry planners, authentication, sessions, recommendation history, Gemini integration, optional jewelry image input, marketplace search links, and fallback recommendations.

## Structure

- `app/models/` — domain dataclasses and Pydantic request/response schemas.
- `app/routes/` — page, authentication, planner, recommendation and session endpoints.
- `app/services/` — Gemini, recommendation orchestration, marketplace links, fallback engine and auth service.
- `app/utils/` — prompts, validation, security and helpers.
- `app/templates/` — Jinja2 pages and planner/recommendation templates.
- `app/static/` — CSS, JavaScript and SVG assets.
- `tests/` — automated API tests.

## Run in VS Code

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows cmd
# or: cp .env.example .env
python run.py
```

Open `http://127.0.0.1:8000` and API docs at `http://127.0.0.1:8000/docs`.

## Gemini

Set `GEMINI_API_KEY` in `.env`. The model is configurable with `GEMINI_MODEL`. If no key is supplied, the application uses its local fallback engine so the complete UI and API remain usable.

## Tests

```bash
pytest -q
```

## Notes

Marketplace URLs are search links. They do not represent live inventory or exact current pricing. The Gemini prompt also instructs the model not to claim live marketplace data. The application follows the documentation's mock/simulated marketplace and fallback approach.
