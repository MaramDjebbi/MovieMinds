import csv
import tkinter as tk
from PIL import Image, ImageTk 


# Function to read movie data from the CSV file
def read_movie_data(file_path):
    movies = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movies.append(row)
    return movies

# Read movie data from the CSV file
movie_dataset = read_movie_data('dataset.csv')

def recommend_movies(user_profile, movies):
    liked_movies = user_profile['liked_movies']
    recommended_movies = []
    max_match_count = 0

    for movie in movies:
        match_count = 0

        if movie['title'] not in liked_movies:  # Exclude movies already liked by the user
            if movie['genre'] == user_profile['preferred_genre']:
                match_count += 1
            if any(actor in user_profile['favorite_actors'] for actor in movie['actors']):
                match_count += 1
            if movie['title'] in user_profile['liked_movies']:
                match_count += 1
            if float(movie['rating']) >= user_profile['min_rating']:
                match_count += 1

            if match_count > max_match_count:
                max_match_count = match_count
                recommended_movies = [movie['title']]
            elif match_count == max_match_count and match_count > 0:
                recommended_movies.append(movie['title'])

    return recommended_movies

def get_user_profile():
    user_profile = {
        'liked_movies': liked_movies_entry.get().split(','),
        'preferred_genre': preferred_genre_entry.get(),
        'favorite_actors': favorite_actors_entry.get().split(','),
        'min_rating': float(min_rating_entry.get())
    }

    recommendations = recommend_movies(user_profile, movie_dataset)
    recommended_movies_label.config(text=f"Recommended Movies: {', '.join(recommendations)}")

root = tk.Tk()
root.title("MovieMinds: Your Favorite Recommendation System")

root.geometry("600x400")  # Set window size to 800x600

# Load the background image...
bg_image = Image.open("Background.jpg")  # Replace with your image file
#bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)  # Correct attribute name
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Canvas to place the background image...
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Labels, Entry Fields, Buttons, and other elements...
tk.Label(root, text="Your Liked Movies (Comma-separated):").pack()
liked_movies_entry = tk.Entry(root)
liked_movies_entry.pack()

tk.Label(root, text="Your Preferred Genre:").pack()
preferred_genre_entry = tk.Entry(root)
preferred_genre_entry.pack()

tk.Label(root, text="Your Favorite Actors (Comma-separated):").pack()
favorite_actors_entry = tk.Entry(root)
favorite_actors_entry.pack()

tk.Label(root, text="Minimum Movie Rating:").pack()
min_rating_entry = tk.Entry(root)
min_rating_entry.pack()

# Button to generate recommendations
generate_button = tk.Button(root, text="Generate Recommendations", command=get_user_profile)
generate_button.pack()

# Label to display recommendations
recommended_movies_label = tk.Label(root, text="")
recommended_movies_label.pack()

root.mainloop()

