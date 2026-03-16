import json
import unicodedata
import streamlit as st

st.set_page_config(page_title="Anatomie – test", page_icon="🧠", layout="wide")

def load_questions(path: str = "questions.json") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def norm(s: str) -> str:
    s = (s or "").strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return " ".join(s.split())

def card_start():
    st.markdown(
        """
        <div style="
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 16px;
            padding: 16px;
            background: rgba(250, 250, 250, 0.6);
            margin-bottom: 12px;">
        """,
        unsafe_allow_html=True,
    )

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

data = load_questions()
st.title(data.get("title", "Test"))

sections = data.get("sections", [])
all_ids = [s["id"] for s in sections]

# ── Session state init ─────────────────────────────────────────────────────────
if "selected" not in st.session_state:
    st.session_state["selected"] = set(all_ids)

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("📚 Kapitoly")

if st.sidebar.button("🔄 Reset odpovědí"):
    for k in list(st.session_state.keys()):
        if k.startswith("ans_"):
            del st.session_state[k]
    st.rerun()

st.sidebar.markdown("---")

col_a, col_b = st.sidebar.columns(2)
if col_a.button("✅ Vše"):
    st.session_state["selected"] = set(all_ids)
    st.rerun()
if col_b.button("❌ Nic"):
    st.session_state["selected"] = set()
    st.rerun()

st.sidebar.markdown("---")

for sec in sections:
    checked = sec["id"] in st.session_state["selected"]
    new_checked = st.sidebar.checkbox(
        sec["title"],
        value=checked,
        key=f"chk_{sec['id']}"
    )
    if new_checked != checked:
        if new_checked:
            st.session_state["selected"].add(sec["id"])
        else:
            st.session_state["selected"].discard(sec["id"])
        st.rerun()

selected = st.session_state["selected"]

# ── Navigační přehled kapitol na začátku stránky ───────────────────────────────
st.markdown("### 📋 Přehled vybraných kapitol")

visible_sections = [s for s in sections if s["id"] in selected]

if visible_sections:
    nav_cols = st.columns(3)
    for i, sec in enumerate(visible_sections):
        nav_cols[i % 3].markdown(f"[{sec['title']}](#{sec['id']})")
else:
    st.info("Žádná kapitola není vybrána. Zaškrtni kapitoly v levém panelu.")

st.divider()

# ── Otázky ─────────────────────────────────────────────────────────────────────
total = 0
answered = 0
correct = 0

for sec in sections:
    if sec["id"] not in selected:
        continue

    # HTML kotva pro navigaci
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
