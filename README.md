# Bestway — "Can I Afford This?" Budget Snapshot Tool

An interactive web app that helps customers understand what Bestway products fit their budget, with **AI-powered insights and chat** via Claude.

## Features

| Feature | Details |
|---|---|
| **Live budget calculator** | Income, tax, expense inputs update results instantly |
| **Budget donut chart** | Visual Plotly breakdown |
| **Safe payment range** | Personalized `$X–$Y /wk` hero result |
| **12-product grid** | Color-coded ✅ Fits / ⚠️ Stretch / gray Over Budget |
| **✨ AI Budget Insight** | One-click Claude-generated personalized analysis |
| **💬 AI Chat (Alex)** | Streaming chat advisor with full budget context |
| **Bestway brand UI** | Purple #4a298e, yellow #feef02, Roboto font |

---

## Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and paste your key
```

Or use an environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Run
```bash
streamlit run app.py
```

---

## Deploy to Streamlit Community Cloud

1. Push this repo to **GitHub** (public or connected private)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select repo → branch `main` → file `app.py` → **Deploy**
4. In **App settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Save and reboot the app — live in ~2 minutes

> **Important:** Never commit `.streamlit/secrets.toml` — it's in `.gitignore`.

---

## AI Features

Both AI features are powered by **Claude Opus 4.6** via the Anthropic API and use **streaming** so responses appear word-by-word.

### ✨ AI Budget Insight
Click **Generate Insight** after entering your budget. Claude analyzes your full financial picture and returns a 3–4 sentence personalized summary with:
- A specific product recommendation and why it fits
- One actionable tip to reach a stretch goal

### 💬 Chat with Alex (AI Advisor)
Ask follow-up questions in natural language. The advisor (Alex) knows your complete budget snapshot and can answer questions like:
- "Which product is the best value for me?"
- "What if I cut my grocery bill by $50/month?"
- "How long until I own the 65" TV outright?"

---

## Project Structure

```
budget-tool/
├── app.py                        # Full Streamlit application
├── requirements.txt              # Python dependencies
├── .gitignore                    # Excludes secrets.toml
├── .streamlit/
│   ├── config.toml               # Theme & server config
│   └── secrets.toml.example      # API key template
└── README.md
```

## Brand Reference

| Token          | Value     |
|----------------|-----------|
| Primary Purple | `#4a298e` |
| Dark Purple    | `#351d65` |
| Bestway Yellow | `#feef02` |
| Body Text      | `#343546` |
| Light BG       | `#f6f6f6` |
| Font           | Roboto    |
