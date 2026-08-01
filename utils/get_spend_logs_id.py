
def get_spend_logs_id(
    call_type: str, response_obj: dict, kwargs: dict
) -> Optional[str]:
    if call_type == "aretrieve_batch" or call_type == "acreate_file":
        # Generate a hash from the response object
        id: Optional[str] = generate_hash_from_response(response_obj)
    else:
        id = cast(Optional[str], response_obj.get("id")) or cast(
            Optional[str], kwargs.get("litellm_call_id")
        )
    return id

