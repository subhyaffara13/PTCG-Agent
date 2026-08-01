
def mock_vector_store_search_response(
    mock_results: Optional[List[VectorStoreSearchResult]] = None,
):
    """Mock response for vector store search"""
    if mock_results is None:
        mock_results = [
            VectorStoreSearchResult(
                score=0.95,
                content=[
                    VectorStoreResultContent(
                        text="This is a sample search result from the vector store.",
                        type="text",
                    )
                ],
            )
        ]

    return VectorStoreSearchResponse(
        object="vector_store.search_results.page",
        search_query="sample query",
        data=mock_results,
    )

