from gen import ai_generate_content
import pdfplumber

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""  # Handle None returns
    except Exception as e:
        print(f"Error processing {pdf_file}: {str(e)}")
    return text

def translate_large_pdf(pdf_file, chunk_size=5000, target_language="Chinese"):
    """
    Translate a large PDF file by splitting it into chunks and translating each chunk.
    
    Args:
        pdf_file (str): Path to the PDF file
        chunk_size (int): Maximum size of each chunk in characters
        target_language (str): Target language for translation
    
    Returns:
        str: Complete translated text
    """
    # Extract all text from PDF
    full_text = extract_text_from_pdf(pdf_file)
    
    # Create translation prompt
    translation_prompt = f"Translate the following text to {target_language}. Maintain the academic style and technical terminology. Here's the text:\n\n"
    
    # Split text into chunks
    chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]
    
    # Translate each chunk and collect results
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Translating chunk {i+1}/{len(chunks)}...")
        # Combine prompt with chunk
        full_prompt = translation_prompt + chunk
        # each ai_generate_content should be a ray task
        translated_text = ai_generate_content(full_prompt)
        translated_chunks.append(translated_text)
    
    # Combine all translated chunks
    final_translation = "\n".join(translated_chunks)
    return final_translation

# Example usage
if __name__ == "__main__":
    translated_content = translate_large_pdf("test-cases/workflow/test-pdf/2003-xensosp.pdf")
    print(translated_content)
    # save to file
    with open("test-cases/workflow/test-pdf/2003-xensosp-translated.txt", "w") as f:
        f.write(translated_content)
