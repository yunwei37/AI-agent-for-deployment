import ray
from gen import ai_generate_content
from tavily_search import tavily_search

ray.init()

@ray.remote
class BlogGenerator:
    def __init__(self):
        pass
    
    def search_info(self, keyword):
        """Step 1: Search for information"""
        return tavily_search(keyword)
    
    def expand_topic(self, keyword):
        """Step 2: Expand the topic"""
        expand_prompt = f"""Based on the keyword '{keyword}', suggest a comprehensive blog topic and title.
        The topic should be SEO-friendly and engaging. Format your response as:
        Title: [your suggested title]
        Topic: [brief description of the expanded topic]
        """
        return ai_generate_content(expand_prompt)
    
    def create_reference_list(self, url_list):
        """Step 3: Create reference list"""
        reference_prompt = f"""Analyze these URLs and create a reference summary:
        {url_list}
        
        For each relevant URL, provide:
        1. A brief summary of key points
        2. Why it's relevant to our topic
        Format as a bulleted list.
        """
        return ai_generate_content(reference_prompt)
    
    def generate_outline(self, keyword, title):
        """Step 4: Generate outline"""
        outline_prompt = f"""Create a detailed outline for a blog post about {keyword}
        Title: {title}
        
        Create a comprehensive outline with:
        1. Introduction
        2. 4-6 main sections with subsections
        3. Conclusion
        
        Format as a hierarchical outline with roman numerals and letters.
        """
        return ai_generate_content(outline_prompt)
    
    def generate_content_section(self, outline, is_first_half):
        """Step 5/6: Generate content sections"""
        section_prompt = f"""Generate detailed content for the {'first' if is_first_half else 'second'} half of this outline:
        {outline}
        
        Write engaging, informative content that:
        1. Maintains consistent tone and style
        2. Includes relevant examples
        3. Uses transition sentences between sections
        4. Incorporates expert insights
        """
        return ai_generate_content(section_prompt)
    
    def merge_content(self, first_half, second_half):
        """Step 7: Merge content"""
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
    
    def add_references(self, content, reference_list):
        """Step 8: Add references"""
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
    
    def humanize_content(self, content):
        """Step 9: Humanize content"""
        with open("test-cases/workflow/humanize_prompt.txt", "r") as f:
            humanize_prompt = f.read()
        
        final_prompt = f"{humanize_prompt}\n\nContent to humanize:\n{content}"
        return ai_generate_content(final_prompt)

@ray.remote
def orchestrate_blog_generation(keyword):
    """Orchestrate the blog generation process using Ray"""
    generator = BlogGenerator.remote()
    
    # Step 1 & 2: Search and expand topic (can run in parallel)
    search_future = generator.search_info.remote(keyword)
    expand_future = generator.expand_topic.remote(keyword)
    
    # Wait for both results
    search_results, expanded_topic = ray.get([search_future, expand_future])
    
    # Step 3: Create reference list (depends on search results)
    reference_future = generator.create_reference_list.remote(search_results)
    
    # Step 4: Generate outline (depends on expanded topic)
    outline_future = generator.generate_outline.remote(keyword, expanded_topic)
    
    # Wait for outline to proceed with content generation
    outline = ray.get(outline_future)
    
    # Step 5 & 6: Generate both content halves in parallel
    first_half_future = generator.generate_content_section.remote(outline, True)
    second_half_future = generator.generate_content_section.remote(outline, False)
    
    # Wait for both content halves and reference list
    first_half, second_half, reference_list = ray.get([
        first_half_future, 
        second_half_future, 
        reference_future
    ])
    
    # Step 7: Merge content
    merged_future = generator.merge_content.remote(first_half, second_half)
    merged_content = ray.get(merged_future)
    
    # Step 8: Add references
    with_refs_future = generator.add_references.remote(merged_content, reference_list)
    content_with_refs = ray.get(with_refs_future)
    
    # Step 9: Humanize content
    final_future = generator.humanize_content.remote(content_with_refs)
    return ray.get(final_future)

def main():
    keyword = "Xen vs vmware"
    
    # Start the blog generation process
    final_blog_future = orchestrate_blog_generation.remote(keyword)
    
    # Wait for the final result
    final_blog = ray.get(final_blog_future)
    
    # Save the output
    with open(f"seo_blog_{keyword.replace(' ', '_')}.txt", "w") as f:
        f.write(final_blog)
    
    print("\nBlog generated successfully!")
    ray.shutdown()

if __name__ == "__main__":
    main()
