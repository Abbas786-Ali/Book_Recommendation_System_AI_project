# Book Recommendation System Config

DEBUG = True
TESTING = False

# Flask session config
SECRET_KEY = 'dev-secret-key-change-in-production'
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# Application config
MAX_RECOMMENDATIONS = 6
POPULAR_BOOKS_COUNT = 50
