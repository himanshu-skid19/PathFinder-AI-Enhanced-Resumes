from imports import *
from create_vector_store import *
from llm import *
from read_data import *


def main():
    # Set up the title for the webpage
    st.title('Streamlit Example App')
    
    # llm_adapter = HuggingFaceAPIAdapter()
    
    Settings.llm = anthropic_llm
    # Check if the vector store exists and load it
    if check_vector_store_exists():
        st.write("Loading vector store...")
        index = load_vector_store()
        st.write("Vector store loaded successfully.")
    else:
        create_vector_store("resumes")
    # Create a text box for user input
    user_input = st.text_input("Enter your search query:")

    # Button to trigger the search
    if st.button("Search"):
        if user_input and 'index' in locals():
            # Querying the vector store
            results = query_vector_store(index, "Projects", user_input, top_k=2)
            if results:
                st.write("Top matches:")
                for result in results:
                    st.write(result)
            else:
                st.write("No matches found.")
        else:
            st.write("Please enter a valid query to search.")


if __name__ == '__main__':
    main()