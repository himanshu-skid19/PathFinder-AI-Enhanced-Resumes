from imports import *
from read_data import *
from create_vector_store import *
from llm import *
from prompts import *
# Initialize the chatbot API adapter
# chatbot = HuggingFaceAPIAdapter()

chatbot = anthropic_llm
def add_custom_css():
    st.markdown("""
        <style>
        .chat-message {
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        .user-message {
            
            text-align: left;
        }
        .bot-message {
            text-align: left;
        }
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

def display_chat():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Create a visually distinct section for chat history
    with st.container():
        for message in st.session_state.messages:
            if message['sender'] == 'user':
                st.markdown(f"**USER**: {message['text']}", unsafe_allow_html=True)
            elif message['sender'] == 'bot':
                st.markdown(f"**BOT**: ", unsafe_allow_html=True)
                st.json(message["text"])


def chatbot_page():
    add_custom_css()
    st.title("Resume Chatbot Assistant")

    # Check if there's existing context in the session
    if 'context' not in st.session_state:
        st.session_state.context = "Your current resume draft includes your name, experience in software engineering over the last 5 years, including Python and Java development. What changes would you like to make?"


    # Dropdown to select the model
    model = ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]
    selected_model = st.sidebar.selectbox("Choose the model to use:", model)
    st.sidebar.write(f"You have selected the {selected_model} model.")

    if selected_model.startswith("claude"):
        api_key = st.sidebar.text_input("Enter your API Key here:", type="password")
        os.environ["ANTHROPIC_API_KEY"] = api_key
    
    elif selected_model == "gemma-7b":
        api_key = st.sidebar.text_input("Enter your API Key here:", type="password")
        os.environ["HF_TOKEN"] = api_key

    # Option to input resume text directly
    resume_text = st.sidebar.text_area("Enter your resume text here:", height=300)
    if resume_text:
        st.session_state.resume_text = resume_text
        persist_dir = "./storage"
        if check_vector_store_exists(persist_dir):
            print("Loading existing vector store...")
            index = load_vector_store(persist_dir)
            st.session_state.retrieval = index

        else:
            print("Creating new vector store...")
            directory_path = "resumes"  # Path where your PDFs/documents are stored
            index = create_vector_store(directory_path)
            print("Vector store created.")
            st.session_state.retrieval = index
        st.sidebar.success("Text input received!")

    
    
    st.write("Please describe the changes you would like to make")
    display_chat()
    if 'examples' not in st.session_state and "retrieval" in st.session_state:
        st.session_state.examples= query_vector_store(st.session_state.retrieval)
    # Input for text modifications
    user_input = st.text_input("Enter your request:", help="Describe any specific modifications or additions you need.", key="user_input")
    
    submit_button = st.button("Submit")
    if submit_button and user_input:
        # Simulate adding user message to the chat
        st.session_state.messages.append({"sender": "user", "text": user_input})

        if len(st.session_state.messages) == 1:
            response = tailor_resume_anthropic(str(st.session_state.resume_text), str(user_input), selected_model, st.session_state.examples)
        else:
            print("last message in chat: ")
            print(str(st.session_state.messages[-2]))
            response = tailor_resume_anthropic(str(st.session_state.messages[-2]), str(user_input), selected_model, st.session_state.examples)
        
        final_response = response.content[0].text
        
        # Simulated response from the chatbot based on selected model
        st.session_state.messages.append({"sender": "bot", "text": final_response})

        # Output the chatbot response
        st.write("Chatbot response:")
        st.json(final_response)
        print(final_response)
        
        # Clear the input box after showing the response by using a short delay and rerunning the script
        st.experimental_rerun()
    elif submit_button:
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
        entry['start_year'] = st.text_input(f"Start Year {idx + 1}", value=entry.get('start_year', ''), key=f"edu_start_year_{idx}")
        entry['end_year'] = st.text_input(f"End Year {idx + 1}", value=entry.get('end_year', ''), key=f"edu_end_year_{idx}")

def add_project_entry():
    # This function adds an empty dictionary to the list of project entries in the session state
    if 'project_entries' not in st.session_state:
        st.session_state.project_entries = []
    st.session_state.project_entries.append({'name': '', 'duration': '', 'organisation': '', 'description': ''})

def project_form(idx, entry):
    with st.container():
        entry['name'] = st.text_input(f"Project Name {idx + 1}", value=entry.get('name', ''), key=f"project_name_{idx}")
        entry['start_date'] = st.text_input(f"Project Start Date (e.g., Mar 2020) {idx + 1}", value=entry.get('start_date', ''), key=f"proj_start_date_{idx}")
        entry['end_date'] = st.text_input(f"Project End Date or 'Present' {idx + 1}", value=entry.get('end_date', ''), key=f"proj_end_date_{idx}")
        entry['organisation'] = st.text_input(f"Organisation {idx + 1}", value=entry.get('organisation', ''), key=f"project_organisation_{idx}")
        entry['description'] = st.text_area(f"Project Description {idx + 1}", value=entry.get('description', ''), key=f"project_description_{idx}")
        entry['github_link'] = st.text_input(f"GitHub Link {idx + 1}", value=entry.get('github_link', ''), key=f"project_github_link_{idx}")

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
        entry['location'] = st.text_input(f"Location {idx + 1}", value=entry.get('location', ''), key=f"location_{idx}")  # New location input
        entry['start_date'] = st.text_input(f"Start Date (e.g., Mar 2020) {idx + 1}", value=entry.get('start_date', ''), key=f"start_date_{idx}")
        entry['end_date'] = st.text_input(f"End Date or 'Present' {idx + 1}", value=entry.get('end_date', ''), key=f"end_date_{idx}")
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
        entry['company'] = st.text_input(f"Company/Organisation {idx + 1}", value=entry.get('company', ''), key=f"achievement_company_{idx}", help="Enter the name of the company or organisation associated with the achievement.")
        default_year = entry.get('year', datetime.date.today().year)
        entry['year'] = st.number_input(f"Year {idx + 1}", min_value=1900, max_value=2999, value=default_year, key=f"achievement_year_{idx}", help="Enter the year of the achievement.")

def format_experiences(experiences):
    experiences_str = "\\section{Experience}\n"  # Changed from \section* to \section for consistency with your template
    experiences_str += "\\resumeSubHeadingListStart\n"

    for exp in experiences:
        company = exp['company'].replace('&', '\\&')
        role = exp['role'].replace('&', '\\&')
        start_date = exp['start_date'].replace('&', '\\&')
        end_date = exp['end_date'].replace('&', '\\&')
        location = exp['location'].replace('&', '\&')
        duration = f"{start_date} - {end_date}"
        description = exp['description'].replace('&', '\\&').replace('\n', ' ').strip()

        # Begin subheading for the experience
        experiences_str += "\\resumeSubheading\n"
        experiences_str += f"{{ {company} }}{{ {duration} }}\n"
        experiences_str += f"{{ {role} }}{{{location}}}\n"  # Empty braces for the second argument as per your template
        experiences_str += "\\resumeItemListStart\n"
        
        # If the description contains multiple items separated by a specific character (e.g., semicolon),
        # you can split them into multiple items. Otherwise, add it as a single item.
        if ';' in description:
            for item in description.split(';'):
                experiences_str += f"\\item {{{item.strip()}}}\n"
        else:
            experiences_str += f"\\item {{{description}}}\n"

        # End the list of items for the current experience
        experiences_str += "\\resumeItemListEnd\n"
        
    # End the list of experiences
    experiences_str += "\\resumeSubHeadingListEnd\n"
    experiences_str += "\\vspace{-5.5mm}\n"  # Adjust spacing as needed

    return experiences_str

def format_education(education_entries):
    # Header part of the education section with bold title
    education_str = "\\section*{\\large\\textbf{EDUCATION}}\n"
    # Start the tabularx environment, specify the total width (e.g., \textwidth), and define the columns
    education_str += "\\begin{tabularx}{\\textwidth}{|X|X|X|X|}\n"
    # Add the horizontal line at the top of the table and column headers
    education_str += "\\hline\n"
    education_str += "\\textbf{Degree/Certificate} & \\textbf{Institute/Board} & \\textbf{CGPA/Percentage} & \\textbf{Years} \\\\\n"
    education_str += "\\hline\n"
    # Iterate over each education entry and create a row in the table for each
    for edu in education_entries:
        institute = edu["institute"].replace('&', '\\&')
        degree = edu["degree"].replace('&', '\\&')
        cgpa = edu["cgpa"]
        start_year = edu["start_year"]  # Assuming you have start_year and end_year in your entry
        end_year = edu["end_year"]  # Can be 'Present' or a specific year
        years = f"{start_year} - {end_year}"
        # Add each row of education details
        education_str += f"{degree} & {institute} & {cgpa} & {years} \\\\\n"
        education_str += "\\hline\n"  # Add horizontal line after each row
    # End the tabularx environment
    education_str += "\\end{tabularx}\n"
    return education_str

def format_projects(projects):
    projects_str=f"\\section{{Projects}}"
    projects_str += '\\resumeSubHeadingListStart\n'
    for proj in projects:
        name = proj['name'].replace('&', '\\&')
        start_date = proj['start_date'].replace('&', '\\&')
        end_date = proj['end_date'].replace('&', '\\&')
        duration = f"{start_date} - {end_date}"
        organisation = proj['organisation'].replace('&', '\\&')
        description = proj['description'].replace('&', '\\&')
        github=proj['github_link']
        if name and start_date and end_date and duration and organisation and description and github: 
                projects_str += f"\\resumeSubheading{{{name}}}{{{duration}}}{{{organisation}}}\n" \
                            f"{{\\href{{{github}}}{{Github}}}}{{{description}}}\n" \
                       
    projects_str += '\\resumeSubHeadingListEnd\n'
    return projects_str

def format_achievements(achievements):
    achievements_str=f"\\section{{Achievements}}"
    achievements_str += '\\resumeSubHeadingListStart\n'
    for ach in achievements:
        achievement = ach['achievement'].replace('&', '\\&')
        year = ach['year']
        company= ach['company']
        if achievement and year and company:
            achievements_str += f"\\resumePOR{{{achievement}}}{{{company}}}{{{year}}}\n"
    achievements_str += '\\resumeSubHeadingListEnd\n'
    return achievements_str

def format_skills(skills):
    skills_str = "\\section{Skills}\n\\begin{itemize}\n"
    for skill in skills:
        skill_type = skill['skill_type'].replace('&', '\\&').strip()
        skills_list = skill['skills'].replace('&', '\\&').strip()
        
        # Split the skills_list by commas and remove empty strings
        skills_list = [s.strip() for s in skills_list.split(',') if s.strip()]
        
        # Check if both skill_type and skills_list are not empty
        if skill_type and skills_list:
            skills_str += "\\item \\textbf{" + skill_type + ":} "
            skills_str += ", ".join(skills_list) + "\n"
    skills_str += "\\end{itemize}\n"
    return skills_str

def create_pdf(data, experiences, educationEntries, projects, achievements, skills):
    template_text = r"""
\documentclass[a4paper,11pt]{article}
\usepackage{latexsym}
\usepackage{xcolor}
\usepackage{float}
\usepackage{ragged2e}
\usepackage[empty]{fullpage}
\usepackage{wrapfig}
\usepackage{lipsum}
\usepackage{tabularx}
\usepackage{titlesec}
\usepackage{geometry}
\usepackage{marvosym}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage{multicol}
\usepackage{graphicx}
\usepackage{cfr-lm}
\usepackage[T1]{fontenc}
\setlength{\multicolsep}{0pt} 
\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\geometry{left=1.4cm, top=0.8cm, right=1.2cm, bottom=1cm}
% Adjust margins
%\addtolength{\oddsidemargin}{-0.5in}
%\addtolength{\evensidemargin}{-0.5in}
%\addtolength{\textwidth}{1in}
\usepackage[most]{tcolorbox}
\tcbset{
	frame code={}
	center title,
	left=0pt,
	right=0pt,
	top=0pt,
	bottom=0pt,
	colback=gray!20,
	colframe=white,
	width=\dimexpr\textwidth\relax,
	enlarge left by=-2mm,
	boxsep=4pt,
	arc=0pt,outer arc=0pt,
}

\newenvironment{educationtable}{
  \begin{tabular}{lllr}
  \toprule
  \textbf{Degree/Certificate} & \textbf{Institute/Board} & \textbf{CGPA/Percentage} & \textbf{Year} \\
  \midrule
}{ 
  \bottomrule
  \end{tabular}
}
\usepackage{booktabs} % For professional looking tables


\urlstyle{same}

\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-7pt}]

%-------------------------
% Custom commands
\newcommand{\resumeItem}[2]{
  \item{
    \textbf{#1}{:\hspace{0.5mm}#2 \vspace{-0.5mm}}
  }
}

\newcommand{\resumePOR}[3]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1},\hspace{0.3mm}#2 & \textit{\small{#3}} 
    \end{tabular*}
    \vspace{-2mm}
}

\newcommand{\resumeSubheading}[4]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1} & \textit{#2} \\
        \textit{#3} & {#4} \\
    \end{tabular*}
    \vspace{-2.4mm}
}

\newcommand{\resumeProject}[4]{
\vspace{0.5mm}\item
    \begin{tabular*}{0.98\textwidth}[t]{l@{\extracolsep{\fill}}r}
        \textbf{#1} & \textit{\footnotesize{#3}} \\
        \footnotesize{\textit{#2}} & \footnotesize{#4}
    \end{tabular*}
    \vspace{-2.4mm}
}
\newcommand{\resumeExperience}[5]{
  \item
    \textbf{#1} \hfill #4 \\
    \textit{#2} \hfill \textit{#5} \\
    #3
}


\newcommand{\resumeSubItem}[2]{\resumeItem{#1}{#2}\vspace{-4pt}}

% \renewcommand{\labelitemii}{$\circ$}
\renewcommand{\labelitemi}{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=*,labelsep=0mm]}
\newcommand{\resumeHeadingSkillStart}{\begin{itemize}[leftmargin=*,itemsep=1.7mm, rightmargin=2ex]}
\newcommand{\resumeItemListStart}{\begin{justify}\begin{itemize}[leftmargin=3ex, rightmargin=2ex, noitemsep,labelsep=1.2mm,itemsep=0mm]\small}

\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{2mm}}
\newcommand{\resumeHeadingSkillEnd}{\end{itemize}\vspace{-2mm}}
\newcommand{\resumeItemListEnd}{\end{itemize}\end{justify}\vspace{-2mm}}
\newcommand{\cvsection}[1]{%
\vspace{2mm}
\begin{tcolorbox}
    \textbf{\large #1}
\end{tcolorbox}
    \vspace{-4mm}
}

\newcolumntype{L}{>{\raggedright\arraybackslash}X}%
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}%
\newcolumntype{C}{>{\centering\arraybackslash}X}%
%---- End of Packages and Functions ------

%-------------------------------------------
%%%%%%  CV STARTS HERE  %%%%%%%%%%%
%%%%%% DEFINE ELEMENTS HERE %%%%%%%
\newcommand{\name}{{name}} % Your Name
\newcommand{\course}{{branch}} % Your Course
\newcommand{\roll}{{roll}} % Your Roll No.
\newcommand{\phone}{{phone}} % Your Phone Number
\newcommand{\email}{{email}} %Email 1
\newcommand{\github}{{github}}%Github
\newcommand{\website}{{website}} %Website
\newcommand{\linkedin}{{linked}} %linkedin




\begin{document}
\fontfamily{cmr}\selectfont
%----------HEADING-----------------
\parbox{2.35cm}{%

\includegraphics[width=2cm,clip]{iitg_logo.jpg}

}\parbox{\dimexpr\linewidth-2.8cm\relax}{
\begin{tabularx}{\linewidth}{L r}
  \textbf{\LARGE \name} & +91-\phone\\
  {Roll No.:\roll} & \href{mailto:\email}{\email} \\
  {branch} &  \href{https://github.com/\github}{Github} $|$ \href{\website}{Website}\\
  {Indian Institute Of Technology, Guwahati} & \href{https://www.linkedin.com/in/\linkedin/}{linkedin.com/in/\linkedin}
\end{tabularx}
}



%-----------EDUCATION-----------------
\setlength{\tabcolsep}{5pt} % Default
{% block education %}

%-----------EXPERIENCE-----------------
{% block experience %}

%-----------PROJECTS-----------------
{% block projects %}


%-----------TECHNICAL SKILLS-----------------
{% block technical_skills %}


%-----------ACHIEVEMENTS-----------------
{% block achievements %}



%-------------------------------------------
\end{document}


"""

    #experience_section = "\cvsection{Experience}\n\\resumeSubHeadingListStart\n"
    #for exp in experiences:
     #   experience_section += f"\\resumeSubheading{{{exp['company']}}}{{}}{{{exp['role']}}}{{{{{{exp['duration']}}}}}}\n\\resumeItemListStart\n\\resumeItem{{}} {{{exp['description']}}}\n\\resumeItemListEnd\n"
    
    # Placeholder for the education section
    #education_section = "\cvsection{Education}\n\\resumeSubHeadingListStart\n"
    #for edu in educationEntries:
     #   education_section += f"\\resumeSubheading{{{edu['institute']}}}{{}}{{{edu['degree']}}}{{{{{{edu['year']}}}}}}\n\\resumeItemListStart\n\\resumeItem{{CGPA}}{{{{edu['cgpa']}}}}\n\\resumeItemListEnd\n"

    # Closing the list
    #experience_section += "\\resumeSubHeadingListEnd\n"
    #education_section += "\\resumeSubHeadingListEnd\n"

    print("edu: ",educationEntries)
    print("exp: ",experiences)
    education_section = format_education(educationEntries) if educationEntries else ''
    experience_section = format_experiences(experiences) if experiences else ''
    projects_section = format_projects(projects) if projects else ''
    achievements_section = format_achievements(achievements) if achievements else ''
    skills_section = format_skills(skills) if skills else ''

    # Replace the placeholders in the template
    template_text = template_text.replace('{% block education %}', education_section)
    template_text = template_text.replace('{% block experience %}', experience_section)
    template_text = template_text.replace('{% block projects %}', projects_section)
    template_text = template_text.replace('{% block achievements %}', achievements_section)
    template_text = template_text.replace('{% block technical_skills %}', skills_section)

    print("edu str: ",education_section)
    print("exp str: ",experience_section)
    print("project str: ",projects_section)
    print("ach str: ",achievements_section)
    print("skills str: ",skills_section)

    #print(template_text)
    template_text=re.sub(r'{name}',data["name"],template_text)
    template_text=re.sub(r'{email}',data["email"],template_text)
    template_text=re.sub(r'{phone}',data["phone"],template_text)
    template_text=re.sub(r'{branch}',data["branch"],template_text)
    template_text=re.sub(r'{roll}',data["roll"],template_text)
    template_text=re.sub(r'{github}',data["github"],template_text)
    template_text=re.sub(r'{website}',data["website"],template_text)
    template_text=re.sub(r'{college}',data["college"],template_text)


    #template_text=re.sub(r'{}')

    with open('output.tex', 'w') as f:
        f.write(template_text)
    
    # os.system('pdflatex output.tex') # Compile LaTeX to PDF, ensure pdflatex is installed


# Function to create the Form Input page
def form_page():
    add_custom_css()
    st.title("Professional Resume Builder")
    st.write("Provide your details below to create a custom resume tailored to your career goals.")
    
    # Manage education entries outside of the form
    st.markdown("### Education ",help="Required (atleast 1)")
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
            sn = st.text_input("Name", key="name",help="Required")
            ph = st.text_input("Phone", key="phone",help="Required")
            rl= st.text_input("Roll No.",key="roll",help="Required")
            cn = st.text_input("Institute Name", key="college",help="Required")
            br=st.text_input("Branch Name",key="branch",help="Required")
        with cols[1]:
            email = st.text_input("Email", key="email",help="Required")
            linkedin = st.text_input("LinkedIn", key="linkedin")
            github = st.text_input("GitHub", key="github")
            website = st.text_input("Personal Website", key="website")


        
        # Additional Details Sections
        
        # Submit button for the form
        education_entries = st.session_state.get('education_entries', [])
        education_complete = all(entry.get('degree') and entry.get('institute') and entry.get('cgpa') and entry.get('start_year') and entry.get('end_year') for entry in education_entries)
        if len(education_entries) > 0:
            first_education_entry = education_entries[0]
            education_exists = all(value for value in first_education_entry.values())
        else:
            education_exists = False
        submitted = st.form_submit_button("Generate Resume")
        if submitted:
            if not sn or not email or not ph:
                st.error("Please fill out all required fields.")
            elif not education_entries or not education_complete:
                st.error("Please add at least one entry in the Education section.")
            else:
                st.balloons()
                data = {
                'name': sn,
                'email': email,
                'phone': ph,
                'linkedin': linkedin,
                'branch':br,
                'github':github,
                'website':website,
                'college':cn,
                'roll':rl
                }
                projects=st.session_state.get('project_entries',[])
                achievements=st.session_state.get('achievement_entries',[])
                skills=st.session_state.get('skill_entries',[])
                experiences = st.session_state.get('experience_entries', [])
                education_entries = st.session_state.get('education_entries', [])
                create_pdf(data, experiences, education_entries, projects, achievements, skills)
                st.success("Your custom resume is being generated...")


# Main function to handle navigation and page rendering
def main():
    st.sidebar.title("Resume Generator")
    page = st.sidebar.radio("Navigate to", ["Chatbot", "Fill Details"])



    if page == "Chatbot":
        chatbot_page()
    elif page == "Fill Details":
        form_page()


if __name__ == "__main__":
    main()