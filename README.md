# NexAgriTech — Multilingual Agritech MVP

NexAgriTech connects farmer tools, organic-first guidance, direct produce sales, nutrition information, educational content and market insights. The repository follows the requested `frontend/` and `backend/` layout. The current implementation is a runnable MVP with a Next.js/React/TypeScript UI, FastAPI JSON API and SQLite persistence.

## Start locally

Requires Python 3.10+ and Node.js 20+.

**Backend** (from the repository root):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

**Frontend** (in another terminal):

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. Swagger API docs are at `http://127.0.0.1:8000/docs`. SQLite creates `farmveda.db` in the repository root and seeds a sample Guntur farm on first startup. Use `NEXAGRITECH_DB` to choose another database path (`FARMVEDA_DB` remains as a legacy fallback). Docker users can run `docker compose up --build`.

## MVP workflows

- Farmer profile, crop records, growth stage and farm tasks.
- Product listings and inventory; editable price and quantity.
- Customer marketplace with product details, farmer/location, harvest/practices, generic nutrition per 100 g, basket, checkout, and reviews.
- Customer registration and sign-in with salted password hashes, expiring bearer sessions, account view, and per-customer online order history.
- Authenticated demo checkout; farm-gate offline sales remain available from the farmer workspace.
- Online demo orders and farm-gate offline sales both update inventory and appear in sales analytics.
- Cost-based suggested price: `(entered costs + desired profit) / saleable quantity`, compared with a separately labeled market observation.
- Organic-first advisory templates in English, Telugu and Hindi; advice is saved in SQLite.
- Advisor attachment picker supports camera capture and image/video upload (up to five files, 20 MB each); files are stored locally with prompt/language metadata.
- Recipe and crop-growing lesson narration/storyboards in English, Telugu and Hindi. Browser speech synthesis can read scripts, and supported browsers can render/download a simple WebM slide-storyboard locally.
- Market and revenue dashboard with sample market observations.

## Demo data and service boundaries

The initial farmer, listings, nutrition estimates, and Guntur market prices are illustrative seed data. Prices are not live AGMARKNET/eNAM observations, nutrition is generic and not lab-tested, and farmer-declared growing practices are not verified organic certification. Customer accounts use salted password hashes and bearer tokens for the MVP, but farmer accounts/tenant isolation, hardened production session controls, rate limiting and security monitoring are not implemented. Checkout stores demo orders and does not collect money or book delivery. Weather and soil routes return provider/setup guidance. Advisory uses local templates, not an external LLM. Uploaded crop photos/videos are stored locally but not analyzed; crop diagnosis needs a validated model. Payment provider, delivery partner, speech-to-text, certification document checks, and AI-generated farm imagery need production integrations and credentials. Browser-rendered storyboard videos contain text scenes; speech is played separately by browser TTS. Educational advice/content must be checked with local agricultural experts.

Before deployment with real users, add authentication and authorization, rate/input limits, privacy and retention controls, backups, secure payments, licensed market data, agriculture-source review, and operational monitoring. Do not expose this demo as a production commerce service without those controls.
