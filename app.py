import json
import unicodedata
import streamlit as st

st.set_page_config(page_title="Anatomie – test", page_icon="🧠", layout="wide")

st.markdown("""
<style>
/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #EEF2FF 0%, #FAF0FB 50%, #FFF0F6 100%) !important;
}
[data-testid="stSidebar"] * { color: #534AB7 !important; }
.sidebar-link {
    display: block;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 13px;
    color: #7F77DD !important;
    text-decoration: none;
    margin-bottom: 3px;
    line-height: 1.4;
}
.sidebar-link:hover {
    background: rgba(83,74,183,0.12);
    color: #3C3489 !important;
    text-decoration: none;
}

/* ── Hlavní nadpis ── */
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #534AB7, #D4537E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    padding-bottom: 0;
}

/* ── Nadpis sekce ── */
.sec-header {
    font-size: 1.5rem;
    font-weight: 800;
    color: #534AB7;
    margin: 32px 0 16px 0;
    padding: 12px 18px;
    background: linear-gradient(90deg, #EEF2FF, #FFF0F6);
    border-radius: 12px;
    border-left: 5px solid #7F77DD;
}

/* ── Karta otázky ── */
.q-card {
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    background: #FAFAFA;
    border: 1px solid rgba(127,119,221,0.2);
}

/* ── Text otázky ── */
.q-text {
    font-size: 17px;
    font-weight: 700;
    color: #26215C;
    margin-bottom: 14px;
    line-height: 1.5;
}

/* ── Stavové boxy ── */
.box-neutral {
    background: linear-gradient(135deg, #EEF2FF, #FAF0FB);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    color: #534AB7;
    font-weight: 600;
    text-align: center;
    border: 1px solid rgba(127,119,221,0.3);
}
.box-correct {
    background: linear-gradient(135deg, #E1F5EE, #D4F5E9);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    color: #085041;
    font-weight: 700;
    text-align: center;
    border: 1px solid #5DCAA5;
}
.box-wrong {
    background: linear-gradient(135deg, #FAECE7, #FAEEDA);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    color: #712B13;
    font-weight: 700;
    text-align: center;
    border: 1px solid #F0997B;
}
.correct-answer {
    margin-top: 8px;
    font-size: 13px;
    color: #712B13;
    text-align: center;
    font-weight: 600;
}

/* ── Radio button ── */
[data-testid="stRadio"] label {
    font-size: 15px !important;
    color: #3d3d3d !important;
    padding: 3px 0 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 6px !important;
}

/* ── Text input ── */
[data-testid="stTextInput"] input {
    font-size: 15px !important;
    border-radius: 8px !important;
    border: 1px solid rgba(127,119,221,0.4) !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #7F77DD !important;
    box-shadow: 0 0 0 2px rgba(127,119,221,0.15) !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7F77DD, #D4537E) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: #EEF2FF !important;
    border-radius: 99px !important;
    height: 10px !important;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #EEF2FF, #FAF0FB);
    border-radius: 14px;
    padding: 16px !important;
    border: 1px solid rgba(127,119,221,0.2);
}
[data-testid="stMetricLabel"] p { color: #534AB7 !important; font-size: 14px !important; }
[data-testid="stMetricValue"] { color: #26215C !important; font-size: 2rem !important; font-weight: 700 !important; }

/* ── Reset button ── */
.stButton > button {
    background: white !important;
    color: #534AB7 !important;
    border: 1px solid #AFA9EC !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100%;
    padding: 8px !important;
}
.stButton > button:hover {
    background: #EEF2FF !important;
    border-color: #7F77DD !important;
}

/* ── Divider ── */
hr { border-color: rgba(127,119,221,0.25) !important; }

/* ── Skrýt výchozí st.subheader ── */
h2, h3 { display: none !important; }
</style>
""", unsafe_allow_html=True)


def load_questions(path: str = "questions.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return " ".join(s.split())


data = load_questions()

st.markdown(f'<div class="main-title">{data.get("title", "Test")}</div>', unsafe_allow_html=True)

sections = data.get("sections", [])

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<p style="font-size:12px;font-weight:700;color:#3C3489 !important;'
    'text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;">📚 Kapitoly</p>',
    unsafe_allow_html=True
)

links_html = "".join(
    f'<a class="sidebar-link" href="#{s["id"]}">▸ {s["title"]}</a>'
    for s in sections
)
st.sidebar.markdown(links_html, unsafe_allow_html=True)
st.sidebar.markdown("---")

if st.sidebar.button("🔄 Reset odpovědí"):
    for k in list(st.session_state.keys()):
        if k.startswith("ans_"):
            del st.session_state[k]
    st.rerun()

# ── Otázky ─────────────────────────────────────────────────────────────────────
total = 0
answered = 0
correct = 0

for sec in sections:
    # Kotva + nadpis sekce
    st.markdown(
        f'<div id="{sec["id"]}"></div>'
        f'<div class="sec-header">{sec["title"]}</div>',
        unsafe_allow_html=True
    )

    for q in sec["questions"]:
        total += 1
        qid = f"ans_{q['id']}"

        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f'<div class="q-card">'
                f'<div class="q-text">{q["q"]}</div>',
                unsafe_allow_html=True
            )

            if sec["type"] == "mcq":
                choice = st.radio(
                    "",
                    options=list(range(len(q["options"]))),
                    index=None,
                    format_func=lambda i, q=q: q["options"][i],
                    key=qid
                )
                if choice is not None:
                    answered += 1
                    if choice == q["answer_index"]:
                        correct += 1

            elif sec["type"] == "bones":
                user = st.text_input("Tvoje odpověď:", key=qid)
                if user.strip():
                    answered += 1
                    ok = any(norm(user) == norm(a) for a in q["answers"])
                    if ok:
                        correct += 1

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
            if sec["type"] == "mcq":
                choice = st.session_state.get(qid)
                correct_idx = q["answer_index"]
                if choice is None:
                    st.markdown('<div class="box-neutral">💭 Zatím bez<br>odpovědi</div>', unsafe_allow_html=True)
                elif choice == correct_idx:
                    st.markdown('<div class="box-correct">✅ Správně!</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="box-wrong">❌ Špatně</div>'
                        f'<div class="correct-answer">Správně:<br><b>{q["options"][correct_idx]}</b></div>',
                        unsafe_allow_html=True
                    )

            elif sec["type"] == "bones":
                user = st.session_state.get(qid, "")
                if not user.strip():
                    st.markdown('<div class="box-neutral">💭 Zatím bez<br>odpovědi</div>', unsafe_allow_html=True)
                else:
                    ok = any(norm(user) == norm(a) for a in q["answers"])
                    if ok:
                        st.markdown('<div class="box-correct">✅ Správně!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f'<div class="box-wrong">❌ Špatně</div>'
                            f'<div class="correct-answer">Správně:<br><b>{q["answers"][0]}</b></div>',
                            unsafe_allow_html=True
                        )

# ── Statistiky ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.progress(answered / total if total else 0)
st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("Zodpovězeno", f"{answered} / {total}")
c2.metric("Správně", correct)
c3.metric("Úspěšnost", f"{(correct / answered * 100):.0f} %" if answered else "—")
