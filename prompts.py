from imports import *

def create_combined_prompt(similar_resumes, original_query):
    """
    Combine the context of similar resumes with the original query to create a new prompt.

    Args:
    - similar_resumes (list[str]): Texts of similar resumes.
    - original_query (str): The original query that needs to be answered based on the resume context.

    Returns:
    - str: A combined prompt that includes the context and the original query.
    """
    # Combine the texts of the similar resumes
    context = "\n\n".join(similar_resumes)
    # Create the combined prompt
    combined_prompt = f"Based on the following resumes:\n\n ! EXAMPLE RESUMES BEGINS ! {context} ! EXAMPLE RESUMES END ! \n\n{original_query}"
    return combined_prompt

def query_with_context(combined_prompt, index, top_k = 2):
    """
    Query the engine with a combined prompt that includes context and the original query.

    Args:
    - combined_prompt (str): The combined prompt.

    Returns:
    - str: The response from the query engine.
    """
    # Query the engine
    query_engine = index.as_query_engine(similarity_top_k = top_k)
    response = query_engine.query(combined_prompt)
    return response


SYSTEM_PROMPT = "You are a smart assistant to career advisors at the Indian Institute of Technology Guwahati. You will reply with JSON only."

CV_TEXT_PLACEHOLDER = "<CV_TEXT>"

SYSTEM_TAILORING = """
You are a smart assistant to career advisors at the Indian Institute of Technology Guwahati. Your take is to rewrite
resumes to be more brief and convincing according to the Resumes and Cover Letters guide.
"""

TAILORING_PROMPT = """
Consider the following CV:
<CV_TEXT>

Your task is to rewrite the given CV. Follow these guidelines:
- Be truthful and objective to the experience listed in the CV
- Be specific rather than general
- Rewrite job highlight items using STAR methodology (but do not mention STAR explicitly)
- Fix spelling and grammar errors
- Writte to express not impress
- Articulate and don't be flowery
- Prefer active voice over passive voice
- Do not include a summary about the candidate

Improved CV:
"""

BASICS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface Basics {
    name: string;
    email: string;
    rollno: string;
    degree: string;
    phone: string;
    iitg id: string;
    github: string;
    linkedin: string;
}

Write the basics section according to the Basic schema. On the response, include only the JSON.
"""


EDUCATION_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface EducationItem {
    degree: string;
    institute: string;
    CGPA: string[];
    Year: string;
    ongoing: bool;
}

interface Education {
    education: EducationItem[];
}


Write the education section according to the Education schema. On the response, include only the JSON.
"""

AWARDS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface AwardItem {
    title: string;
    year: string;
    summary: string;
}

interface Awards {
    awards: AwardItem[];
}

Write the awards section according to the Awards schema. Include only the awards section. On the response, include only the JSON.
"""

PROJECTS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface ProjectItem {
    name: string;
    startdate: string;
    enddate: string;
    type: string;
    url: string;
    description: string;
}

interface Projects {
    projects: ProjectItem[];
}

Write the projects section according to the Projects schema. Include all projects, but only the ones present in the CV. On the response, include only the JSON.
"""


SKILLS_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

type HardSkills = "Programming Languages" | "Tools" | "Frameworks" | "Computer Proficiency";
type SoftSkills = "Team Work" | "Communication" | "Leadership" | "Problem Solving" | "Creativity";
type OtherSkills = string;

Now consider the following TypeScript Interface for the JSON schema:

interface SkillItem {
    name: HardSkills | SoftSkills | OtherSkills;
    keywords: string[];
}

interface Skills {
    skills: SkillItem[];
}

Write the skills section according to the Skills schema. Include only up to the top 4 skill names that are present in the CV and related with the education and work experience. On the response, include only the JSON.
"""

WORK_PROMPT = """
You are going to write a JSON resume section for an applicant applying for job posts.

Consider the following CV:
<CV_TEXT>

Now consider the following TypeScript Interface for the JSON schema:

interface WorkItem {
    company: string;
    position: string;
    startDate: string;
    endDate: string;
    location: string;
    highlights: string[];
}

interface Work {
    work: WorkItem[];
}

Write a work section for the candidate according to the Work schema. Include only the work experience and not the project experience. For each work experience, provide  a company name, position name, start and end date, and bullet point for the highlights. Follow the Harvard Extension School Resume guidelines and phrase the highlights with the STAR methodology
"""


def generate_json_resume(cv_text, api_key, model):
    """Generate a JSON resume from a CV text"""
    sections = []
    client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])

    for prompt in stqdm(
        [
            BASICS_PROMPT,
            EDUCATION_PROMPT,
            AWARDS_PROMPT,
            PROJECTS_PROMPT,
            SKILLS_PROMPT,
            WORK_PROMPT,
        ],
        desc="This may take a while...",
    ):
        
        
        filled_prompt = prompt.replace(CV_TEXT_PLACEHOLDER, cv_text)
        response = client.messages.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": filled_prompt},
            ],
        )

        try:
            answer = response.choices[0].message.content
            answer = json.loads(answer)

            if prompt == BASICS_PROMPT and "basics" not in answer:
                answer = {"basics": answer}  # common mistake GPT makes

            sections.append(answer)
        except Exception as e:
            print(e)

    final_json = {}
    for section in sections:
        final_json.update(section)

    return final_json


def tailor_resume(cv_text, api_key, model):
    filled_prompt = TAILORING_PROMPT.replace("<CV_TEXT>", cv_text)
    client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])

    try:
        response = client.messages.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_TAILORING},
                {"role": "user", "content": filled_prompt},
            ],
        )

        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(e)
        print("Failed to tailor resume.")
        return cv_text