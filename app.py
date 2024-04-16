from imports import *
from read_data import *
from create_vector_store import *
from llm import *
# Initialize the chatbot API adapter
# chatbot = HuggingFaceAPIAdapter()
chatbot = anthropic_llm
def add_custom_css():
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
        }
        .text-bold {
            font-weight: bold;
        }
        .reportview-container .main .block-container{
            padding-top: 5rem;
            padding-bottom: 5rem;
        }
        .sidebar .sidebar-content {
            background-color: white;
        }
        .stButton>button {
            width: 100%;
            border-radius: 25px;
            border: 1px solid #f63366;
            color: #f63366;
        }
        .stButton>button:hover {
            border: 1px solid #f63366;
            background-color: #f63366;
            color: white;
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
        }
        .stTextArea>div>div>textarea {
            border-radius: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def chatbot_page():
    add_custom_css()
    st.title("Resume Chatbot Assistant")
    st.write("Please describe the changes you would like to make to the resume template:")

    context = "Your current resume draft includes your name, experience in software engineering over the last 5 years, including Python and Java development. What changes would you like to make?"
    user_input = st.text_area("Enter your request:", height=150, help="Describe any specific modifications or additions you need.")
    
    if st.button("Submit"):
        if user_input:
            # Call to the HuggingFace API adapter to get response
            response = chatbot.complete(prompt=user_input, context=context)
            st.write("Chatbot response:")
            st.write(response.text)
        else:
            st.error("Please enter some text to describe your changes.")

# Function to create the Form Input page
def form_page():
    add_custom_css()
    st.title("Professional Resume Builder")
    st.write("Provide your details below to create a custom resume tailored to your career goals.")
    
    with st.form("resume_form", clear_on_submit=True):
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        with cols[1]:
            linkedin = st.text_input("LinkedIn")
            github = st.text_input("GitHub")
            website = st.text_input("Personal Website")

        st.text_area("Professional Summary", help="Write a brief introduction about yourself.")
        st.text_area("Work Experience", help="Detail your professional experience.")
        st.text_area("Education", help="List your educational background.")
        st.text_area("Skills", help="Include relevant skills.")
        st.text_area("Certifications", help="Mention any certifications.")

        submitted = st.form_submit_button("Generate Resume")
        if submitted:
            st.balloons()
            st.success("Your custom resume is being generated...")

# Function to create the Template Selection page
def template_page():
    add_custom_css()
    st.title("Resume Template Gallery")
    st.write("Select from our curated range of resume templates to best showcase your professional background.")

    templates = {
        "Modern": "https://source.unsplash.com/random/300×300/?resume,modern",
        "Professional": "https://source.unsplash.com/random/300×300/?resume,professional",
        "Creative": "https://source.unsplash.com/random/300×300/?resume,creative"
    }

    cols = st.columns(3)
    for idx, (key, url) in enumerate(templates.items()):
        with cols[idx]:
            st.image(url, caption=f"{key} Style")
            if st.button(f"Select {key}", key=f"btn{idx}"):
                st.success(f"You have selected the {key} resume template!")

# Main function to handle navigation and page rendering
def main():
    st.sidebar.title("Resume Generator")
    page = st.sidebar.radio("Navigate to", ["Chatbot", "Fill Details", "Select Template"])

    if page == "Chatbot":
        chatbot_page()
    elif page == "Fill Details":
        form_page()
    elif page == "Select Template":
        template_page()

if __name__ == "__main__":
    main()