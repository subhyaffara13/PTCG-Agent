
def encode_batch_response_ids(response, model: str) -> None:
    """Encode all IDs in a batch response with model routing info (in-place)."""
    if not response or not hasattr(response, "id") or not response.id:
        return
    response.id = encode_file_id_with_model(
        file_id=response.id, model=model, id_type="batch"
    )
    for attr in ("output_file_id", "error_file_id", "input_file_id"):
        if hasattr(response, attr) and getattr(response, attr):
            setattr(
                response,
                attr,
                encode_file_id_with_model(file_id=getattr(response, attr), model=model),
            )

