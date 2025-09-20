from recommender import recommend_movies, recommend_similar

# Filter-based example
print(recommend_movies(genre="Romance", language="hi", actor="Shah Rukh Khan"))

# Content-based example
print(recommend_similar("The Dark Knight"))
