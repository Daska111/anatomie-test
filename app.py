import json
import unicodedata
import streamlit as st

st.set_page_config(page_title="Anatomie – test", page_icon="🧠", layout="wide")

st.markdown("""
<style>
/* Sidebar gradient */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #EEF2FF 0%, #FAF0FB 50%, #FFF0F6 100%) !important;
}

/* Sidebar odkaz styl */
.sidebar-link {
    display: block;
    padding: 7px 10px;
    border-radius: 8px;
    font-size: 14px;
    color: #7F77DD;
    text-decoration: none;
    margin-bottom: 2px;
}
.sidebar-link:hover {
    background: rgba(83,74,183,0.10);
    color: #534AB7;
    text-decoration: none;
}

/* Hlavní nadpis */
.main-title {
    background: linear-gradient(90deg, #534AB7, #D4537E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
}

/* Sekce nadpis */
.sec-title {
    color: #534AB7;
    font-size: 1.3rem;
    font-weight: 600;
    margin: 24px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid;
    border-image: linear-gradient(90deg, #7F77DD, #D4537E) 1;
}

/* Karta otázky */
.q-card {
    border: 0.5px solid rgba(127,119,221,0.3);
    border-radius: 16px;
    padding: 16px 20px;
    background: white;
    margin-bottom: 14px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
}
.q-left { flex: 2; }
.q-right { flex: 1; display: flex; align-items: center; justify-content: center; }

.q-text {
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 12px;
    color: #2d2d2d;
}

/* Stavové boxy vpravo */
.box-neutral {
    background: #EEF2FF;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    color: #534AB7;
    text-align: center;
    width: 100%;
}
.box-correct {
    background: #E1F5EE;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    color: #0F6E56;
    font-weight: 600;
    text-align: center;
    width: 100%;
}
.box-wrong {
    background: #FAECE7;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    color: #993C1D;
    font-weight: 600;
    text-align: center;
    width: 100%;
}
.box-wrong-answer {
    font-size: 12px;
    color: #993C1D;
    text-align: center;
    margin-top: 5px;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7F77DD, #D4537E) !important;
    border-radius: 99px !important;
}
.stProgress > div > div > div {
    background: #EEF2FF !important;
    border-radius: 99px !important;
}

/* Metric karty */
[data-testid="stMetric"] {
    background: #EEF2FF;
    border-radius: 12px;
    padding: 12px !important;
    border: 0.5px solid rgba(127,119,221,0.2);
}
[data-testid="stMetricLabel"] { color: #534AB7 !important; }
[data-testid="stMetricValue"] { color: #3C3489 !important; }

/* Reset tlačítko */
.stButton > button {
    background: white !important;
    color: #534AB7 !important;
    border: 0.5px solid #AFA9EC !important;
    border-radius: 8px !important;
    width: 100%;
}
.stButton > button:hover {
    background: #EEF2FF !important;
}

/* Radio accent */
[data-testid="stRadio"] input[type=radio]:checked {
    accent-color: #534AB7;
}

/* Divider */
hr { border-color: rgba(127,119,221,0.2) !important; }
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

st.markdown(f'<p class="main-title">{data.get("title", "Test")}</p>', unsafe_allow_html=True)

sections = data.get("sections", [])

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.markdown(
    '<p style="font-size:12px;font-weight:600;color:#534AB7;'
    'text-transform:uppercase;letter-spacing:0.05em;margin-bottom:8px;">📚 Kapitoly</p>',
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
    st.markdown(f'<p class="sec-title">{sec["title"]}</p>', unsafe_allow_html=True)

    for q in sec["questions"]:
        total += 1
        qid = f"ans_{q['id']}"

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(
                f'<div class="q-card"><div class="q-left">'
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
                user = st.text_input("Odpověď:", key=qid)
                if user.strip():
                    answered += 1
                    ok = any(norm(user) == norm(a) for a in q["answers"])
                    if ok:
                        correct += 1

            st.markdown("</div></div>", unsafe_allow_html=True)

        with col2:
            if sec["type"] == "mcq":
                choice = st.session_state.get(qid)
                correct_idx = q["answer_index"]
                if choice is None:
                    st.markdown('<div class="box-neutral">Zatím bez odpovědi</div>', unsafe_allow_html=True)
                elif choice == correct_idx:
                    st.markdown('<div class="box-correct">Správně ✅</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="box-wrong">Špatně ❌</div>'
                        f'<div class="box-wrong-answer"><b>Správně:</b> {q["options"][correct_idx]}</div>',
                        unsafe_allow_html=True
                    )

            elif sec["type"] == "bones":
                user = st.session_state.get(qid, "")
                if not user.strip():
                    st.markdown('<div class="box-neutral">Zatím bez odpovědi</div>', unsafe_allow_html=True)
                else:
                    ok = any(norm(user) == norm(a) for a in q["answers"])
                    if ok:
                        st.markdown('<div class="box-correct">Správně ✅</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            f'<div class="box-wrong">Špatně ❌</div>'
                            f'<div class="box-wrong-answer"><b>Správně:</b> {q["answers"][0]}</div>',
                            unsafe_allow_html=True
                        )

# ── Statistiky ─────────────────────────────────────────────────────────────────
st.divider()
st.progress(answered / total if total else 0)

c1, c2, c3 = st.columns(3)
c1.metric("Zodpovězeno", f"{answered}/{total}")
c2.metric("Správně", correct)
c3.metric("Úspěšnost", f"{(correct / answered * 100):.0f}%" if answered else "—")
