from typing import Any, Dict, List, Optional, Union

def _apply_managed_file_id_mapping(
    input: Union[str, ResponseInputParam],
    tools: Optional[Iterable[ToolParam]],
    kwargs: Dict[str, Any],
    local_vars: Dict[str, Any],
) -> tuple[Union[str, ResponseInputParam], Optional[Iterable[ToolParam]]]:
    model_file_id_mapping = kwargs.get("model_file_id_mapping")
    model_info_id = (
        kwargs.get("model_info", {}).get("id")
        if isinstance(kwargs.get("model_info"), dict)
        else None
    )

    input = cast(
        Union[str, ResponseInputParam],
        update_responses_input_with_model_file_ids(
            input=input,
            model_id=model_info_id,
            model_file_id_mapping=model_file_id_mapping,
        ),
    )
    local_vars["input"] = input

    if tools:
        tools = cast(
            Optional[Iterable[ToolParam]],
            update_responses_tools_with_model_file_ids(
                tools=cast(Optional[List[Dict[str, Any]]], tools),
                model_id=model_info_id,
                model_file_id_mapping=model_file_id_mapping,
            ),
        )
        local_vars["tools"] = tools

    return input, tools

