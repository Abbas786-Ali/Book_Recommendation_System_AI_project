# 📚 Book Recommendation System

> A modern, intelligent web application that recommends books tailored to your preferences using machine learning algorithms.

## 🎯 Overview

This Flask-powered application delivers personalized book recommendations using two sophisticated recommendation engines:

- **👥 Collaborative Filtering**: Discovers books loved by users with similar tastes
- **📖 Content-Based Filtering**: Finds books with similar characteristics (title, author, features)

The system features an elegant dark-themed interface with a curated homepage showcasing top-rated books and an intuitive search interface for generating recommendations.

---

## ✨ Key Features

- 🏠 **Beautiful Homepage**: Displays the top 50 most popular and highest-rated books with cover images
- 🔍 **Smart Search**: Find books by title or author using partial or exact matching
- 🤖 **Dual Recommendation Engines**: Switch between collaborative and content-based algorithms
- 🎨 **Modern Dark UI**: Responsive design with smooth animations and gradient backgrounds
- ⭐ **Rich Metadata**: View ratings, number of votes, authors, and cover images
- 📱 **Fully Responsive**: Optimized for desktop, tablet, and mobile devices

---

## 📁 Project Structure

```
Book_Recommendation_System_AI_project/
├── 📄 README.md                         # This file
├── 📄 requirements.txt                  # Python dependencies
├── 📄 config.py                         # Application configuration
├── 🚀 run.py                            # Application entry point
│
├── 📁 src/                              # Source code
│   ├── __init__.py                      # Package initialization
│   └── app.py                           # Flask application
│
├── 📁 app/                              # Flask application assets
│   ├── templates/                       # HTML templates
│   │   ├── Book_recommend.html          # Homepage (top books)
│   │   └── Recommend.html               # Search & recommendations
│   └── static/                          # Static files
│       ├── css/                         # Stylesheets
│       ├── js/                          # JavaScript files
│       └── images/                      # Images
│
├── 📁 data/                             # Data directory
│   ├── raw/                             # Raw data files
│   │   ├── Ratings.csv                  # User ratings
│   │   ├── Users.csv                    # User data
│   │   └── Books.zip                    # Book metadata
│   └── processed/                       # Processed models
│       ├── popular.pkl                  # Top books data
│       ├── pt.pkl                       # Pivot table (collab filtering)
│       ├── books.pkl                    # Book metadata
│       ├── books_unique.pkl             # Unique books
│       ├── similarity_scores.pkl        # Collaborative similarity
│       ├── content_similarity.pkl       # Content-based similarity
│       └── content_book_index.pkl       # Book index mapping
│
└── 📁 notebooks/                        # Jupyter notebooks
    └── book-recommender-system.ipynb    # Data preprocessing
```

---

## 🔧 Prerequisites

- **Python 3.9+** (tested on Ubuntu 20.04 LTS and later)
- **pip** (Python package installer)
- **Git** (optional, for cloning)

---

## ⚙️ Quick Start

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd Book_Recommendation_System_AI_project
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python run.py
```

The app will start on:
```
🌐 http://127.0.0.1:5000/
```

**Optional:** Run on a different port:
```bash
python run.py --port 8000
```

---

## 📦 Dependencies

The application requires:

| Package | Version | Purpose |
|---------|---------|---------|
| **Flask** | ≥2.3 | Web framework |
| **NumPy** | ≥1.24 | Numerical computing |
| **Pandas** | ≥2.0 | Data manipulation |
| **scikit-learn** | ≥1.3 | ML utilities |
| **gunicorn** | ≥21.0 | WSGI server (production) |

---

## 🎮 Usage Guide

### 🏠 Homepage (`/`)
- Displays top 50 rated books with cover images
- Shows title, author, rating, and vote count
- Click "Get Recommendations" to start searching

### 🔍 Recommendation Page (`/recommend`)

1. **Enter Search Term**
   - Book title (e.g., "The Great Gatsby")
   - Author name (e.g., "J.K. Rowling")
   - Partial matches work too!

2. **Choose Algorithm**
   - 👥 **Collaborative Filtering**: Find books rated by similar users
   - 📖 **Content-Based**: Find books with similar titles and authors

3. **View Results**
   - Up to 6 recommendations with cover images
   - Navigate back to search again

---

## 🏗️ Architecture

### Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Homepage with top 50 books |
| `/recommend` | GET | Recommendation search form |
| `/Recommend_Books` | POST | Process search & return recommendations |

### Recommendation Algorithms

#### 👥 Collaborative Filtering
- **How it works**: Uses user-item rating matrix to find similar books
- **Best for**: Popular and trending books
- **Data**: Historical user ratings and preferences

#### 📖 Content-Based
- **How it works**: Analyzes book titles, authors, and characteristics
- **Best for**: Niche books and new additions
- **Data**: Book metadata and features

---

## 📊 Data Files

### Raw Data (`data/raw/`)
- `Ratings.csv` - User-book rating pairs (1M+ records)
- `Users.csv` - User information
- `Books.zip` - Complete book metadata

### Processed Models (`data/processed/`)

| File | Size | Purpose |
|------|------|---------|
| `popular.pkl` | ~7KB | Top 50 popular books |
| `books.pkl` | ~300MB | Full book metadata |
| `books_unique.pkl` | ~200KB | Unique books dataset |
| `pt.pkl` | ~4.6MB | Pivot table for collaborative filtering |
| `similarity_scores.pkl` | ~4MB | Collaborative similarity matrix |
| `content_similarity.pkl` | ~4MB | Content-based similarity matrix |
| `content_book_index.pkl` | ~20KB | Title to index mapping |

**Note:** Generate these files from `notebooks/book-recommender-system.ipynb`

---

## 🚀 Running in Production

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 'src.app:app'
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "src.app:app"]
```

Build and run:

```bash
docker build -t book-recommender .
docker run -p 8000:8000 book-recommender
```

---

## 🐛 Troubleshooting

### 📌 Models Not Found
```
FileNotFoundError: Model file not found
```
**Solution:** Ensure pickle files are in `data/processed/` directory

### 📌 Templates Not Found
```
jinja2.exceptions.TemplateNotFound
```
**Solution:** Check that templates are in `app/templates/` directory

### 📌 Import Errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Activate virtual environment and run `pip install -r requirements.txt`

### 📌 Port Already in Use
```
OSError: [Errno 48] Address already in use
```
**Solution:** 
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process or use a different port
python run.py --port 8000
```

---

## 📈 Performance Tips

- **First Load**: May take a few seconds (loading pickle files into memory)
- **Search Speed**: Optimized with exact-match lookup before partial matching
- **Recommendations**: Generated in <100ms for most queries
- **Caching**: Consider Redis for frequently accessed data in production

---

## 🔒 Security Notes

✅ **Current Implementation:**
- Input validation on search terms
- Safe template rendering with Jinja2

⚠️ **Production Recommendations:**
- Enable HTTPS/SSL configuration
- Add CSRF protection
- Implement rate limiting
- Use environment variables for secrets
- Set `DEBUG = False` in production

---

## 🚀 Future Enhancements

- [ ] User authentication and accounts
- [ ] Personalized recommendation history
- [ ] Pagination for large result sets
- [ ] Advanced filtering (genre, year, etc.)
- [ ] Rating system integration
- [ ] Social sharing features
- [ ] Full Docker containerization
- [ ] PostgreSQL database backend
- [ ] REST API endpoints
- [ ] Mobile app

---

## 📚 Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

```bash
# Format code
black src/ app/

# Lint code
pylint src/ app/
```

### Generating Models

```bash
# Open Jupyter notebook
jupyter notebook notebooks/book-recommender-system.ipynb

# Run all cells to generate pickle files
```

---

## 📝 Dataset Information

**Data Sources:**
- Book ratings from multiple users
- User demographic information
- Book metadata and cover images

**Statistics:**
- ~1M+ books in database
- ~100K+ users
- ~1M+ ratings

---

## 📄 License

This project is open source. Check LICENSE file for details.

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review `notebooks/book-recommender-system.ipynb` for data processing details

---

## 🙏 Acknowledgments

Built with:
- **Flask** - Web framework
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation
- **scikit-learn** - Machine learning
- **Bootstrap** - UI framework

**Happy Reading! 📖✨**
