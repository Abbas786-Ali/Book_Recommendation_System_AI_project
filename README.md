# Book Recommendation System (Flask)

A simple web app that recommends books using two approaches:
- Collaborative filtering (similar users/books)
- Content-based similarity (matching by title/author/content features)

The app serves a popular-books homepage and a recommendation form where you can search by book title or author and choose the recommendation method.

---

## Features
- Popular books landing page with title, author, ratings, and cover images
- Search by exact or partial book title/author
- Choose recommendation type: collaborative or content-based
- Clean Flask templates for results and errors

## Project Structure
```
Book_Recommendation_System_AI_project/
├── Books.csv.zip
├── Ratings.csv
├── Users.csv
├── book recommendation/
│   ├── app.py
│   ├── books_unique.pkl
│   ├── popular.pkl
│   ├── pt.pkl
│   ├── similarity_scores.pkl
│   └── (expected)
│       ├── books.pkl
│       ├── content_similarity.pkl
│       └── content_book_index.pkl
└── templates/
    ├── Book_recommend.html
    └── Recommend.html
```

Note: The Flask app expects templates beside `app.py` by default. See “Template location” below.

## Prerequisites
- Python 3.9+ (tested on Linux)
- Pip

## Installation
You can install dependencies either via a requirements file (recommended) or manually.

### Option A: Manual install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Flask numpy pandas
```

### Option B: Using requirements.txt
If you prefer, create `requirements.txt` with:
```
Flask
numpy
pandas
```
Then install:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Data Artifacts (Pickles)
The app loads several precomputed pickle files. Place them next to `app.py` (or update the code paths):
- `popular.pkl`: DataFrame with columns `Book-Title`, `Book-Author`, `num_ratings`, `avg_rating`, `Image-URL-M`
- `pt.pkl`: Pivot table/DataFrame indexed by `Book-Title` used for collaborative filtering
- `similarity_scores.pkl`: 2D numpy array with similarity values for collaborative filtering
- `books.pkl`: DataFrame containing book metadata (title, author, image URL)
- `books_unique.pkl`: DataFrame of unique books with `Book-Title`, `Book-Author`, `Image-URL-M`
- `content_similarity.pkl`: 2D numpy array for content-based similarity
- `content_book_index.pkl`: Dict mapping `Book-Title` → row index into `content_similarity`

If any of these are missing, generate them from your preprocessing scripts/notebooks before running the app.

## Template Location
Current code in `app.py` sets:
```python
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
```
You have two options:
1) Move the `templates/` folder so it lives at `book recommendation/templates/` (recommended), or
2) Change the `template_folder` to point to the top-level `templates` directory.

## Running Locally
Run from the `book recommendation/` directory so relative paths resolve:
```bash
cd "book recommendation"
source ../.venv/bin/activate  # if you created a venv at project root
python app.py
```

The app starts in debug mode on `http://127.0.0.1:5000/`.

## Usage
- Open the homepage to see popular books
- Navigate to the recommendation form (`/recommend`)
- Enter a book title or author (partial matches allowed)
- Choose recommendation type: collaborative or content
- Submit to view recommended books with title, author, and cover image

## Troubleshooting
- Templates not found: Ensure `templates/` is inside `book recommendation/` or update `template_folder`.
- Missing pickles: Create/generate the required `.pkl` files and place them next to `app.py`.
- Wrong working directory: Make sure you run `python app.py` from `book recommendation/` so relative file loads work.
- Import errors on unpickle: Install `pandas`—unpickling DataFrames requires it.

## Notes
- `Ratings.csv` and `Users.csv` are raw datasets; use them to build the pickles via offline preprocessing.
- `Books.csv.zip` may contain additional book metadata useful for constructing `books.pkl` and `books_unique.pkl`.

## Next Steps
- Add a `requirements.txt` and automated data-building scripts
- Dockerize the app
- Add pagination and richer book metadata
