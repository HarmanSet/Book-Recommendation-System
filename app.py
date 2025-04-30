from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df=pickle.load(open('popular.pkl', 'rb'))
pt=pickle.load(open('pt.pkl', 'rb'))
all_books=pickle.load(open('books.pkl', 'rb'))
similarity_score=pickle.load(open('similarity_score.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    books = popular_df[['Book-Title', 'Book-Author_x', 'Image-URL-M_x', 'num_ratings', 'avg_rating']].to_dict(orient='records')
    return render_template('index.html', books=books)

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input=request.form.get('user_input')

    index= np.where(pt.index==user_input)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:21]

    data=[]
    for i in similar_items:
        item=[]
        temp_df=all_books[all_books['Book-Title']== pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    # print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)