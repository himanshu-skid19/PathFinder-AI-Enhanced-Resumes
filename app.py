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

def add_education_entry():
    # This function adds an empty dictionary to the list of education entries in the session state
    if 'education_entries' not in st.session_state:
        st.session_state.education_entries = []
    st.session_state.education_entries.append({'degree': '', 'institute': '', 'cgpa': '', 'year': ''})

def education_form(idx, entry):
    with st.container():
        entry['degree'] = st.text_input(f"Degree {idx + 1}", value=entry.get('degree', ''), key=f"degree_{idx}")
        entry['institute'] = st.text_input(f"Institute/Board {idx + 1}", value=entry.get('institute', ''), key=f"institute_{idx}")
        entry['cgpa'] = st.text_input(f"CGPA/Percentage {idx + 1}", value=entry.get('cgpa', ''), key=f"cgpa_{idx}")
        entry['year'] = st.text_input(f"Year {idx + 1}", value=entry.get('year', ''), key=f"year_{idx}")

def add_project_entry():
    # This function adds an empty dictionary to the list of project entries in the session state
    if 'project_entries' not in st.session_state:
        st.session_state.project_entries = []
    st.session_state.project_entries.append({'name': '', 'duration': '', 'organisation': '', 'description': ''})

def project_form(idx, entry):
    with st.container():
        entry['name'] = st.text_input(f"Project Name {idx + 1}", value=entry.get('name', ''), key=f"project_name_{idx}")
        entry['duration'] = st.text_input(f"Duration {idx + 1}", value=entry.get('duration', ''), key=f"project_duration_{idx}")
        entry['organisation'] = st.text_input(f"Organisation {idx + 1}", value=entry.get('organisation', ''), key=f"project_organisation_{idx}")
        entry['description'] = st.text_area(f"Project Description {idx + 1}", value=entry.get('description', ''), key=f"project_description_{idx}")

def add_experience_entry():
    # This function adds an empty dictionary to the list of experience entries in the session state
    if 'experience_entries' not in st.session_state:
        st.session_state.experience_entries = []
    st.session_state.experience_entries.append({'type': '', 'company': '', 'role': '', 'description': ''})

def experience_form(idx, entry):
    with st.container():
        entry['type'] = st.selectbox(f"Type of Experience {idx + 1}", ['Work', 'Internship', 'Research', 'Volunteer'], key=f"type_{idx}")
        entry['company'] = st.text_input(f"Company/University {idx + 1}", value=entry.get('company', ''), key=f"company_{idx}")
        entry['role'] = st.text_input(f"Role {idx + 1}", value=entry.get('role', ''), key=f"role_{idx}")
        entry['description'] = st.text_area(f"Description {idx + 1}", value=entry.get('description', ''), key=f"description_{idx}")

def add_skill_entry():
    # This function adds an empty dictionary to the list of skill entries in the session state
    if 'skill_entries' not in st.session_state:
        st.session_state.skill_entries = []
    st.session_state.skill_entries.append({'skill_type': '', 'skills': ''})

def skill_form(idx, entry):
    with st.container():
        entry['skill_type'] = st.text_input(f"Skill Type {idx + 1}", value=entry.get('skill_type', ''), key=f"skill_type_{idx}")
        entry['skills'] = st.text_input(f"Skills in {entry['skill_type']}", value=entry.get('skills', ''), placeholder="Enter skills separated by commas", key=f"skills_{idx}")

def add_achievement_entry():
    if 'achievement_entries' not in st.session_state:
        st.session_state.achievement_entries = []
    st.session_state.achievement_entries.append({'achievement': '', 'year': datetime.date.today().year})

def achievement_form(idx, entry):
    with st.container():
        entry['achievement'] = st.text_area(f"Achievement {idx + 1}", value=entry.get('achievement', ''), key=f"achievement_{idx}", help="Describe your achievement.")
        default_year = entry.get('year', datetime.date.today().year)
        entry['year'] = st.number_input(f"Year {idx + 1}", min_value=1900, max_value=2999, value=default_year, key=f"achievement_year_{idx}", help="Enter the year of the achievement.")

# Function to create the Form Input page
def form_page():
    add_custom_css()
    st.title("Professional Resume Builder")
    st.write("Provide your details below to create a custom resume tailored to your career goals.")
    
    # Manage education entries outside of the form
    st.markdown("### Education")
    # Show existing education entries
    for idx, entry in enumerate(st.session_state.get('education_entries', [])):
        education_form(idx, entry)
    # Button to add new education entry
    st.button("Add Education Entry", on_click=add_education_entry)

    st.markdown("### Work Experience")
    #Show existing experience entries
    for idx, entry in enumerate(st.session_state.get('experience_entries', [])):
        experience_form(idx, entry)
    st.button("Add Experience Entry", on_click=add_experience_entry)

 
    # Manage project entries outside of the form
    st.markdown("### Projects")
    # Show existing project entries
    for idx, entry in enumerate(st.session_state.get('project_entries', [])):
        project_form(idx, entry)
    st.button("Add Project Entry", on_click=add_project_entry)

    st.markdown("### Skills")
    # Show existing skill entries
    for idx, entry in enumerate(st.session_state.get('skill_entries', [])):
        skill_form(idx, entry)
    st.button("Add Skill Entry", on_click=add_skill_entry)

     # Manage achievement entries outside of the form
    st.markdown("### Achievements")
    # Show existing achievement entries
    for idx, entry in enumerate(st.session_state.get('achievement_entries', [])):
        achievement_form(idx, entry)
    st.button("Add Achievement Entry", on_click=add_achievement_entry)

    # The main form for other details
    with st.form("resume_form"):
        # Personal Information Section
        cols = st.columns(2)
        with cols[0]:
            name = st.text_input("Name", key="name")
            email = st.text_input("Email", key="email")
            phone = st.text_input("Phone", key="phone")
        with cols[1]:
            linkedin = st.text_input("LinkedIn", key="linkedin")
            github = st.text_input("GitHub", key="github")
            website = st.text_input("Personal Website", key="website")
        
        # Additional Details Sections
        
        # Submit button for the form
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