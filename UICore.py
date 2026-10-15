from dotenv import load_dotenv
load_dotenv()

import html
import json
from typing import List, Optional

import streamlit as st
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, field_validator

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="CineScan • Movie Info Extractor",
    page_icon="🎬",
    layout="wide",
)

HERO_IMG = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?auto=format&fit=crop&w=1800&q=80"

# -------------------- Styling --------------------
st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}

.stApp {{
    background:
        radial-gradient(circle at 15% 10%, rgba(255,75,92,0.12), transparent 40%),
        radial-gradient(circle at 85% 30%, rgba(124,58,237,0.14), transparent 45%),
        #0b0d14;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 1.5rem; max-width: 1150px; }}

/* Hero */
.hero {{
    position: relative; border-radius: 24px; overflow: hidden;
    padding: 64px 48px; margin-bottom: 28px;
    background:
        linear-gradient(100deg, rgba(11,13,20,0.96) 25%, rgba(11,13,20,0.55) 100%),
        url('{HERO_IMG}') center/cover no-repeat;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}
.hero .badge {{
    display:inline-block; padding: 6px 14px; border-radius: 999px; font-size: 0.78rem;
    background: rgba(255,75,92,0.15); color: #ff6b7a; border: 1px solid rgba(255,75,92,0.4);
    letter-spacing: 1px; text-transform: uppercase; font-weight: 600;
}}
.hero h1 {{
    font-size: 3rem; font-weight: 800; margin: 16px 0 8px 0; line-height: 1.1;
    background: linear-gradient(90deg, #fff, #ff8a96 60%, #b794f6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.hero p {{ color: #b8bccb; font-size: 1.05rem; max-width: 560px; margin: 0; }}

/* Cards */
.card {{
    background: rgba(255,255,255,0.04); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 18px;
    padding: 22px 24px; margin-bottom: 16px;
}}
.card h4 {{ margin: 0 0 12px 0; color: #fff; font-weight: 600; font-size: 1rem; }}
.card p, .card li {{ color: #c9cddb; line-height: 1.65; }}
.label {{ color: #8a8fa3; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; }}
.value {{ color: #fff; font-size: 1.05rem; font-weight: 600; margin-bottom: 14px; }}

/* Chips */
.chip {{
    display:inline-block; padding: 6px 14px; margin: 0 8px 8px 0; border-radius: 999px;
    font-size: 0.85rem; font-weight: 500; color: #fff;
    background: linear-gradient(135deg, rgba(255,75,92,0.35), rgba(124,58,237,0.35));
    border: 1px solid rgba(255,255,255,0.15);
}}
.chip.alt {{ background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.12); color:#dfe2ee; }}

/* Title banner */
.title-banner {{
    border-radius: 20px; padding: 28px 32px; margin-bottom: 16px;
    background: linear-gradient(135deg, rgba(255,75,92,0.2), rgba(124,58,237,0.2));
    border: 1px solid rgba(255,255,255,0.12);
    display:flex; justify-content: space-between; align-items:center; gap: 24px; flex-wrap: wrap;
}}
.title-banner h2 {{ margin:0; color:#fff; font-size: 2.1rem; font-weight: 800; }}
.title-banner .sub {{ color:#c4c8d8; margin-top: 6px; }}
.ring {{
    --p: 0; width: 92px; height: 92px; border-radius: 50%;
    background: conic-gradient(#ffb800 calc(var(--p) * 1%), rgba(255,255,255,0.1) 0);
    display:flex; align-items:center; justify-content:center; flex-shrink: 0;
}}
.ring-inner {{
    width: 72px; height: 72px; border-radius: 50%; background: #11131c;
    display:flex; flex-direction: column; align-items:center; justify-content:center;
    color:#ffb800; font-weight:700; font-size: 1.3rem; line-height: 1;
}}
.ring-inner small {{ color:#8a8fa3; font-size: 0.6rem; margin-top: 3px; font-weight: 500; }}

/* Inputs & buttons */
.stTextArea textarea {{
    background: rgba(255,255,255,0.04) !important; color: #fff !important;
    border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 14px !important;
    font-size: 0.95rem;
}}
.stTextArea textarea:focus {{ border-color: #ff4b5c !important; box-shadow: 0 0 0 2px rgba(255,75,92,0.25) !important; }}
.stButton > button {{
    border-radius: 12px; font-weight: 600; border: 1px solid rgba(255,255,255,0.15);
    transition: all .2s ease;
}}
.stButton > button:hover {{ transform: translateY(-2px); border-color: #ff4b5c; }}
.stButton > button[kind="primary"] {{
    background: linear-gradient(90deg, #ff4b5c, #7c3aed); border: none; color: #fff; padding: 0.7rem 1rem;
    box-shadow: 0 8px 24px rgba(255,75,92,0.35);
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #10121b, #0b0d14);
    border-right: 1px solid rgba(255,255,255,0.06);
}}
#MainMenu, footer {{ visibility: hidden; }}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------- Model & Schema --------------------
@st.cache_resource
def get_model():
    return ChatMistralAI(model="open-mistral-7b", temperature=0)


model = get_model()


class Movie(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: Optional[List[str]] = None
    director: Optional[str] = None
    main_cast: Optional[List[str]] = None
    setting_location: Optional[str] = None
    plot: Optional[str] = None
    themes: Optional[List[str]] = None
    ratings: Optional[float] = None
    notable_features: Optional[List[str]] = None
    short_summary: Optional[str] = None

    # Small models often return a list for director — accept both.
    @field_validator("director", "setting_location", mode="before")
    @classmethod
    def _join_lists(cls, v):
        if isinstance(v, list):
            return ", ".join(str(x) for x in v)
        return v


parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
Extract movie information from the paragraph.
Rules:
- "director" and "setting_location" must be a single string (join multiple names with commas).
- Use null for anything not mentioned.
- Return ONLY the JSON object.
{format_instructions}
"""),
    ("human", "{paragraph}"),
])

# -------------------- Helpers --------------------
def esc(x) -> str:
    return html.escape(str(x))


def chips(items, alt=False) -> str:
    cls = "chip alt" if alt else "chip"
    return "".join(f'<span class="{cls}">{esc(i)}</span>' for i in items)


SAMPLES = {
    "📺 Mirzapur": (
        "Mirzapur is a gritty crime thriller web series created by Puneet Krishna and directed by "
        "Gurmmeet Singh and others. Released in 2018 on Amazon Prime Video, the show stars Pankaj "
        "Tripathi, Ali Fazal, Divyendu Sharma, Shweta Tripathi, and Rasika Dugal. Set in the lawless "
        "town of Mirzapur in Uttar Pradesh, the story revolves around a ruthless power struggle between "
        "rival gangs. It is rated 8.5 out of 10 on IMDb."
    ),
    "🚀 Interstellar": (
        "Interstellar (2014) is a sci-fi epic directed by Christopher Nolan, starring Matthew McConaughey, "
        "Anne Hathaway and Jessica Chastain. A team of astronauts travels through a wormhole near Saturn "
        "to find a new home for humanity as Earth becomes uninhabitable. Themes include love, time and "
        "survival. Praised for its visuals and Hans Zimmer's score, it holds an 8.7 rating on IMDb."
    ),
    "🦇 The Dark Knight": (
        "The Dark Knight (2008), directed by Christopher Nolan, stars Christian Bale, Heath Ledger and "
        "Aaron Eckhart. Set in Gotham City, Batman faces the anarchic Joker in a battle for the city's "
        "soul. Heath Ledger's performance won a posthumous Oscar. It is rated 9.0 on IMDb."
    ),
}


def load_sample(text: str):
    st.session_state["paragraph"] = text


def clear_text():
    st.session_state["paragraph"] = ""


# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("### 🎞️ CineScan")
    st.caption("AI-powered movie data extraction")
    st.divider()
    st.markdown("**How it works**")
    st.markdown("1. Paste any text about a movie or show\n2. Hit **Extract**\n3. Get clean, structured details")
    st.divider()
    st.markdown("**Fields extracted**")
    st.markdown(
        chips(
            ["Title", "Year", "Genre", "Director", "Cast", "Setting", "Plot",
             "Themes", "Rating", "Features", "Summary"],
            alt=True,
        ),
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Powered by Mistral AI • LangChain • Streamlit")

# -------------------- Hero --------------------
st.markdown(
    """
<div class="hero">
    <span class="badge">🎬 AI Powered</span>
    <h1>Movie Information<br>Extractor</h1>
    <p>Drop in any paragraph about a film or series and watch it turn into beautifully structured details in seconds.</p>
</div>
""",
    unsafe_allow_html=True,
)

# -------------------- Input --------------------
st.markdown("##### ✨ Try a sample")
cols = st.columns(len(SAMPLES))
for col, (label, text) in zip(cols, SAMPLES.items()):
    col.button(label, use_container_width=True, on_click=load_sample, args=(text,))

st.text_area(
    "Movie description",
    key="paragraph",
    height=190,
    placeholder="Paste any text about a movie or series here...",
    label_visibility="collapsed",
)

c1, c2 = st.columns([4, 1])
submitted = c1.button("🚀  Extract Information", type="primary", use_container_width=True)
c2.button("🗑️ Clear", use_container_width=True, on_click=clear_text)

# -------------------- Extraction --------------------
if submitted:
    paragraph = st.session_state.get("paragraph", "")
    if not paragraph.strip():
        st.warning("Please enter some text about a movie.")
    else:
        with st.spinner("🎞️ Rolling the cameras... extracting details"):
            try:
                final_prompt = prompt.invoke({
                    "paragraph": paragraph,
                    "format_instructions": parser.get_format_instructions(),
                })
                response = model.invoke(final_prompt)
            except Exception as e:
                st.error(f"Error while calling the model: {e}")
                st.info("Make sure your `MISTRAL_API_KEY` is correctly set in the `.env` file.")
                st.stop()

        try:
            movie = parser.parse(response.content)
        except Exception as e:
            st.warning("Could not parse into the structured format. Showing the raw response:")
            st.code(response.content, language="json")
            st.caption(f"Parser error: {str(e)[:300]}")
            st.stop()

        st.toast("Extraction complete!", icon="✅")

        # ---- Title banner with rating ring ----
        meta = " • ".join(
            x for x in [str(movie.release_year) if movie.release_year else "", ", ".join(movie.genre or [])] if x
        )
        ring = ""
        if movie.ratings is not None:
            pct = max(0, min(100, movie.ratings * 10 if movie.ratings <= 10 else movie.ratings))
            ring = (
                f'<div class="ring" style="--p:{pct}"><div class="ring-inner">'
                f'{movie.ratings:g}<small>/ 10</small></div></div>'
            )
        st.markdown(
            f"""
<div class="title-banner">
    <div>
        <div class="label">Title</div>
        <h2>🎥 {esc(movie.title)}</h2>
        <div class="sub">{esc(meta)}</div>
    </div>
    {ring}
</div>
""",
            unsafe_allow_html=True,
        )

        # ---- Details ----
        left, right = st.columns([1, 1])

        with left:
            info = ""
            if movie.director:
                info += f'<div class="label">Director</div><div class="value">🎬 {esc(movie.director)}</div>'
            if movie.release_year:
                info += f'<div class="label">Release Year</div><div class="value">📅 {movie.release_year}</div>'
            if movie.setting_location:
                info += f'<div class="label">Setting</div><div class="value">📍 {esc(movie.setting_location)}</div>'
            if info:
                st.markdown(f'<div class="card">{info}</div>', unsafe_allow_html=True)

            if movie.genre:
                st.markdown(f'<div class="card"><h4>🎭 Genre</h4>{chips(movie.genre)}</div>', unsafe_allow_html=True)
            if movie.themes:
                st.markdown(f'<div class="card"><h4>💡 Themes</h4>{chips(movie.themes, alt=True)}</div>', unsafe_allow_html=True)

        with right:
            if movie.main_cast:
                st.markdown(f'<div class="card"><h4>⭐ Main Cast</h4>{chips(movie.main_cast)}</div>', unsafe_allow_html=True)
            if movie.short_summary:
                st.markdown(f'<div class="card"><h4>📝 Short Summary</h4><p>{esc(movie.short_summary)}</p></div>', unsafe_allow_html=True)
            if movie.notable_features:
                lis = "".join(f"<li>{esc(f)}</li>" for f in movie.notable_features)
                st.markdown(f'<div class="card"><h4>🏆 Notable Features</h4><ul>{lis}</ul></div>', unsafe_allow_html=True)

        if movie.plot:
            st.markdown(f'<div class="card"><h4>📖 Plot</h4><p>{esc(movie.plot)}</p></div>', unsafe_allow_html=True)

        # ---- Raw data + download ----
        data = movie.model_dump()
        with st.expander("🧾 View raw structured data"):
            st.json(data)
        st.download_button(
            "⬇️ Download JSON",
            data=json.dumps(data, indent=2, ensure_ascii=False),
            file_name=f"{movie.title.replace(' ', '_')}.json",
            mime="application/json",
        )