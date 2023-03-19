import streamlit as st
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pivot_table = pickle.load(open('pivot_table.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

def index():
    st.markdown("<h1 style='text-align: center;'>Book Recommender</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h2>Popular Books</h2>", unsafe_allow_html=True)
    for title, author, image, votes, rating in zip(popular_df['Book-Title'], popular_df['Book-Author'], popular_df['Image-URL-M'], popular_df['num_rating'], popular_df['avg_rating']):
        st.write(f"**{title}** by {author}")
        st.image(image, width=150)
        st.write(f"Votes: {votes}, Rating: {rating:.1f}")
        st.markdown("---")

def recommend_ui():
    st.markdown("<h2>Get Book Recommendations</h2>", unsafe_allow_html=True)
    user_input = st.text_input("Enter the name of a book you like:")
    if st.button("Recommend"):
        if user_input not in pivot_table.index:
            st.warning("Name not found. Please try again.")
        else:
            index_new = np.where(pivot_table.index==user_input)[0][0]
            similar_book_recommend = sorted(list(enumerate(similarity_score[index_new])),key=lambda x:x[1],reverse=True)[1:6]
            for items in similar_book_recommend:
                temp_df = books[books['Book-Title'] == pivot_table.index[items[0]]].drop_duplicates('Book-Title')
                title, author, image = temp_df['Book-Title'].values[0], temp_df['Book-Author'].values[0], temp_df['Image-URL-M'].values[0]
                st.write(f"**{title}** by {author}")
                st.image(image, width=150)
                st.markdown("---")

def main():
    menu = ["Home", "Recommend"]
    choice = st.sidebar.selectbox("Select an option", menu)
    if choice == "Home":
        index()
    elif choice == "Recommend":
        recommend_ui()

if __name__ == "__main__":
    main()