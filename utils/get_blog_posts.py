from typing import Dict, List

def get_blog_posts(url: str) -> List[Dict[str, str]]:
    """Public entry point — returns the blog posts list."""
    return GetBlogPosts.get_blog_posts(url=url)

