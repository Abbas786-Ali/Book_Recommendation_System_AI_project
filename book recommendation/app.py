from flask import Flask, render_template, request
import numpy as np
import pickle
import os

popular_df = pickle.load(open('popular.pkl','rb'))
pt= pickle.load(open('pt.pkl','rb'))
books= pickle.load(open('books.pkl','rb'))
similarity_scores= pickle.load(open('similarity_scores.pkl','rb'))

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
    user_input=request.form.get('user_input')
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:7]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    print(data)
    return render_template('Recommend.html',data=data)


if __name__ == '__main__':
    app.run(debug=True)



