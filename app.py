import streamlit as st

def main():
    # Set up the title for the webpage
    st.title('Streamlit Example App')

    # Create a text box for user input
    user_input = st.text_input("Enter your data:")

    # Display user input back on the page, or some operation based on it
    if user_input:
        # Example operation: reversing the input string
        reversed_input = user_input[::-1]
        # Displaying the processed output
        st.write(f"Reversed Input: {reversed_input}")

        # Example of simply displaying input, uncomment below line to use it
        # st.write(f"You entered: {user_input}")

# Run the app
if __name__ == '__main__':
    main()
