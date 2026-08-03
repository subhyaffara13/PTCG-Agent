from typing import Optional

def mock_vector_store_create_response(
    mock_response: Optional[VectorStoreCreateResponse] = None,
):
    """Mock response for vector store create"""
    if mock_response is None:
        mock_response = VectorStoreCreateResponse(
            id="vs_mock123",
            object="vector_store",
            created_at=1699061776,
            name="Mock Vector Store",
            bytes=0,
            file_counts=VectorStoreFileCounts(
                in_progress=0,
                completed=0,
                failed=0,
                cancelled=0,
                total=0,
            ),
            status="completed",
            expires_after=None,
            expires_at=None,
            last_active_at=None,
            metadata=None,
        )

    return mock_response

