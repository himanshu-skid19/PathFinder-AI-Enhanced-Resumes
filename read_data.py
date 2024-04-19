from imports import *


def process_directory(directory_path, embed_model, vector_store):
    """
    Process each PDF in the directory for section-wise embedding storage.
    """
    documents = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, filename)
            logging.info(f"Processing {filename}...")
            sections_data = extract_resume_sections(pdf_path)
            for section, content in sections_data.items():
                document = create_document(content, filename, section, embed_model)
                documents.append(document)
    logging.info("All PDFs processed.")
    return documents


def extract_resume_sections(pdf_path, output_dir="./resume_sections"):
    """
    Extracts categorized sections from the resume PDF and stores extracted text or tables in separate files by section.
    """
    # Use PDFMiner to extract raw text for the pattern search
    text = extract_text(pdf_path, laparams=LAParams(line_overlap=0.5))

    # Define sections and compile regex pattern
    sections = [
        "Research Experiences", "Industrial Experience",
        "Key Projects", "Other Projects", "Teaching Experience",
         "Projects", "Experience"
    ]
    pattern = '|'.join([f"({re.escape(sec)})" for sec in sections])
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dictionary to store section texts or table data
    section_data = {}

    # Open the PDF with pdfplumber for table extraction
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(len(matches)):
            start = matches[i].start()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            section_title = text[matches[i].start():matches[i].end()].strip()

            section_content = text[start:end].strip()
            section_data[section_title] = section_content
            with open(os.path.join(output_dir, f"{section_title}.txt"), "w", encoding="utf-8") as file:
                file.write(section_content)

    return section_data

def preprocess_text(text):
    """
    Normalize and clean text for embedding.
    """
    if type(text) == list:
        return text
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def embed_text(model, text):
    """
    Embed the text using the specified embedding model.
    """
    return model.get_text_embedding(text)  # Example, adjust based on your model's method



def create_document(text, filename, category, embed_model):
    """
    Create a Document object with embedded text and metadata.
    """
    # Parse filename to extract branch, role, and company
    parts = filename.replace('.pdf', '').split('_')
    if len(parts) == 3:
        branch, role, company = parts
    else:
        logging.warning(f"Filename {filename} does not match expected pattern. Metadata will not include branch, role, company.")
        branch, role, company = None, None, None

    preprocessed_text = preprocess_text(text)
    embedding = embed_text(embed_model, preprocessed_text)
    metadata = {
        "filename": filename,
        "category": category,
        "branch": branch,
        "role": role,
        "company": company
    }
    
    document = Document(
        text=preprocessed_text,
        embedding=embedding,
        metadata=metadata
    )
    return document


