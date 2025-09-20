import os
import requests
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# ----------------------- Poster fetching -----------------------
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None
    except:
        return None

# ----------------------- Trailer fetching -----------------------
def fetch_trailer(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
        data = requests.get(url).json()
        for vid in data.get("results", []):
            if vid["type"].lower() == "trailer" and vid["site"].lower() == "youtube":
                return f"https://www.youtube.com/watch?v={vid['key']}"
        return "https://www.youtube.com"
    except:
        return "https://www.youtube.com"

# ----------------------- Streaming providers -----------------------
def fetch_watch_providers(movie_id, country="IN"):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={API_KEY}"
        data = requests.get(url).json()
        results = data.get('results', {})
        providers = results.get(country, {}).get('flatrate', [])
        return {p['provider_name']: p['logo_path'] for p in providers} if providers else {}
    except:
        return {}

# ----------------------- Fetch popular movies -----------------------
def fetch_popular_movies(language='hi', page=1):
    """
    Fetches popular movies from TMDB for a given language.
    """
    try:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language={language}&sort_by=popularity.desc&page={page}"
        data = requests.get(url).json()
        movies = []
        for m in data.get('results', []):
            movies.append({
                "id": m['id'],
                "title": m['title'],
                "overview": m.get('overview',''),
                "release_date": m.get('release_date',''),
                "poster": fetch_poster(m['id']),
                "trailer": fetch_trailer(m['id']),
                "providers": fetch_watch_providers(m['id'])
            })
        return movies
    except:
        return []

# ----------------------- Filter-based recommendation -----------------------
def recommend_movies_filtered(language='hi', genre=None, actor=None, year=None, top_n=10):
    movies = fetch_popular_movies(language=language, page=1)
    filtered = []
    for m in movies:
        # Fetch detailed info for genres, cast if needed
        try:
            url = f"https://api.themoviedb.org/3/movie/{m['id']}?api_key={API_KEY}&language=en-US&append_to_response=credits,genres"
            data = requests.get(url).json()
            movie_genres = [g['name'] for g in data.get('genres',[])]
            cast = [c['name'] for c in data.get('credits', {}).get('cast', [])]
            director = [c['name'] for c in data.get('credits', {}).get('crew', []) if c['job']=='Director']
        except:
            movie_genres, cast, director = [], [], []

        # Apply filters
        if genre and genre.lower() not in ' '.join(movie_genres).lower():
            continue
        if actor and actor.lower() not in ' '.join(cast).lower():
            continue
        if year and m.get('release_date'):
            if str(year) != m['release_date'][:4]:
                continue

        m['genres'] = ' '.join(movie_genres)
        m['cast'] = ' '.join(cast)
        m['crew'] = ' '.join(director)
        filtered.append(m)

    # Sort by popularity (already sorted by TMDB, but safe)
    filtered = filtered[:top_n]
    return filtered

# ----------------------- Content-based recommendation -----------------------
def recommend_similar(movie_title, movies_list=None, top_n=10):
    if not movies_list:
        movies_list = fetch_popular_movies(language='hi', page=1)

    # Build tags
    for m in movies_list:
        m['tags'] = (m.get('overview','') + ' ' + m.get('genres','') + ' ' + m.get('cast','') + ' ' + m.get('crew','')).strip()

    titles = [m['title'] for m in movies_list]
    if movie_title not in titles:
        return f"❌ Movie '{movie_title}' not found in TMDB popular list."

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform([m['tags'] for m in movies_list]).toarray()
    similarity = cosine_similarity(vectors)

    index = titles.index(movie_title)
    distances = list(enumerate(similarity[index]))
    movies_list_sorted = sorted(distances, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommended = []
    for i in movies_list_sorted:
        idx = i[0]
        recommended.append(movies_list[idx])
    return recommended
