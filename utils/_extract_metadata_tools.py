
def _extract_metadata_tools(metadata: Optional[Any]) -> Optional[list]:
    if not isinstance(metadata, dict):
        return None
    llm_obj = metadata.get("llm")
    if isinstance(llm_obj, dict):
        return llm_obj.get("tools")
    return None

