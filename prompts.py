from imports import *
from app import *
from create_vector_store import *

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


# SYSTEM_PROMPT = "You are a smart assistant to career advisors at the Indian Institute of Technology Guwahati. You will reply with JSON only."

CV_TEXT_PLACEHOLDER = "<CV_TEXT>"



SYSTEM_PROMPT = """
You are a smart assistant to career advisors at the Indian Institute of Technology Guwahati. Your take is to rewrite
resume content to be more brief and convincing according to the Resumes and Cover Letters guide.

Consider the following text from a cv:
<CV_TEXT>

Your task is to rewrite this based on the query provided by the user. You may follow these guidelines:
- Be truthful and objective to the experience listed in the CV
- Be specific rather than general
- Rewrite job highlight items using STAR methodology (but do not mention STAR explicitly)
- Fix spelling and grammar errors
- Writte to express not impress
- Articulate and don't be flowery
- Prefer active voice over passive voice
- Do not include a summary about the candidate
- give your output as json only

HERE ARE SOME EXAMPLES FOR YOUR REFERENCE
<RETRIEVED EXAMPLES>

ONLY GIVE THE JSON AS THE OUTPUT AND NOTHING ELSE
This is the last message that the user sent and output he/she got:
<HISTORY>
Make sure you give your output with this as the new context

"""

JSON_PROMPT = """
<QUERY>

Give your output in json format.

JSON_FORMAT EXAMPLE:
  {
    "project_name": "Devrev's AI Agent 007",
    "project_type": "Inter IIT Tech Meet 12.0",
    "start_date" : "Nov. 2023",
    "end_date" : "Dec. 2023",
    "project link" : "Github",
    "description" : [
      "Employed various innovative prompting techniques such as Few-Shot CoT, ReACT, and Decomposed Prompting
to enhance the language model’s interpretability and problem-solving capabilities.",
     "Explored and tested Self-Instruct methodologies for synthetic dataset creation",
     "Drawing on Named Entity Recognition, the novel method Automated Generation Using Tuned Entities (AGUTE)
is proposed to enhance data complexity and diversity, thereby enriching query sets."
    ]

  }

Note: if any key is missing from the user input, just ignore that.
"""




def tailor_resume_anthropic(cv_text, prompt, model, retrieved_examples):
    filled_sys_prompt = SYSTEM_PROMPT.replace("<CV_TEXT>", cv_text)
    filled_sys_prompt = filled_sys_prompt.replace("<RETRIEVED_EXAMPLES>", str(retrieved_examples))
    final_prompt = JSON_PROMPT.replace("<QUERY>", prompt)
    client = anthropic.Client(api_key=os.environ["ANTHROPIC_API_KEY"])


    try:
        response = client.messages.create(
            model=model,
            system = filled_sys_prompt,
            messages=[
                {"role": "user", "content": final_prompt},
            ],
            max_tokens = 2000
        )

        answer = response
        return answer
    except Exception as e:
        print(e)
        print("Failed to tailor resume.")
        return cv_text