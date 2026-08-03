from typing import Any, Optional, Union

def _add_headers_to_response(response: Any, headers: dict) -> Any:
    """
    Helper function to add headers to a response's hidden params
    """
    if response is None or not isinstance(response, BaseModel):
        return response

    hidden_params: Optional[Union[dict, HiddenParams]] = getattr(
        response, "_hidden_params", {}
    )

    if hidden_params is None:
        hidden_params_dict = {}
    elif isinstance(hidden_params, HiddenParams):
        hidden_params_dict = hidden_params.model_dump()
    else:
        hidden_params_dict = hidden_params

    hidden_params_dict.setdefault("additional_headers", {})
    hidden_params_dict["additional_headers"].update(headers)

    setattr(response, "_hidden_params", hidden_params_dict)
    return response

