"""
================================================================================
    BOOK RECOMMENDATION SYSTEM - Flask Web Application
================================================================================

A modern web application that provides personalized book recommendations using
two sophisticated recommendation algorithms:
  1. Collaborative Filtering - Based on user ratings and preferences
  2. Content-Based Filtering - Based on book characteristics and metadata

Author: AI Project Team
Version: 1.0
Last Updated: January 2026

================================================================================
"""

from flask import Flask, render_template, request
import numpy as np
import pickle
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get the root directory of the project
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
TEMPLATE_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR / "app" / "static"

# ============================================================================
# LOAD PRE-COMPUTED MODELS AND DATA
# ============================================================================

def load_models():
    """Load all pre-computed machine learning models and data."""
    try:
        # Popular books data (top 50 rated books with metadata)
        popular_df = pickle.load(open(DATA_DIR / 'popular.pkl', 'rb'))
        
        # Collaborative Filtering Models
        pt = pickle.load(open(DATA_DIR / 'pt.pkl', 'rb'))                          # User-Item Matrix
        books = pickle.load(open(DATA_DIR / 'books.pkl', 'rb'))                    # Book metadata
        similarity_scores = pickle.load(open(DATA_DIR / 'similarity_scores.pkl', 'rb'))  # Cosine similarity
        
        # Content-Based Filtering Models
        content_similarity = pickle.load(open(DATA_DIR / 'content_similarity.pkl', 'rb'))
        content_book_index = pickle.load(open(DATA_DIR / 'content_book_index.pkl', 'rb'))
        books_unique = pickle.load(open(DATA_DIR / 'books_unique.pkl', 'rb'))
        
        return {
            'popular_df': popular_df,
            'pt': pt,
            'books': books,
            'similarity_scores': similarity_scores,
            'content_similarity': content_similarity,
            'content_book_index': content_book_index,
            'books_unique': books_unique
        }
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Model file not found: {e}. Ensure all pickle files are in {DATA_DIR}")

# Load models globally
models = load_models()
popular_df = models['popular_df']
pt = models['pt']
books = models['books']
similarity_scores = models['similarity_scores']
content_similarity = models['content_similarity']
content_book_index = models['content_book_index']
books_unique = models['books_unique']

# ============================================================================
# FLASK APP CONFIGURATION
# ============================================================================

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__, 
                template_folder=str(TEMPLATE_DIR),
                static_folder=str(STATIC_DIR),
                static_url_path='/static')
    
    return app

app = create_app()

# ============================================================================
# ROUTE HANDLERS
# ============================================================================

@app.route('/')
def home():
    """
    Display homepage with top 50 most popular and highest-rated books.
    
    Returns:
        Rendered HTML template with:
        - book_name: List of book titles
        - author: List of authors
        - votes: List of rating counts
        - rating: List of average ratings
        - image: List of book cover image URLs
    """
    return render_template('Book_recommend.html',
                        book_name=list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        votes=list(popular_df['num_ratings'].values),
                        rating=list(popular_df['avg_rating'].values),
                        image=list(popular_df['Image-URL-M'].values))

@app.route('/recommend')
def recommend_ui():
    """
    Display the recommendation search interface.
    
    Returns:
        Rendered HTML template for book search and recommendations
    """
    return render_template('Recommend.html')

@app.route('/Recommend_Books', methods=['POST'])
def recommend():
    """
    Process recommendation request and return personalized book suggestions.
    
    POST Parameters:
        - user_input (str): Book title or author name to search for
        - recommendation_type (str): 'collaborative' or 'content'
    
    Returns:
        Rendered HTML with:
        - data: List of recommended books [title, author, image_url]
        - recommendation_type: Type of recommendation used
        - error_message: Error message if no books found
    """
    
    # Get user input and recommendation type from form
    user_input = request.form.get('user_input', '').strip()
    recommendation_type = request.form.get('recommendation_type', 'collaborative')
    
    data = []
    found_book = None
    error_message = ""
    
    # ========================================================================
    # SEARCH FOR BOOK IN DATABASE
    # ========================================================================
    
    # Try exact match first (faster lookup)
    if user_input in content_book_index:
        found_book = user_input
    else:
        # Try partial match by book title or author name (case-insensitive)
        matching_books = books_unique[
            (books_unique['Book-Title'].str.contains(user_input, case=False, na=False)) |
            (books_unique['Book-Author'].str.contains(user_input, case=False, na=False))
        ]['Book-Title'].values
        
        if len(matching_books) > 0:
            found_book = matching_books[0]  # Use first match
    
    # ========================================================================
    # GENERATE RECOMMENDATIONS
    # ========================================================================
    
    if found_book:
        if recommendation_type == 'content':
            # ================================================================
            # CONTENT-BASED RECOMMENDATION
            # ================================================================
            # Find books with similar characteristics (title, author, features)
            
            idx = content_book_index[found_book]
            sim_scores = list(enumerate(content_similarity[idx]))
            
            # Sort by similarity score (descending) and get top 6 (excluding the input book)
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:7]
            
            for i, score in sim_scores:
                book_info = books_unique.iloc[i]
                item = [
                    book_info['Book-Title'],
                    book_info['Book-Author'],
                    book_info['Image-URL-M']
                ]
                data.append(item)
        else:
            # ================================================================
            # COLLABORATIVE FILTERING RECOMMENDATION
            # ================================================================
            # Find books that similar users (with similar ratings) liked
            
            if found_book in pt.index:
                index = np.where(pt.index == found_book)[0][0]
                
                # Get similarity scores for this book
                similar_items = sorted(
                    list(enumerate(similarity_scores[index])), 
                    key=lambda x: x[1], 
                    reverse=True
                )[1:7]  # Top 6 similar books (excluding itself)
                
                # Extract book details for each recommendation
                for i in similar_items:
                    item = []
                    temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                    
                    data.append(item)
            else:
                error_message = f"Book '{found_book}' not found in our collaborative filtering database."
    else:
        # No matching book found
        error_message = f"No books found matching '{user_input}'. Try searching by book title or author name."

    # Render results page with recommendations or error message
    return render_template('Recommend.html', 
                         data=data, 
                         recommendation_type=recommendation_type, 
                         error_message=error_message)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Internal server error"), 500

# ============================================================================
# APP STARTUP
# ============================================================================

if __name__ == '__main__':
    # Start Flask development server
    # DEBUG MODE: Enables auto-reload and better error messages
    # WARNING: Never use debug=True in production!
    app.run(debug=True)



