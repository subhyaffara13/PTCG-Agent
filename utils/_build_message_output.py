from typing import Any, Dict, List

def _build_message_output(
    response_text: str,
    results: List[VectorStoreSearchResult],
) -> Dict[str, Any]:
    """Build the message output item with optional file_citation annotations."""
    annotations = _build_file_citation_annotations(results, response_text)
    return {
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "output_text",
                "text": response_text,
                "annotations": annotations,
            }
        ],
    }

