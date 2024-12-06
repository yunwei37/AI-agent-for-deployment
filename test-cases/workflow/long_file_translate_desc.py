app_desc = """
This application translates the text of large PDF documents into a specified target language while preserving academic style and technical terminology. It extracts text from the PDF file, splits the text into manageable chunks, translates each chunk using a language model, and then combines the translated chunks into a complete text result.
"""

agents_desc = """
- extract_text_from_pdf: A function that retrieves text content from a PDF file using the pdfplumber library, handling errors gracefully.
- translate_large_pdf: A function that splits the extracted text into chunks, creates a translation prompt, and processes each chunk through an AI content generation process to produce the translated text.
- ai_generate_content: A function that acts as an AI translation service, receiving prompts and returning the generated translations for each text chunk.
"""