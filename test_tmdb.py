import requests

API_KEY = "2274ea1e7ea801b44f8cd658a3760725" # replace with your real TMDB key
language = "hi"
url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_original_language={language}&sort_by=popularity.desc&page=1"

try:
    response = requests.get(url, timeout=10)  # add timeout to prevent hanging
    response.raise_for_status()  # raises error for bad responses
    data = response.json()
    print("Status code:", response.status_code)
    print("First movie:", data['results'][0]['title'])
except requests.exceptions.RequestException as e:
    print("Error:", e)
