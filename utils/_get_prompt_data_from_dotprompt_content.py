
def _get_prompt_data_from_dotprompt_content(dotprompt_content: str) -> dict:
    """
    Get the prompt data from the dotprompt content.

    The UI stores prompts under `dotprompt_content` in the database. This function parses the content and returns the prompt data in the format expected by the prompt manager.
    """
    from .prompt_manager import PromptManager

    # Parse the dotprompt content to extract frontmatter and content
    temp_manager = PromptManager()
    metadata, content = temp_manager._parse_frontmatter(dotprompt_content)

    # Convert to prompt_data format
    return {"content": content.strip(), "metadata": metadata}

