# Development Guide

This guide helps you understand and develop features for the Book Recommendation System.

## 🏗️ Project Structure Overview

### `/src/app.py` - Main Application
- Flask app initialization and configuration
- Route handlers (`/`, `/recommend`, `/Recommend_Books`)
- Model loading functions
- Error handlers

### `/app/templates/` - HTML Templates
- `Book_recommend.html` - Homepage with popular books
- `Recommend.html` - Search and recommendation interface

### `/data/` - Data Directory
- `raw/` - Original datasets and archives
- `processed/` - Pre-computed ML models (pickle files)

### `/config.py` - Configuration
- Flask settings
- Application constants
- Environment-specific configuration

---

## 🔄 Request Flow

### Homepage Request (`GET /`)
```
1. User visits http://localhost:5000/
2. Flask route handler: home()
3. Load popular_df from pickle
4. Render Book_recommend.html with data
5. Display top 50 books with ratings
```

### Recommendation Request
```
1. User submits search form (POST /Recommend_Books)
2. Extract user_input and recommendation_type
3. Search for book in database
4. If found:
   - If content-based: Calculate content similarity
   - If collaborative: Find similar users' preferences
5. Return top 6 recommendations
6. Display results with Book_recommend.html template
```

---

## 🧠 Recommendation Algorithms

### Collaborative Filtering
**File:** `data/processed/pt.pkl`, `similarity_scores.pkl`

```python
# Pseudo-code
user_ratings = load_pivot_table()  # Books × Users matrix
similarity = cosine_similarity(user_ratings)
similar_books = find_top_6(similarity[book_idx])
```

**Advantages:**
- Works well for popular books
- Discovers trends
- No need for book metadata

**Disadvantages:**
- Cold start problem for new books
- May miss niche preferences

### Content-Based Filtering
**File:** `data/processed/content_similarity.pkl`

```python
# Pseudo-code
book_features = extract_features(title, author, genre)
similarity = cosine_similarity(book_features)
similar_books = find_top_6(similarity[book_idx])
```

**Advantages:**
- Works for new books
- Better for niche items
- Predictable results

**Disadvantages:**
- Limited by feature extraction
- May miss user preferences
- Requires good metadata

---

## 🛠️ Adding New Features

### Add a New Route

```python
@app.route('/api/books/<title>')
def get_book_info(title):
    """Get detailed info about a specific book."""
    book = books_unique[books_unique['Book-Title'] == title]
    if not book.empty:
        return jsonify(book.to_dict(orient='records')[0])
    return jsonify({'error': 'Book not found'}), 404
```

### Add a New Template

1. Create `app/templates/new_page.html`
2. Add route handler in `src/app.py`
3. Render template: `return render_template('new_page.html')`

### Modify the UI

- Edit CSS in `Book_recommend.html` or `Recommend.html` `<style>` section
- Or create external stylesheet in `app/static/css/`

Example:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

---

## 📊 Generating New Models

### Step 1: Prepare Raw Data
```bash
cd notebooks
jupyter notebook book-recommender-system.ipynb
```

### Step 2: Run Preprocessing
- Follow notebook cells to:
  - Load CSV files
  - Clean data
  - Create matrices
  - Generate similarity scores

### Step 3: Save Models
```python
import pickle

pickle.dump(popular_books, open('../data/processed/popular.pkl', 'wb'))
pickle.dump(similarity_matrix, open('../data/processed/similarity_scores.pkl', 'wb'))
# ... etc
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test homepage
curl http://localhost:5000/

# Test recommendation
curl -X POST http://localhost:5000/Recommend_Books \
  -d "user_input=Harry Potter&recommendation_type=collaborative"
```

### Unit Tests

Create `tests/test_app.py`:

```python
import pytest
from src.app import app

@pytest.fixture
def client():
    return app.test_client()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Top 50 Rated Books' in response.data
```

Run tests:
```bash
pytest tests/
```

---

## 🚀 Deployment

### Development Server
```bash
python run.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 'src.app:app'
```

### Docker
```bash
docker build -t book-recommender .
docker run -p 8000:8000 book-recommender
```

### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
export SECRET_KEY=your-secret-key
```

---

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| `src/app.py` | Main application logic |
| `app/templates/*.html` | UI templates |
| `config.py` | Configuration |
| `run.py` | Entry point |
| `requirements.txt` | Dependencies |
| `notebooks/*.ipynb` | Data processing |

---

## 🐛 Debugging

### Enable Flask Debug Mode
```python
# In src/app.py
app.run(debug=True)
```

### Check Loaded Models
```bash
python -c "from src.app import models; print(models.keys())"
```

### View Template Variables
```html
<!-- In template -->
{{ book_name|length }}  <!-- Count items -->
```

---

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [scikit-learn Metrics](https://scikit-learn.org/stable/modules/metrics.html)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)

---

## 💡 Tips & Tricks

1. **Model Loading Speed:** Pickle files load entire matrices into memory. Consider lazy-loading for very large datasets.

2. **Search Optimization:** Exact match lookup is O(1), partial match is O(n). Order matters!

3. **UI Responsiveness:** Bootstrap classes handle mobile layout automatically.

4. **Performance:** Cache recommendation results for popular searches.

---

Happy Coding! 🎉
