# from googlesearch import search
from gen import ai_generate_content
from tavily_search import tavily_search
import time

# def google_search(query, num_results=10):
#     """Perform Google search and return results."""
#     try:
#         return list(search(query, num_results=num_results, lang="en", pause=2.0))
#     except Exception as e:
#         print(f"Error in search: {str(e)}")
#         return []

def expand_topic(keyword):
    """Expand keyword into a full topic with title."""
    expand_prompt = f"""Based on the keyword '{keyword}', suggest a comprehensive blog topic and title.
    The topic should be SEO-friendly and engaging. Format your response as:
    Title: [your suggested title]
    Topic: [brief description of the expanded topic]
    """
    response = ai_generate_content(expand_prompt)
    return response

def create_reference_list(url_list):
    """Create a summary of reference materials from URLs."""
    # url_list = "\n".join(urls)
    reference_prompt = f"""Analyze these URLs and create a reference summary:
    {url_list}
    
    For each relevant URL, provide:
    1. A brief summary of key points
    2. Why it's relevant to our topic
    Format as a bulleted list.
    """
    return ai_generate_content(reference_prompt)

def generate_outline(keyword, title):
    """Generate a detailed blog outline."""
    outline_prompt = f"""Create a detailed outline for a blog post about {keyword}
    Title: {title}
    
    Create a comprehensive outline with:
    1. Introduction
    2. 4-6 main sections with subsections
    3. Conclusion
    
    Format as a hierarchical outline with roman numerals and letters.
    """
    return ai_generate_content(outline_prompt)

def generate_content_from_outline(outline, is_first_half):
    """Generate content for either first or second half of outline."""
    section_prompt = f"""Generate detailed content for the {'first' if is_first_half else 'second'} half of this outline:
    {outline}
    
    Write engaging, informative content that:
    1. Maintains consistent tone and style
    2. Includes relevant examples
    3. Uses transition sentences between sections
    4. Incorporates expert insights
    """
    return ai_generate_content(section_prompt)

def merge_content(first_half, second_half):
    """Merge two content halves seamlessly."""
    merge_prompt = f"""Merge these two blog sections into one cohesive piece:
    
    First Half:
    {first_half}
    
    Second Half:
    {second_half}
    
    Ensure:
    1. Smooth transitions between sections
    2. Consistent tone throughout
    3. Logical flow of ideas
    """
    return ai_generate_content(merge_prompt)

def add_references(content, reference_list):
    """Add references and external links to content."""
    reference_prompt = f"""Enhance this blog post with references:
    
    Content:
    {content}
    
    Reference Materials:
    {reference_list}
    
    Please:
    1. Add relevant in-text citations
    2. Insert external links naturally
    3. Add a "References" section at the end
    4. Maintain the flow of the content
    """
    return ai_generate_content(reference_prompt)

def humanize_content(content):
    """Make content more engaging and human-like."""
    with open("test-cases/workflow/humanize_prompt.txt", "r") as f:
        humanize_prompt = f.read()
    
    final_prompt = f"{humanize_prompt}\n\nContent to humanize:\n{content}"
    return ai_generate_content(final_prompt)

def generate_seo_blog(keyword):
    """Main function to generate complete SEO blog."""
    print(f"1. Searching for: {keyword}")
    search_results = tavily_search(keyword)
    print(search_results)
    print("2. Expanding topic...")
    expanded_topic = expand_topic(keyword)
    print(expanded_topic)
    
    print("3. Creating reference list...")
    reference_list = create_reference_list(search_results)
    print(reference_list)
    
    print("4. Generating outline...")
    outline = generate_outline(keyword, expanded_topic)
    print(outline)
    
    print("5. Generating first half content...")
    first_half = generate_content_from_outline(outline, True)
    print(first_half)
    
    print("6. Generating second half content...")
    second_half = generate_content_from_outline(outline, False)
    print(second_half)
    
    print("7. Merging content...")
    merged_content = merge_content(first_half, second_half)
    print(merged_content)
    
    print("8. Adding references...")
    content_with_refs = add_references(merged_content, reference_list)
    print(content_with_refs)
    
    print("9. Humanizing content...")
    final_content = humanize_content(content_with_refs)
    print(final_content)
    return final_content

if __name__ == "__main__":
    # keyword = input("Enter your keyword for the blog post: ")
    keyword = "Xen vs vmware"
    final_blog = generate_seo_blog(keyword)
    
    # Save the output
    with open(f"seo_blog_{keyword.replace(' ', '_')}.txt", "w") as f:
        f.write(final_blog)
    
    print("\nBlog generated successfully!")