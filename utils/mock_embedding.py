from typing import List, Optional

def mock_embedding(model: str, mock_response: Optional[List[float]]):
    if mock_response is None:
        mock_response = [0.0] * 1536
    elif mock_response == "error":
        raise Exception("Mock error")
    return EmbeddingResponse(
        model=model,
        data=[Embedding(embedding=mock_response, index=0, object="embedding")],
        usage=Usage(prompt_tokens=10, completion_tokens=0),
    )

