
def _build_function_tool(vector_store_ids: List[str]) -> Dict[str, Any]:
    """
    Create a Responses API function-tool definition that describes file search.
    The function accepts one or more natural-language queries (like OpenAI's native
    file_search); LiteLLM runs the actual vector search against the configured
    vector stores.

    Note: Uses Responses API format (name/description/parameters at top level),
    NOT Chat Completion format (nested under "function"), so that the
    LiteLLMCompletionResponsesConfig transformation picks up name and description.
    """
    return {
        "type": "function",
        "name": FILE_SEARCH_FUNCTION_NAME,
        "description": (
            "Search the knowledge base for information relevant to the query. "
            "Use this whenever you need to look up specific facts, documents, "
            "or content from the vector store. You can provide multiple queries "
            "to search for different aspects of the information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "queries": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "One or more search queries to look up in the vector store. "
                        "Multiple queries help find comprehensive information from "
                        "different angles."
                    ),
                },
                "vector_store_id": {
                    "type": "string",
                    "description": "ID of the vector store to search.",
                    "enum": vector_store_ids,
                },
            },
            "required": ["queries"],
        },
    }

