import json
import unicodedata
import streamlit as st

st.set_page_config(page_title="Anatomie – test", page_icon="🧠", layout="wide")

# ── CSS styling ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #EEF2FF 0%, #FAF0FB 50%, #FFF0F6 100%) !important;
}

/* Sidebar nadpis */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] .sidebar-header {
    color: #534AB7 !important;
}

/* Sidebar odkaz styl */
.sidebar-link {
    display: block;
    padding: 7px 10px;
    border-radius: 8px;
    font-size: 14px;
    color: #7F77DD;
    text-decoration: none;
    transition: background 0.15s;
    margin-bottom: 2px;
}
.sidebar-link:hover {
    background: rgba(83,74,183,0.10);
    color: #534AB7;
}

/* Hlavní nadpis s gradientem */
.main-title {
    background: linear-gradient(90deg, #534AB7, #D4537E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
}

/* Karty otázek */
.question-card {
    border: 0.5px solid rgba(127, 119, 221, 0.25);
    border-radius: 16px;
    padding: 16px;
    background: white;
    margin-bottom: 12px;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7F77DD, #D4537E) !important;
}

/* Metric karty */
[data-testid="stMetric"] {
    background: #EEF2FF;
    border-radius: 12px;
    padding: 12px !important;
}

/* Reset tlačítko */
.stButton > button {
    background: white !important;
    color: #534AB7 !important;
    border: 0.5px solid #AFA9EC !important;
    border-radius: 8px !important;
}
.stButton > button:hover {
    background: #EEF2FF !important;
}

/* Subheader barva */
h2, h3 {
    color: #534AB7 !important;
}

/* Info box – bez odpovědi */
[data-testid="stInfo"] {
    background: #EEF2FF !important;
    border-left-color: #7F77DD !important;
    color: #534AB7 !important;
}

/* Success box */
[data-testid="stSuccess"] {
    background: #E1F5EE !important;
    border-left-color: #1D9E75 !important;
}

/* Error box */
[data-testid="stError"] {
    background: #FAECE7 !important;
    border-left-color: #D85A30 !important;
}

/* Radio button akcent */
[data-testid="stRadio"] label span {
    color: #534AB7 !important;
}
</style>
""", unsafe_allow_html=True)


def load_questions(path: str = "questions.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return " ".join(s.split())

def card_start():
    st.markdown(
        """<div style="
            border: 0.5px solid rgba(127,119,221,0.25);
            border-radius: 16px;
            padding: 16px;
            background: white;
            margin-bottom: 12px;">
        """, unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


data = load_questions()

# Gradient nadpis
st.markdown(
    f'<p class="main-title">{data.get("title", "Test")}</p>',
    unsafe_allow_html=True
)

sections = data.get("sections", [])

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<p style="font-size:13px; font-weight:600; color:#534AB7; '
    'text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px;">📚 Kapitoly</p>',
    unsafe_allow_html=True
)

links_html = ""
for sec in sections:
    links_html += f'<a class="sidebar-link" href="#{sec["id"]}">▸ {sec["title"]}</a>\n'
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
    st.markdown(f"<div id='{sec['id']}'></div>", unsafe_allow_html=True)
    st.subheader(sec["title"])

    for q in sec["questions"]:
        total += 1
        qid = f"ans_{q['id']}"

        card_start()
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**{q['q']}**")

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
                user = st.text_input("Odpověď:", key=qid)
                if user.strip():
                    answered += 1
                    ok = any(norm(user) == norm(a) for a in q["answers"])
                    if ok:
                        correct += 1

        with col2:
            if sec["type"] == "mcq":
                choice = st.session_state.get(qid)
                correct_idx = q["answer_index"]
                if choice is None:
                    st.info("Zatím bez odpovědi")
                else:
                    if choice == correct_idx:
                        st.success("Správně ✅")
                    else:
                        st.error("Špatně ❌")
                        st.markdown(f"**Správně:** {q['options'][correct_idx]}")

            elif sec["type"] == "bones":
                user = st.session_state.get(qid, "")
                if not user.strip():
                    st.info("Zatím bez odpovědi")
                else:
                    ok = any(norm(user) == norm(a) for a in q["answers"])
                    if ok:
                        st.success("Správně ✅")
                    else:
                        st.error("Špatně ❌")
                        st.markdown(f"**Správně:** {q['answers'][0]}")

        card_end()

# ── Statistiky ─────────────────────────────────────────────────────────────────
st.divider()
st.progress(answered / total if total else 0)

c1, c2, c3 = st.columns(3)
c1.metric("Zodpovězeno", f"{answered}/{total}")
c2.metric("Správně", correct)
c3.metric("Úspěšnost", f"{(correct / answered * 100):.0f}%" if answered else "—")
