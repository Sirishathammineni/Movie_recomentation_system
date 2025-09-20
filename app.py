import streamlit as st
from recommender import fetch_popular_movies, recommend_movies_filtered, recommend_similar

# ------------------- Page Config -------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# ------------------- CSS Styling -------------------
st.markdown("""
<style>
body {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
                url('https://images.unsplash.com/photo-1524985069026-dd778a71c7b4?auto=format&fit=crop&w=1950&q=80')
                no-repeat center center fixed;
    background-size: cover;
    color: #fff;
    font-family: 'Segoe UI', sans-serif;
}
.stApp > header, .stApp > div:nth-child(1) { text-align: center; }
h1, h2 { text-shadow: 2px 2px 8px rgba(0,0,0,0.7); }
.movie-card {
    position: relative;
    overflow: hidden;
    border-radius: 15px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    background: rgba(255,255,255,0.9);
    margin-bottom: 25px;
    color: #000;
}
.movie-card:hover { transform: scale(1.08); box-shadow: 0 10px 25px rgba(0,0,0,0.35); }
.movie-card::after {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(120deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 60%);
    transform: rotate(25deg) translateX(-100%);
    transition: all 0.7s ease;
    pointer-events: none;
}
.movie-card:hover::after { transform: rotate(25deg) translateX(200%); }
.trailer-btn {
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    background-color: #ff3b2e;
    color: #fff;
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 8px;
    display: none;
    cursor: pointer;
    font-size: 14px;
    transition: 0.3s;
}
.movie-card:hover .trailer-btn { display: block; }
.movie-title { font-weight: bold; font-size: 20px; margin: 5px 0; }
.movie-details { font-size: 14px; color: #333; }
.provider-logo { height:30px; margin:2px; }
.stButton>button { background-color:#ff6f61; color:#fff; font-weight:bold; border-radius:10px; padding:10px 20px; transition: 0.3s; }
.stButton>button:hover { background-color:#ff3b2e; }
</style>
""", unsafe_allow_html=True)

# ------------------- Page Title -------------------
st.title("🎬 Movie Recommender System")
st.subheader("Discover your next favorite movie in any language!")

# ------------------- Indian Languages Dropdown -------------------
indian_languages = {
    "hi": "Hindi", "ta": "Tamil", "te": "Telugu",
    "kn": "Kannada", "ml": "Malayalam", "bn": "Bengali",
    "mr": "Marathi", "pa": "Punjabi", "gu": "Gujarati",
    "or": "Odia"
}
language = st.selectbox(
    "Select Language",
    options=list(indian_languages.keys()),
    format_func=lambda x: indian_languages[x]
)

# ------------------- Recommendation Type -------------------
option = st.radio("Choose recommendation type:", ('Filter-based', 'Content-based'))

# ------------------- Filter-based -------------------
if option == 'Filter-based':
    genre = st.text_input("Enter genre (e.g., Action)")
    actor = st.text_input("Enter actor name (optional)")
    year = st.text_input("Enter release year (optional)")

    if st.button("Show Recommendations"):
        recs = recommend_movies_filtered(language=language, genre=genre or None, actor=actor or None, year=year or None)
        if not recs:
            st.warning("No movies found.")
        else:
            cols = st.columns(3)
            for i, movie in enumerate(recs):
                with cols[i % 3]:
                    providers_html = ""
                    for name, logo in movie.get("providers", {}).items():
                        logo_url = f"https://image.tmdb.org/t/p/w92{logo}"
                        providers_html += f'<img class="provider-logo" src="{logo_url}" title="{name}">'
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{movie['poster']}" width="100%" style="border-radius:12px;">
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-details">
                            <b>Genres:</b> {movie.get('genres','N/A')}<br>
                            <b>Cast:</b> {movie.get('cast','N/A')}<br>
                            <b>Watch:</b> {providers_html if providers_html else 'Not available in India'}
                        </div>
                        <a href="{movie.get('trailer','https://www.youtube.com')}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                    </div>
                    """, unsafe_allow_html=True)

# ------------------- Content-based -------------------
elif option == 'Content-based':
    movie_title = st.text_input("Enter a movie title")
    if st.button("Show Similar Movies"):
        recs = recommend_similar(movie_title)
        if isinstance(recs, str):
            st.error(recs)
        else:
            cols = st.columns(3)
            for i, movie in enumerate(recs):
                with cols[i % 3]:
                    providers_html = ""
                    for name, logo in movie.get("providers", {}).items():
                        logo_url = f"https://image.tmdb.org/t/p/w92{logo}"
                        providers_html += f'<img class="provider-logo" src="{logo_url}" title="{name}">'
                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{movie['poster']}" width="100%" style="border-radius:12px;">
                        <div class="movie-title">{movie['title']}</div>
                        <div class="movie-details">
                            <b>Genres:</b> {movie.get('genres','N/A')}<br>
                            <b>Cast:</b> {movie.get('cast','N/A')}<br>
                            <b>Watch:</b> {providers_html if providers_html else 'Not available in India'}
                        </div>
                        <a href="{movie.get('trailer','https://www.youtube.com')}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                    </div>
                    """, unsafe_allow_html=True)
