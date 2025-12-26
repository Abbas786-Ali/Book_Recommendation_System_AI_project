from flask import Flask, render_template, request
import numpy as np
import pickle
import os

popular_df = pickle.load(open('popular.pkl','rb'))
pt= pickle.load(open('pt.pkl','rb'))
books= pickle.load(open('books.pkl','rb'))
similarity_scores= pickle.load(open('similarity_scores.pkl','rb'))
books_unique = pickle.load(open('books_unique.pkl','rb'))


# Load content-based recommendation models
try:
    content_similarity = pickle.load(open('content_similarity.pkl','rb'))
    content_book_index = pickle.load(open('content_book_index.pkl','rb'))
    books_unique = pickle.load(open('books_unique.pkl','rb'))
except FileNotFoundError:
    print("Warning: Content-based models not found. Please run the notebook first.")

# Get the absolute path to the templates folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def home():
    # render the mypro.html template located in the templates/ folder
    return render_template('Book_recommend.html',
                        book_name=list(popular_df['Book-Title'].values),
                        author=list(popular_df['Book-Author'].values),
                        votes=list(popular_df['num_ratings'].values),
                        rating=list(popular_df['avg_rating'].values),
                        image=list(popular_df['Image-URL-M'].values)) 

@app.route('/recommend')
def recommend_ui():
    return render_template('Recommend.html')

@app.route('/Recommend_Books',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input', '').strip()
    recommendation_type = request.form.get('recommendation_type', 'collaborative')
    
    data = []
    found_book = None
    error_message = ""
    
    try:
        # Try to find exact book title match first
        if user_input in content_book_index:
            found_book = user_input
        else:
            # Try to find by partial book title or author match
            matching_books = books_unique[
                (books_unique['Book-Title'].str.contains(user_input, case=False, na=False)) |
                (books_unique['Book-Author'].str.contains(user_input, case=False, na=False))
            ]['Book-Title'].values
            
            if len(matching_books) > 0:
                found_book = matching_books[0]
        
        if found_book:
            if recommendation_type == 'content':
                # Content-based recommendation
                idx = content_book_index[found_book]
                sim_scores = list(enumerate(content_similarity[idx]))
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
                # Collaborative filtering recommendation
                if found_book in pt.index:
                    index = np.where(pt.index == found_book)[0][0]
                    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]
                    
                    for i in similar_items:
                        item = []
                        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                        
                        data.append(item)
                else:
                    error_message = f"Book '{found_book}' not found in collaborative filtering database."
        else:
            error_message = f"No books found matching '{user_input}'. Try searching by book title or author name."
    
    except Exception as e:
        print(f"Error: {e}")
        error_message = f"An error occurred: {str(e)}"
        data = []
    
    return render_template('Recommend.html', data=data, recommendation_type=recommendation_type, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)



