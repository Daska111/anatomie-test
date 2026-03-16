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

# ── Pracovní listy – data ──────────────────────────────────────────────────────
WORKSHEETS = [
    {
        "id": "obratel",
        "title": "Stavba obratle",
        "image": "IMG_0091.jpg",
        # souřadnice jako % šířky/výšky obrázku – levý obratel (pohled zepředu)
        # čísla 1–7 dle legendy v učebnici
        "labels": [
            {"n": 1, "x": 14.0, "y": 21.5, "text": "trnový výběžek"},
            {"n": 2, "x": 14.0, "y": 26.5, "text": "příčný výběžek"},
            {"n": 3, "x": 14.0, "y": 31.0, "text": "obratlový otvor"},
            {"n": 4, "x": 35.0, "y": 38.5, "text": "tělo obratle"},
            {"n": 5, "x": 52.0, "y": 26.5, "text": "horní kloubní výběžek"},
            {"n": 6, "x": 52.0, "y": 21.5, "text": "obratlový oblouk"},
            {"n": 7, "x": 72.0, "y": 50.5, "text": "dolní kloubní výběžek"},
        ],
        "crop": {"top": 12, "bottom": 55},  # zobrazit jen horní část obrázku (%)
    },
    {
        "id": "hrudnik",
        "title": "Kostra hrudníku",
        "image": "IMG_0093.jpg",
        "labels": [
            {"n": 1, "x": 14.0, "y": 52.0, "text": "pravá žebra"},
            {"n": 2, "x": 14.0, "y": 72.0, "text": "nepravá žebra"},
            {"n": 3, "x": 14.0, "y": 80.0, "text": "volná žebra"},
            {"n": 4, "x": 72.0, "y": 68.0, "text": "mečovitý výběžek kosti hrudní"},
            {"n": 5, "x": 79.0, "y": 55.0, "text": "tělo kosti hrudní"},
            {"n": 6, "x": 79.0, "y": 42.0, "text": "lopatka"},
            {"n": 7, "x": 79.0, "y": 36.0, "text": "rukojeť kosti hrudní"},
            {"n": 8, "x": 79.0, "y": 30.0, "text": "kost klíční"},
        ],
        "crop": {"top": 28, "bottom": 92},
    },
    {
        "id": "lebka",
        "title": "Kostra hlavy – lebka",
        "image": "IMG_0094.jpg",
        "labels": [
            {"n": 1,  "x": 18.0, "y": 38.0, "text": "kost čelní"},
            {"n": 2,  "x": 18.0, "y": 48.0, "text": "kost klínová"},
            {"n": 3,  "x": 18.0, "y": 53.0, "text": "kost slzní"},
            {"n": 4,  "x": 18.0, "y": 58.0, "text": "kost nosní"},
            {"n": 5,  "x": 18.0, "y": 66.0, "text": "horní čelist"},
            {"n": 6,  "x": 40.0, "y": 80.0, "text": "dolní čelist"},
            {"n": 7,  "x": 72.0, "y": 62.0, "text": "kost lícní"},
            {"n": 8,  "x": 72.0, "y": 56.0, "text": "kost týlní"},
            {"n": 9,  "x": 72.0, "y": 49.0, "text": "kost spánková"},
            {"n": 10, "x": 72.0, "y": 38.0, "text": "kost temenní"},
        ],
        "crop": {"top": 28, "bottom": 92},
    },
    {
        "id": "lopatka",
        "title": "Lopatka",
        "image": "IMG_0095.jpg",
        "labels": [
            {"n": 1,  "x": 48.0, "y": 18.0, "text": "horní hrana"},
            {"n": 2,  "x": 34.0, "y": 18.0, "text": "hákovitý výběžek"},
            {"n": 3,  "x": 22.0, "y": 28.0, "text": "nadpažek (acromion) – kloubní jamka"},
            {"n": 4,  "x": 22.0, "y": 38.0, "text": "vnější úhel"},
            {"n": 5,  "x": 22.0, "y": 55.0, "text": "vnější hrana"},
            {"n": 6,  "x": 40.0, "y": 75.0, "text": "dolní úhel"},
            {"n": 7,  "x": 65.0, "y": 60.0, "text": "vnitřní hrana"},
            {"n": 8,  "x": 65.0, "y": 48.0, "text": "jáma podhřebenová"},
            {"n": 9,  "x": 65.0, "y": 38.0, "text": "hřeben lopatky"},
            {"n": 10, "x": 65.0, "y": 28.0, "text": "jáma nadhřebenová"},
            {"n": 11, "x": 55.0, "y": 18.0, "text": "horní úhel"},
        ],
        "crop": {"top": 28, "bottom": 92},
    },
    {
        "id": "kost_pazni",
        "title": "Kost pažní",
        "image": "IMG_0096.jpg",
        "labels": [
            {"n": 1,  "x": 22.0, "y": 30.0, "text": "hlavice"},
            {"n": 2,  "x": 22.0, "y": 35.0, "text": "anatomický krček"},
            {"n": 3,  "x": 22.0, "y": 40.0, "text": "chirurgický krček"},
            {"n": 4,  "x": 38.0, "y": 33.0, "text": "malý hrbol"},
            {"n": 5,  "x": 45.0, "y": 30.0, "text": "velký hrbol"},
            {"n": 6,  "x": 38.0, "y": 55.0, "text": "tělo"},
            {"n": 7,  "x": 22.0, "y": 80.0, "text": "vnitřní epikondyl"},
            {"n": 8,  "x": 35.0, "y": 85.0, "text": "kladka (pro kost loketní)"},
            {"n": 9,  "x": 42.0, "y": 83.0, "text": "hlavička (pro kost vřetenní)"},
            {"n": 10, "x": 55.0, "y": 80.0, "text": "jáma loketní"},
        ],
        "crop": {"top": 28, "bottom": 95},
    },
    {
        "id": "predlokti",
        "title": "Kosti předloktí",
        "image": "IMG_0097.jpg",
        "labels": [
            {"n": 1,  "x": 28.0, "y": 28.0, "text": "olecranon (výběžek kosti loketní)"},
            {"n": 2,  "x": 28.0, "y": 55.0, "text": "tělo kosti loketní"},
            {"n": 3,  "x": 28.0, "y": 78.0, "text": "hlavička kosti loketní"},
            {"n": 4,  "x": 35.0, "y": 84.0, "text": "bodcovitý výběžek kosti loketní"},
            {"n": 5,  "x": 42.0, "y": 82.0, "text": "kloubní plocha pro zápěstní kůstky"},
            {"n": 6,  "x": 55.0, "y": 78.0, "text": "bodcovitý výběžek kosti vřetenní"},
            {"n": 7,  "x": 58.0, "y": 55.0, "text": "tělo kosti vřetenní"},
            {"n": 8,  "x": 58.0, "y": 35.0, "text": "drsnatina kosti vřetenní"},
            {"n": 9,  "x": 58.0, "y": 30.0, "text": "krček kosti vřetenní"},
            {"n": 10, "x": 58.0, "y": 26.0, "text": "hlavička kosti vřetenní"},
        ],
        "crop": {"top": 25, "bottom": 90},
    },
    {
        "id": "panev",
        "title": "Kost pánevní",
        "image": "IMG_0100.jpg",
        "labels": [
            {"n": 1,  "x": 22.0, "y": 28.0, "text": "hřeben kosti kyčelní"},
            {"n": 2,  "x": 22.0, "y": 38.0, "text": "přední horní trn kosti kyčelní"},
            {"n": 3,  "x": 22.0, "y": 48.0, "text": "přední dolní trn kosti kyčelní"},
            {"n": 4,  "x": 22.0, "y": 55.0, "text": "acetabulum (jamka kyčelního kloubu)"},
            {"n": 5,  "x": 22.0, "y": 65.0, "text": "kost sedací"},
            {"n": 6,  "x": 22.0, "y": 75.0, "text": "hrbol kosti sedací"},
            {"n": 7,  "x": 65.0, "y": 65.0, "text": "kost stydká"},
            {"n": 8,  "x": 65.0, "y": 55.0, "text": "kost kyčelní"},
            {"n": 9,  "x": 65.0, "y": 42.0, "text": "kloubní plocha pro kost křížovou"},
            {"n": 10, "x": 65.0, "y": 28.0, "text": "lopata kosti kyčelní"},
        ],
        "crop": {"top": 28, "bottom": 92},
    },
    {
        "id": "femur",
        "title": "Kost stehenní (femur)",
        "image": "IMG_0101.jpg",
        "labels": [
            {"n": 1, "x": 30.0, "y": 20.0, "text": "hlavice"},
            {"n": 2, "x": 22.0, "y": 24.0, "text": "velký chocholík"},
            {"n": 3, "x": 22.0, "y": 28.0, "text": "krček"},
            {"n": 4, "x": 38.0, "y": 26.0, "text": "malý chocholík"},
            {"n": 5, "x": 38.0, "y": 55.0, "text": "tělo"},
            {"n": 6, "x": 38.0, "y": 78.0, "text": "vnitřní kondyl"},
            {"n": 7, "x": 55.0, "y": 78.0, "text": "vnější kondyl"},
            {"n": 8, "x": 38.0, "y": 84.0, "text": "kloubní plocha pro čéšku"},
            {"n": 9, "x": 55.0, "y": 84.0, "text": "kloubní plochy pro kost holenní"},
        ],
        "crop": {"top": 25, "bottom": 90},
    },
    {
        "id": "berec",
        "title": "Kosti bérce",
        "image": "IMG_0101.jpg",  # sdílí stránku s femurem – použijeme IMG_0102
        "labels": [
            {"n": 1, "x": 22.0, "y": 28.0, "text": "hlavička kosti lýtkové"},
            {"n": 2, "x": 22.0, "y": 55.0, "text": "tělo kosti lýtkové"},
            {"n": 3, "x": 22.0, "y": 80.0, "text": "zevní kotník"},
            {"n": 4, "x": 35.0, "y": 82.0, "text": "vnitřní kotník"},
            {"n": 5, "x": 55.0, "y": 55.0, "text": "tělo kosti holenní"},
            {"n": 6, "x": 55.0, "y": 35.0, "text": "drsnatina kosti holenní"},
            {"n": 7, "x": 55.0, "y": 28.0, "text": "vnitřní kondyl kosti holenní"},
            {"n": 8, "x": 42.0, "y": 26.0, "text": "vnější kondyl kosti holenní"},
        ],
        "crop": {"top": 25, "bottom": 90},
    },
]

# ── Pomocná funkce – HTML pracovní list ───────────────────────────────────────
def render_worksheet(ws: dict, github_raw_base: str):
    img_url = f"{github_raw_base}/{ws['image']}"
    labels_js = json.dumps(ws["labels"], ensure_ascii=False)
    crop_top = ws.get("crop", {}).get("top", 0)
    crop_bottom = ws.get("crop", {}).get("bottom", 100)

    html = f"""
<style>
  .ws-wrap {{
    position: relative;
    width: 100%;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    background: #f8f5f0;
  }}
  .ws-img {{
    width: 100%;
    display: block;
    object-fit: cover;
    object-position: top;
  }}
  .ws-btn {{
    position: absolute;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #e63946;
    color: white;
    font-weight: bold;
    font-size: 13px;
    border: 2px solid white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: translate(-50%, -50%);
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    transition: background 0.2s, transform 0.15s;
    z-index: 10;
  }}
  .ws-btn:hover {{ background: #c1121f; transform: translate(-50%, -50%) scale(1.2); }}
  .ws-btn.revealed {{ background: #2d6a4f; }}
  .ws-tooltip {{
    position: absolute;
    background: rgba(20,20,20,0.92);
    color: #fff;
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 13px;
    white-space: nowrap;
    pointer-events: none;
    display: none;
    z-index: 20;
    transform: translateX(-50%);
  }}
  .ws-reset {{
    margin-top: 10px;
    padding: 6px 18px;
    background: #457b9d;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
  }}
  .ws-reset:hover {{ background: #1d3557; }}
  .ws-score {{
    margin-top: 8px;
    font-size: 14px;
    color: #333;
  }}
</style>

<div class="ws-wrap" id="ws-{ws['id']}">
  <img class="ws-img" src="{img_url}"
       style="margin-top: -{crop_top}%; margin-bottom: -{100-crop_bottom}%;"
       id="wsimg-{ws['id']}" />
</div>
<div class="ws-score" id="score-{ws['id']}">Odkryto: 0 / {len(ws['labels'])}</div>
<button class="ws-reset" onclick="resetWS('{ws['id']}')">↺ Resetovat</button>

<script>
(function() {{
  var labels = {labels_js};
  var cropTop = {crop_top};
  var cropBottom = {crop_bottom};
  var revealed = {{}};
  var wsId = "{ws['id']}";

  function pct(val) {{ return val + "%"; }}

  function placeButtons() {{
    var wrap = document.getElementById("ws-" + wsId);
    var img = document.getElementById("wsimg-" + wsId);
    if (!wrap || !img) return;

    // čistíme staré
    wrap.querySelectorAll(".ws-btn, .ws-tooltip").forEach(function(e) {{ e.remove(); }});

    var wrapH = wrap.offsetHeight;
    var cropRange = cropBottom - cropTop;

    labels.forEach(function(lbl) {{
      // přepočet y z celkového % na % v oříznutém výřezu
      var relY = (lbl.y - cropTop) / cropRange * 100;

      var btn = document.createElement("button");
      btn.className = "ws-btn" + (revealed[lbl.n] ? " revealed" : "");
      btn.textContent = lbl.n;
      btn.style.left = pct(lbl.x);
      btn.style.top = pct(relY);
      btn.id = "btn-" + wsId + "-" + lbl.n;

      var tip = document.createElement("div");
      tip.className = "ws-tooltip";
      tip.textContent = lbl.text;
      tip.style.left = pct(lbl.x);
      tip.style.top = "calc(" + pct(relY) + " - 38px)";
      tip.id = "tip-" + wsId + "-" + lbl.n;

      btn.addEventListener("click", function() {{
        revealed[lbl.n] = true;
        btn.classList.add("revealed");
        tip.style.display = "block";
        updateScore();
        setTimeout(function() {{ tip.style.display = "none"; }}, 3000);
      }});

      wrap.appendChild(btn);
      wrap.appendChild(tip);
    }});
  }}

  function updateScore() {{
    var cnt = Object.keys(revealed).length;
    var el = document.getElementById("score-" + wsId);
    if (el) el.textContent = "Odkryto: " + cnt + " / " + labels.length;
  }}

  window["resetWS"] = window["resetWS"] || {{}};
  window["resetWS_" + wsId] = function() {{
    revealed = {{}};
    placeButtons();
    updateScore();
  }};

  // global reset dispatcher
  var origReset = window.resetWS;
  window.resetWS = function(id) {{
    if (window["resetWS_" + id]) window["resetWS_" + id]();
  }};

  // init po načtení obrázku
  var img = document.getElementById("wsimg-" + wsId);
  if (img && img.complete) {{ placeButtons(); }}
  else if (img) {{ img.addEventListener("load", placeButtons); }}
  window.addEventListener("resize", placeButtons);
}})();
</script>
"""
    st.components.v1.html(html, height=700, scrolling=True)


# ── Hlavní app ────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝 Test", "🦴 Pracovní listy"])

# ── TAB 1: Test ────────────────────────────────────────────────────────────────
with tab1:
    data = load_questions()
    st.title(data.get("title", "Test"))

    sections = data.get("sections", [])

    st.sidebar.header("Kapitoly")
    selected = st.sidebar.multiselect(
        "Vyber kapitoly",
        options=[s["id"] for s in sections],
        default=[s["id"] for s in sections],
        format_func=lambda sid: next((s["title"] for s in sections if s["id"] == sid), sid),
    )

    if st.sidebar.button("Reset"):
        for k in list(st.session_state.keys()):
            if k.startswith("ans_"):
                del st.session_state[k]
        st.rerun()

    total = 0
    answered = 0
    correct = 0

    for sec in sections:
        if sec["id"] not in selected:
            continue

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
                        format_func=lambda i: q["options"][i],
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

    st.divider()
    st.progress(answered / total if total else 0)

    c1, c2, c3 = st.columns(3)
    c1.metric("Zodpovězeno", f"{answered}/{total}")
    c2.metric("Správně", correct)
    c3.metric("Úspěšnost", f"{(correct / answered * 100):.0f}%" if answered else "—")


# ── TAB 2: Pracovní listy ──────────────────────────────────────────────────────
with tab2:
    st.title("🦴 Pracovní listy – anatomické nákresy")
    st.markdown(
        "Klikni na **červené číslo** v obrázku a zobrazí se název dané části. "
        "Po 3 sekundách se popisek schová. Tlačítkem **Resetovat** skryješ všechny odpovědi."
    )

    GITHUB_RAW = "https://raw.githubusercontent.com/Daska111/anatomie-test/main"

    ws_options = {ws["title"]: ws for ws in WORKSHEETS}
    selected_ws = st.selectbox("Vyber pracovní list:", list(ws_options.keys()))

    ws = ws_options[selected_ws]
    st.subheader(ws["title"])
    render_worksheet(ws, GITHUB_RAW)
