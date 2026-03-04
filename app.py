import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import anthropic
import os
import re

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Can I Afford This? | Bestway",
    page_icon="💛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Brand CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

.stApp { background-color: #f6f6f6; }

/* ── Header ── */
.bw-header {
    background: linear-gradient(135deg, #351d65 0%, #4a298e 100%);
    padding: 28px 40px 24px;
    border-radius: 0 0 24px 24px;
    margin-bottom: 32px;
    box-shadow: 0 6px 24px rgba(74,41,142,0.25);
    display: flex;
    align-items: center;
    gap: 20px;
}
.bw-header-text h1 {
    color: #feef02;
    font-size: 2.1em;
    font-weight: 900;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
}
.bw-header-text p {
    color: rgba(255,255,255,0.82);
    font-size: 1.05em;
    margin: 0;
}
.bw-logo-badge {
    background: #feef02;
    color: #351d65;
    font-weight: 900;
    font-size: 1.1em;
    padding: 10px 18px;
    border-radius: 12px;
    letter-spacing: 1px;
    white-space: nowrap;
}

/* ── Section cards ── */
.bw-card {
    background: white;
    border-radius: 14px;
    padding: 26px 28px;
    box-shadow: 0 2px 14px rgba(0,0,0,0.07);
    margin-bottom: 20px;
}
.bw-card-title {
    color: #351d65;
    font-size: 1.1em;
    font-weight: 700;
    border-left: 4px solid #feef02;
    padding-left: 12px;
    margin-bottom: 20px;
}

/* ── Result hero ── */
.bw-result-hero {
    background: linear-gradient(135deg, #4a298e 0%, #351d65 100%);
    border-radius: 16px;
    padding: 30px 24px;
    text-align: center;
    color: white;
    box-shadow: 0 6px 24px rgba(74,41,142,0.35);
}
.bw-result-hero .label { font-size: 0.95em; opacity: 0.8; margin-bottom: 6px; }
.bw-result-hero .range {
    color: #feef02;
    font-size: 2.6em;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 6px;
}
.bw-result-hero .sublabel { font-size: 0.85em; opacity: 0.7; }

/* ── Score badge ── */
.score-row { display: flex; gap: 12px; margin-bottom: 16px; }
.score-pill {
    flex: 1;
    border-radius: 10px;
    padding: 14px 10px;
    text-align: center;
    font-weight: 700;
}
.score-pill .sp-val { font-size: 1.5em; }
.score-pill .sp-lbl { font-size: 0.75em; margin-top: 2px; opacity: 0.85; }
.sp-green  { background: #dcfce7; color: #166534; }
.sp-yellow { background: #fef9c3; color: #713f12; }
.sp-purple { background: #ede9fe; color: #4a298e; }

/* ── Tip box ── */
.bw-tip {
    background: #eef2ff;
    border-left: 4px solid #4a298e;
    border-radius: 8px;
    padding: 12px 16px;
    color: #343546;
    font-size: 0.88em;
    margin-top: 8px;
}
.bw-tip b { color: #4a298e; }

/* ── AI Insight box ── */
.ai-insight {
    background: linear-gradient(135deg, #f5f3ff 0%, #eef2ff 100%);
    border-left: 4px solid #4a298e;
    border-radius: 10px;
    padding: 16px 20px;
    color: #343546;
    font-size: 0.97em;
    line-height: 1.75;
    margin-top: 10px;
}

/* ── Product cards ── */
.prod-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.prod-card {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-top: 5px solid #e9eef4;
    text-align: center;
    transition: transform 0.15s;
}
.prod-card:hover { transform: translateY(-3px); box-shadow: 0 6px 18px rgba(0,0,0,0.12); }
.prod-card.can-afford { border-top-color: #22c55e; }
.prod-card.stretch    { border-top-color: #f59e0b; }
.prod-card.out        { border-top-color: #e5e7eb; opacity: 0.55; }
.prod-card .prod-icon { font-size: 2.2em; margin-bottom: 8px; }
.prod-card .prod-name { font-weight: 700; color: #351d65; font-size: 0.92em; margin-bottom: 4px; }
.prod-card .prod-price { color: #4a298e; font-size: 1.3em; font-weight: 900; }
.prod-card .prod-week  { font-size: 0.72em; color: #767676; }
.prod-card .prod-term  { font-size: 0.75em; color: #767676; margin-top: 4px; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7em;
    font-weight: 700;
    margin-top: 6px;
}
.badge-green  { background: #22c55e; color: white; }
.badge-yellow { background: #f59e0b; color: white; }
.badge-gray   { background: #e5e7eb; color: #6b7280; }

/* ── Streamlit widget overrides ── */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stRadio"] label {
    color: #351d65 !important;
    font-weight: 600 !important;
    font-size: 0.92em !important;
}
.stButton > button {
    background-color: #feef02 !important;
    color: #351d65 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 25px !important;
    font-size: 1em !important;
    width: 100%;
    padding: 12px !important;
    letter-spacing: 0.3px;
}
.stButton > button:hover {
    background-color: #e8d900 !important;
    box-shadow: 0 4px 12px rgba(254,239,2,0.4) !important;
}
.stProgress > div > div { background-color: #4a298e !important; }

/* ── Chat message overrides ── */
[data-testid="stChatMessage"] {
    background: white;
    border-radius: 10px;
    margin-bottom: 8px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}

/* ── Suggestion chips ── */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: #ede9fe !important;
    color: #4a298e !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 20px !important;
    font-size: 0.82em !important;
    padding: 6px 14px !important;
    font-weight: 500 !important;
}

/* ── Footer ── */
.bw-footer {
    background: #351d65;
    color: rgba(255,255,255,0.65);
    text-align: center;
    padding: 18px;
    border-radius: 14px;
    margin-top: 40px;
    font-size: 0.8em;
    line-height: 1.7;
}
.bw-footer a { color: #feef02; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ─── Anthropic Client ────────────────────────────────────────────────────────────
def get_client():
    """Return an Anthropic client using Streamlit secrets or env var."""
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
    except Exception:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    return anthropic.Anthropic(api_key=key)

AI_SYSTEM = """You are Alex, a warm and knowledgeable budget advisor at Bestway, a rent-to-own store. Your role is to help customers understand their finances and feel genuinely confident about their purchasing decisions.

Guidelines:
- Be encouraging and empathetic — never judgmental about budget size
- Always reference specific dollar amounts from their budget snapshot
- Keep responses concise (2–4 sentences) unless the customer asks for more detail
- When recommending products, explain specifically WHY they fit this customer's situation
- Suggest practical, achievable ways to reach stretch goals
- Use simple, friendly language — no financial jargon
- If asked about ownership timelines, use: weeks to own = term in weekly payments shown"""

# ─── Product Catalog ────────────────────────────────────────────────────────────
PRODUCTS = [
    {"icon": "📺", "name": '75" 4K Smart TV',        "weekly": 34.99, "term": 78, "category": "Electronics"},
    {"icon": "📺", "name": '65" 4K Smart TV',        "weekly": 24.99, "term": 78, "category": "Electronics"},
    {"icon": "📺", "name": '55" Smart TV',            "weekly": 18.99, "term": 78, "category": "Electronics"},
    {"icon": "🛏️", "name": "Queen Bedroom Set",       "weekly": 29.99, "term": 96, "category": "Furniture"},
    {"icon": "🛋️", "name": "Living Room Set",         "weekly": 34.99, "term": 96, "category": "Furniture"},
    {"icon": "🛋️", "name": "Recliner Sofa",           "weekly": 16.99, "term": 78, "category": "Furniture"},
    {"icon": "🍽️", "name": "Dining Room Set",         "weekly": 19.99, "term": 78, "category": "Furniture"},
    {"icon": "🧺", "name": "Washer & Dryer Set",      "weekly": 24.99, "term": 96, "category": "Appliances"},
    {"icon": "❄️", "name": "French Door Refrigerator","weekly": 21.99, "term": 96, "category": "Appliances"},
    {"icon": "❄️", "name": "Top-Load Refrigerator",  "weekly": 14.99, "term": 78, "category": "Appliances"},
    {"icon": "💻", "name": 'Laptop (15")',            "weekly": 14.99, "term": 78, "category": "Electronics"},
    {"icon": "🎮", "name": "Gaming Console Bundle",   "weekly": 12.99, "term": 78, "category": "Electronics"},
]

# ─── Helpers ────────────────────────────────────────────────────────────────────
def to_html_content(text):
    """Safely convert AI text to HTML — prevents Streamlit from treating
    dollar amounts like $18.99 as LaTeX $...$ expressions."""
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = text.replace('$', '&#36;')                          # block LaTeX
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)  # bold
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',          text)  # italic
    text = text.replace('\n', '<br>')
    return text

def stream_chat_response(client, messages, budget_context):
    """Stream an AI reply to the last user message and append it to history."""
    api_messages = []
    for i, m in enumerate(messages):
        if i == 0 and m["role"] == "user":
            api_messages.append({
                "role": "user",
                "content": f"My current budget snapshot:\n\n{budget_context}\n\n---\n\nMy question: {m['content']}",
            })
        else:
            api_messages.append(m)

    with st.chat_message("assistant", avatar="🤖"):
        def gen():
            with client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=450,
                system=AI_SYSTEM,
                messages=api_messages,
            ) as stream:
                for chunk in stream.text_stream:
                    yield chunk
        full_response = st.write_stream(gen())
    st.session_state.chat_messages.append({"role": "assistant", "content": full_response})

# ─── Session State ───────────────────────────────────────────────────────────────
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "ai_insight" not in st.session_state:
    st.session_state.ai_insight = None
if "pending_response" not in st.session_state:
    st.session_state.pending_response = False

# ─── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bw-header">
  <div class="bw-logo-badge">BESTWAY</div>
  <div class="bw-header-text">
    <h1>Can I Afford This?</h1>
    <p>Enter your income &amp; expenses — we'll show you exactly what fits your budget.</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Layout ─────────────────────────────────────────────────────────────────────
left, right = st.columns([1.05, 1], gap="large")

# ════════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Inputs
# ════════════════════════════════════════════════════════════════════════════════
with left:

    # ── Income ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="bw-card"><div class="bw-card-title">💰 My Income</div>', unsafe_allow_html=True)

    pay_freq = st.selectbox(
        "How often do you get paid?",
        ["Weekly", "Bi-Weekly (every 2 weeks)", "Semi-Monthly (twice/month)", "Monthly"],
        key="pay_freq",
    )
    gross_income = st.number_input(
        "Gross income per pay period ($)",
        min_value=0, max_value=20_000, value=1_500, step=50,
        help="Before taxes. Enter what appears on your paycheck.",
    )
    tax_rate = st.slider(
        "Estimated tax rate (%)",
        min_value=0, max_value=40, value=22,
        help="Federal + state taxes. 22% is a common effective rate.",
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Monthly Expenses ─────────────────────────────────────────────────────────
    st.markdown('<div class="bw-card"><div class="bw-card-title">🏠 My Monthly Expenses</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        rent      = st.number_input("Rent / Mortgage ($)",  0, 10_000, 900,  50)
        utilities = st.number_input("Utilities ($)",         0,  2_000, 150,  25)
        groceries = st.number_input("Groceries ($)",         0,  2_000, 350,  25)
    with col_b:
        transport = st.number_input("Transportation ($)",    0,  2_000, 250,  25)
        insurance = st.number_input("Insurance ($)",         0,  2_000, 175,  25)
        other_exp = st.number_input("Other expenses ($)",    0,  5_000, 200,  50)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Existing Payments ────────────────────────────────────────────────────────
    st.markdown('<div class="bw-card"><div class="bw-card-title">📋 Existing Payments</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns(2)
    with col_c:
        existing_rto  = st.number_input("Current RTO payments ($/wk)", 0, 500, 0, 5)
    with col_d:
        existing_debt = st.number_input("Other debt payments ($/wk)",  0, 500, 0, 5)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Preferences ─────────────────────────────────────────────────────────────
    st.markdown('<div class="bw-card"><div class="bw-card-title">⚙️ My Preferences</div>', unsafe_allow_html=True)
    comfort = st.select_slider(
        "How comfortable are you stretching your budget?",
        options=["Very Conservative", "Conservative", "Moderate", "Flexible", "Very Flexible"],
        value="Moderate",
    )
    pref_category = st.multiselect(
        "Show me products from (leave blank for all)",
        ["Electronics", "Furniture", "Appliances"],
        default=[],
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Results
# ════════════════════════════════════════════════════════════════════════════════
with right:

    # ── Compute ─────────────────────────────────────────────────────────────────
    FREQ_TO_MONTHLY = {
        "Weekly": 52 / 12,
        "Bi-Weekly (every 2 weeks)": 26 / 12,
        "Semi-Monthly (twice/month)": 2.0,
        "Monthly": 1.0,
    }
    multiplier       = FREQ_TO_MONTHLY[pay_freq]
    net_per_period   = gross_income * (1 - tax_rate / 100)
    monthly_net      = net_per_period * multiplier

    monthly_expenses = rent + utilities + groceries + transport + insurance + other_exp
    existing_weekly  = existing_rto + existing_debt
    existing_monthly = existing_weekly * (52 / 12)

    disposable_monthly = monthly_net - monthly_expenses - existing_monthly
    disposable_weekly  = disposable_monthly / (52 / 12)

    comfort_map = {
        "Very Conservative": (0.10, 0.15),
        "Conservative":      (0.12, 0.18),
        "Moderate":          (0.15, 0.22),
        "Flexible":          (0.18, 0.27),
        "Very Flexible":     (0.22, 0.32),
    }
    lo_ratio, hi_ratio = comfort_map[comfort]
    safe_lo = max(0, disposable_weekly * lo_ratio)
    safe_hi = max(0, disposable_weekly * hi_ratio)

    expense_ratio = (monthly_expenses + existing_monthly) / monthly_net if monthly_net > 0 else 1

    # ── Result Hero ─────────────────────────────────────────────────────────────
    if disposable_weekly > 0:
        st.markdown(f"""
        <div class="bw-result-hero">
            <div class="label">Your estimated safe weekly payment range</div>
            <div class="range">${safe_lo:.2f} – ${safe_hi:.2f}</div>
            <div class="sublabel">per week &nbsp;·&nbsp; based on your {comfort.lower()} comfort level</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="bw-result-hero" style="border: 2px solid #f59e0b;">
            <div class="range" style="font-size:1.6em;">⚠️ Budget Tight</div>
            <div class="sublabel" style="opacity:1; color:#fde68a;">
                Your expenses exceed your take-home pay.<br>Try adjusting your numbers.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Score Pills ──────────────────────────────────────────────────────────────
    expense_pct  = min(100, round(expense_ratio * 100))
    leftover_pct = max(0, 100 - expense_pct)
    disp_label   = "✅ Healthy" if leftover_pct >= 25 else ("⚠️ Tight" if leftover_pct >= 10 else "🔴 Critical")

    st.markdown(f"""
    <div class="score-row">
        <div class="score-pill sp-purple">
            <div class="sp-val">${monthly_net:,.0f}</div>
            <div class="sp-lbl">Monthly Take-Home</div>
        </div>
        <div class="score-pill sp-yellow">
            <div class="sp-val">${monthly_expenses + existing_monthly:,.0f}</div>
            <div class="sp-lbl">Monthly Committed</div>
        </div>
        <div class="score-pill {'sp-green' if leftover_pct >= 25 else 'sp-yellow'}">
            <div class="sp-val">{leftover_pct}%</div>
            <div class="sp-lbl">Disposable&nbsp;{disp_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Budget Donut ─────────────────────────────────────────────────────────────
    labels = ["Rent/Mortgage", "Utilities", "Groceries", "Transport", "Insurance", "Other", "Existing Payments", "Disposable"]
    values = [rent, utilities, groceries, transport, insurance, other_exp,
              existing_monthly, max(0, disposable_monthly)]
    colors = ["#4a298e", "#6b46c1", "#7c3aed", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ddd6fe", "#feef02"]

    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.55,
        marker_colors=colors, textinfo="percent",
        hovertemplate="<b>%{label}</b><br>$%{value:,.2f}/mo<extra></extra>",
        textfont=dict(size=11),
    ))
    fig.add_annotation(
        text=f"${monthly_net:,.0f}<br><span style='font-size:10px'>Monthly Net</span>",
        x=0.5, y=0.5, font_size=16, showarrow=False,
        font=dict(color="#351d65", family="Roboto"),
    )
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10), height=280,
        showlegend=False, paper_bgcolor="white", plot_bgcolor="white",
    )
    st.markdown('<div class="bw-card"><div class="bw-card-title">📊 Budget Breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Smart Tip ────────────────────────────────────────────────────────────────
    if expense_ratio > 0.85:
        tip = "<b>Heads up:</b> Your committed expenses are over 85% of take-home. Consider reducing discretionary costs before adding a new payment."
    elif expense_ratio > 0.70:
        tip = "<b>Good news:</b> You have some breathing room. Staying at the lower end of your payment range gives you a safety cushion."
    else:
        tip = "<b>Looking great!</b> You have strong disposable income — you can comfortably explore more options, or pay ahead to own sooner."

    st.markdown(f'<div class="bw-tip">💡 {tip}</div>', unsafe_allow_html=True)

# ─── Product Recommendations ─────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="bw-card"><div class="bw-card-title">🛍️ Products That Fit Your Budget</div>', unsafe_allow_html=True)

filtered = PRODUCTS if not pref_category else [p for p in PRODUCTS if p["category"] in pref_category]

cards_html = '<div class="prod-grid">'
for p in filtered:
    w       = p["weekly"]
    can     = w <= safe_hi
    stretch = (not can) and (w <= safe_hi * 1.4)
    css_cls = "can-afford" if can else ("stretch" if stretch else "out")
    badge   = ('<span class="badge badge-green">✓ Fits Budget</span>' if can
               else '<span class="badge badge-yellow">Stretch</span>' if stretch
               else '<span class="badge badge-gray">Over Budget</span>')
    total   = w * p["term"]
    cards_html += f"""
    <div class="prod-card {css_cls}">
        <div class="prod-icon">{p['icon']}</div>
        <div class="prod-name">{p['name']}</div>
        <div class="prod-price">${w:.2f}<span class="prod-week">/wk</span></div>
        <div class="prod-term">{p['term']} wks · Total ${total:,.0f}</div>
        {badge}
    </div>"""
cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── How It Works ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bw-card">
  <div class="bw-card-title">ℹ️ How This Works</div>
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:24px;">
    <div>
      <p style="font-weight:700; color:#351d65; margin:0 0 6px;">1. Enter Your Numbers</p>
      <p style="color:#343546; font-size:0.88em; line-height:1.6; margin:0;">Tell us your income, how often you're paid, and your regular monthly costs. Everything stays private — nothing is saved.</p>
    </div>
    <div>
      <p style="font-weight:700; color:#351d65; margin:0 0 6px;">2. We Do The Math</p>
      <p style="color:#343546; font-size:0.88em; line-height:1.6; margin:0;">We calculate your take-home pay, subtract your expenses, and apply your comfort level to find a safe weekly payment range.</p>
    </div>
    <div>
      <p style="font-weight:700; color:#351d65; margin:0 0 6px;">3. Shop With Confidence</p>
      <p style="color:#343546; font-size:0.88em; line-height:1.6; margin:0;">Products marked ✅ Fits Budget are within your range. Ask the AI advisor below for personalised guidance.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── CTA ─────────────────────────────────────────────────────────────────────────
cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
with cta_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4a298e, #351d65); border-radius: 16px; padding: 28px; text-align: center; color: white;">
        <div style="font-size: 1.4em; font-weight: 700; margin-bottom: 8px;">Ready to take the next step?</div>
        <div style="opacity: 0.8; margin-bottom: 18px; font-size: 0.95em;">A Bestway advisor can walk you through flexible payment options — no obligation.</div>
        <a href="https://www.bestwayrto.com" target="_blank"
           style="background:#feef02; color:#351d65; font-weight:700; padding:12px 32px; border-radius:25px; text-decoration:none; font-size:1em;">
            Talk to a Bestway Advisor →
        </a>
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# AI SECTION
# ════════════════════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)

# Build budget context string (used by both insight + chat)
affordable = [p for p in PRODUCTS if p["weekly"] <= safe_hi]
stretch_prods = [p for p in PRODUCTS if safe_hi < p["weekly"] <= safe_hi * 1.4]

budget_context = f"""CUSTOMER BUDGET SNAPSHOT
• Gross income: ${gross_income:,.2f} per {pay_freq.split('(')[0].strip().lower()}
• Tax rate: {tax_rate}%  →  Monthly net take-home: ${monthly_net:,.2f}

MONTHLY EXPENSES  (total committed: ${monthly_expenses + existing_monthly:,.2f})
• Rent/Mortgage: ${rent:,.2f}   Utilities: ${utilities:,.2f}   Groceries: ${groceries:,.2f}
• Transportation: ${transport:,.2f}   Insurance: ${insurance:,.2f}   Other: ${other_exp:,.2f}
• Existing RTO/debt: ${existing_monthly:,.2f}/mo (${existing_weekly:.2f}/wk)

AFFORDABILITY
• Monthly disposable: ${disposable_monthly:,.2f}  →  Weekly disposable: ${disposable_weekly:,.2f}
• Expense-to-income ratio: {expense_ratio*100:.1f}%
• Comfort preference: {comfort}
• Safe weekly payment range: ${safe_lo:.2f}–${safe_hi:.2f}

PRODUCTS WITHIN BUDGET: {', '.join([p['name'] + ' $' + str(p['weekly']) + '/wk' for p in affordable]) or 'None at current range'}
STRETCH PRODUCTS: {', '.join([p['name'] + ' $' + str(p['weekly']) + '/wk' for p in stretch_prods[:4]]) or 'None'}"""

# ─── AI Insight Card ─────────────────────────────────────────────────────────────
st.markdown('<div class="bw-card"><div class="bw-card-title">✨ AI Budget Insight — powered by Claude</div>', unsafe_allow_html=True)

ins_left, ins_right = st.columns([3, 1])
with ins_left:
    st.markdown(
        "<p style='color:#767676; font-size:0.9em; margin:0;'>Get a personalised AI analysis of your budget with tailored product recommendations and actionable tips.</p>",
        unsafe_allow_html=True,
    )
with ins_right:
    gen_btn = st.button("✨ Generate Insight", key="gen_insight")

if gen_btn:
    if disposable_weekly <= 0:
        st.warning("Please adjust your inputs — expenses exceed income — before generating an insight.")
    else:
        client = get_client()
        if not client:
            st.error("⚠️ ANTHROPIC_API_KEY not set. Add it to `.streamlit/secrets.toml` or your Streamlit Cloud secrets.")
        else:
            insight_prompt = f"""Here is the customer's budget:

{budget_context}

Write a warm, personalised 3–4 sentence budget insight that:
1. Acknowledges their financial picture positively and specifically
2. States their safe weekly range and what it unlocks
3. Recommends the single best-fit product and explains why
4. Offers one concrete, achievable tip (e.g. 'cutting $X from Y would unlock Z')

Be encouraging, specific with dollar amounts, and keep it conversational."""

            placeholder = st.empty()
            full_text   = ""

            with client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=450,
                system=AI_SYSTEM,
                messages=[{"role": "user", "content": insight_prompt}],
            ) as stream:
                for chunk in stream.text_stream:
                    full_text += chunk
                    placeholder.markdown(
                        f'<div class="ai-insight">{to_html_content(full_text)}▌</div>',
                        unsafe_allow_html=True,
                    )

            placeholder.markdown(
                f'<div class="ai-insight">{to_html_content(full_text)}</div>',
                unsafe_allow_html=True,
            )
            st.session_state.ai_insight = full_text

elif st.session_state.ai_insight:
    st.markdown(
        f'<div class="ai-insight">{to_html_content(st.session_state.ai_insight)}</div>',
        unsafe_allow_html=True,
    )
    if st.button("↺ Regenerate", key="regen"):
        st.session_state.ai_insight = None
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ─── AI Chat Card ────────────────────────────────────────────────────────────────
st.markdown('<div class="bw-card"><div class="bw-card-title">💬 Chat with Your Budget Advisor — Alex (AI)</div>', unsafe_allow_html=True)

chat_top_l, chat_top_r = st.columns([4, 1])
with chat_top_l:
    st.markdown(
        "<p style='color:#767676; font-size:0.9em; margin:0 0 14px;'>Ask anything about your budget, products, or payment strategies. Alex knows your full financial picture.</p>",
        unsafe_allow_html=True,
    )
with chat_top_r:
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.chat_messages = []
        st.rerun()

# Suggested questions (only when chat is empty)
if not st.session_state.chat_messages:
    suggestions = [
        "Which product is the best value for me?",
        "What if I cut groceries by $50/month?",
        "Should I get the washer or the TV first?",
        "How long until I own the 55\" TV outright?",
    ]
    st.markdown("<p style='font-size:0.82em; color:#4a298e; font-weight:600; margin:0 0 8px;'>💡 Try asking:</p>", unsafe_allow_html=True)
    sug_cols = st.columns(2)
    for i, sug in enumerate(suggestions):
        with sug_cols[i % 2]:
            if st.button(sug, key=f"sug_{i}"):
                st.session_state.chat_messages.append({"role": "user", "content": sug})
                st.session_state.pending_response = True
                st.rerun()

# Render chat history
for msg in st.session_state.chat_messages:
    avatar = "🙋" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Fire AI response for suggestion-button clicks
if st.session_state.pending_response:
    st.session_state.pending_response = False
    client = get_client()
    if client:
        stream_chat_response(client, st.session_state.chat_messages, budget_context)
    else:
        st.error("⚠️ ANTHROPIC_API_KEY not configured. Add it to your Streamlit secrets.")

# Chat input
elif user_input := st.chat_input("Ask about your budget, products, or payment plans..."):
    with st.chat_message("user", avatar="🙋"):
        st.write(user_input)
    st.session_state.chat_messages.append({"role": "user", "content": user_input})

    client = get_client()
    if not client:
        with st.chat_message("assistant", avatar="🤖"):
            st.error("⚠️ ANTHROPIC_API_KEY not configured. Add it to your Streamlit secrets.")
    else:
        stream_chat_response(client, st.session_state.chat_messages, budget_context)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="bw-footer">
    <b style="color:white;">BESTWAY</b> · Budget Snapshot Tool · For illustrative purposes only.<br>
    Results are estimates based on self-reported data and do not constitute financial advice.<br>
    AI insights are generated by Claude and may not reflect all individual circumstances.<br>
    <a href="https://www.bestwayrto.com" target="_blank">bestwayrto.com</a>
</div>
""", unsafe_allow_html=True)
