
def validate_and_fix_openai_tools(tools: Optional[List]) -> Optional[List[dict]]:
    """
    Ensure tools is List[dict] and not List[BaseModel]
    """
    new_tools = []
    if tools is None:
        return tools
    for tool in tools:
        if isinstance(tool, BaseModel):
            new_tools.append(tool.model_dump())
        elif isinstance(tool, dict):
            new_tools.append(tool)
    return new_tools

