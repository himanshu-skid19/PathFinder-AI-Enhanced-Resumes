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

def query_with_context(combined_prompt):
    """
    Query the engine with a combined prompt that includes context and the original query.

    Args:
    - combined_prompt (str): The combined prompt.

    Returns:
    - str: The response from the query engine.
    """
    # Query the engine
    response = query_engine.query(combined_prompt)
    return response
