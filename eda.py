import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

# Load datasets
movies = pd.read_csv(r"C:\Users\Sirisha T\Desktop\movie\tmdb_5000_movies.csv")
credits = pd.read_csv(r"C:\Users\Sirisha T\Desktop\movie\tmdb_5000_credits.csv")

# Convert JSON-like columns to Python lists
movies['genres'] = movies['genres'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])
movies['keywords'] = movies['keywords'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])
credits['cast'] = credits['cast'].apply(lambda x: [d['name'] for d in ast.literal_eval(x)] if pd.notnull(x) else [])
credits['crew'] = credits['crew'].apply(lambda x: [d['name'] for d in ast.literal_eval(x) if d['job'] == 'Director'] if pd.notnull(x) else [])

# Merge both datasets
movies = movies.merge(credits, left_on='id', right_on='movie_id', how='left')

# --- 1. Most common genres ---
all_genres = movies['genres'].explode().value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=all_genres.values, y=all_genres.index, palette="viridis")
plt.title("Top 10 Movie Genres")
plt.show()

# --- 2. Most common languages ---
lang_counts = movies['original_language'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=lang_counts.values, y=lang_counts.index, palette="plasma")
plt.title("Top 10 Languages")
plt.show()

# --- 3. Movies per year ---
movies['release_date'] = pd.to_datetime(movies['release_date'], errors='coerce')
year_counts = movies['release_date'].dt.year.value_counts().sort_index()
plt.figure(figsize=(12,5))
sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o")
plt.title("Movies Released per Year")
plt.show()
