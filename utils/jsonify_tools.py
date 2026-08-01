
def jsonify_tools(tools: List[Any]) -> List[Dict]:
    """
    Fixes https://github.com/BerriAI/litellm/issues/9321

    Where user passes in a pydantic base model
    """
    new_tools: List[Dict] = []
    for tool in tools:
        if isinstance(tool, BaseModel):
            tool = tool.model_dump(exclude_none=True)
        elif isinstance(tool, dict):
            tool = tool.copy()
        if isinstance(tool, dict):
            new_tools.append(tool)
    return new_tools

