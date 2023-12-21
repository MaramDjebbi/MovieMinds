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
        'preferred_genre': preferred_genre_var.get(),
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

# Labels, Entry Fields, Buttons, and other elements on the canvas...

label1 = tk.Label(canvas, text="Your Liked Movies (Comma-separated):", fg="#118ab2")
label1.place(x=320 , y=10)
liked_movies_entry = tk.Entry(canvas)
liked_movies_entry.place(x=365 , y=40)

genre_options = [
    "Crime", "Action", "Drama", "Sci-Fi", "War", "Thriller",
    "Fantasy", "Biography", "Adventure", "Western", "Comedy",
    "Musical", "Romance"
]

label2 = tk.Label(canvas, text="Your Preferred Genre:", fg="#118ab2")
label2.place(x=372 , y=70)
# Dropdown menu for preferred genre
preferred_genre_var = tk.StringVar(root)
preferred_genre_var.set(genre_options[0])  # Set the default value
preferred_genre_dropdown = tk.OptionMenu(canvas, preferred_genre_var, *genre_options)
preferred_genre_dropdown.place(x=400, y=100)

label3 = tk.Label(canvas, text="Your Favorite Actors (Comma-separated):", fg="#118ab2")
label3.place(x=310 , y=140)
favorite_actors_entry = tk.Entry(canvas)
favorite_actors_entry.place(x=365 , y=170)

label4 = tk.Label(canvas, text="Minimum Movie Rating:", fg="#118ab2")
label4.place(x=372 , y=200)
min_rating_entry = tk.Entry(canvas)
min_rating_entry.place(x=365 , y=230)

generate_button = tk.Button(canvas, text="Generate Recommendations", command=get_user_profile, fg="#003049")
generate_button.place(x=340 , y=265)

recommended_movies_label = tk.Label(canvas, text="",fg="#003049")
recommended_movies_label.place(x=320 , y=290)

root.mainloop()

