import time
import uuid
from typing import Any, Dict, List, Optional, Union

def _synthesize_responses_api_response(
    original_response: ResponsesAPIResponse,
    file_search_call_output: Dict[str, Any],
    message_output: Dict[str, Any],
    first_response: Optional[ResponsesAPIResponse] = None,
) -> ResponsesAPIResponse:
    """
    Return a new ResponsesAPIResponse with:
      output[0] = file_search_call item
      output[1] = message item (with citations)

    When first_response is provided, its response_cost is accumulated into the
    synthesized _hidden_params so that billing callbacks see the total cost of
    both provider calls that the emulated flow makes.
    """
    synthesized_output: List[Dict[str, Any]] = [file_search_call_output, message_output]
    synthesized = ResponsesAPIResponse(
        id=getattr(original_response, "id", f"resp_{uuid.uuid4().hex}"),
        object="response",
        created_at=getattr(original_response, "created_at", int(time.time())),
        status="completed",
        model=getattr(original_response, "model", ""),
        output=cast(
            List[Union[ResponseOutputItem, Dict[str, Any]]], synthesized_output
        ),
        usage=getattr(original_response, "usage", None),
        error=None,
    )
    if hasattr(original_response, "_hidden_params"):
        hidden = dict(getattr(original_response, "_hidden_params") or {})
        if first_response is not None and hasattr(first_response, "_hidden_params"):
            first_hidden = getattr(first_response, "_hidden_params") or {}
            first_cost = (
                first_hidden.get("response_cost")
                if isinstance(first_hidden, dict)
                else getattr(first_hidden, "response_cost", None)
            )
            if first_cost is not None:
                current_cost = (
                    hidden.get("response_cost") if isinstance(hidden, dict) else 0
                )
                hidden["response_cost"] = (current_cost or 0) + first_cost
        synthesized._hidden_params = hidden
    return synthesized

