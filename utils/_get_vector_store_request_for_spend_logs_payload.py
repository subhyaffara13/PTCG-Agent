
def _get_vector_store_request_for_spend_logs_payload(
    vector_store_request_metadata: Optional[List[StandardLoggingVectorStoreRequest]],
) -> Optional[List[StandardLoggingVectorStoreRequest]]:
    """
    If user does not want to store prompts and responses, then remove the content from the vector store request metadata
    """
    if _should_store_prompts_and_responses_in_spend_logs():
        return vector_store_request_metadata

    # if user does not want to store prompts and responses, then remove the content from the vector store request metadata
    if vector_store_request_metadata is None:
        return None
    for vector_store_request in vector_store_request_metadata:
        vector_store_search_response: VectorStoreSearchResponse = (
            vector_store_request.get("vector_store_search_response")
            or VectorStoreSearchResponse()
        )
        response_data = vector_store_search_response.get("data", []) or []
        for response_item in response_data:
            for content_item in response_item.get("content", []) or []:
                if "text" in content_item:
                    content_item["text"] = REDACTED_BY_LITELM_STRING
    return vector_store_request_metadata

