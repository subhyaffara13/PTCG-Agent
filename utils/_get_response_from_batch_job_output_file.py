
def _get_response_from_batch_job_output_file(batch_job_output_file: dict) -> Any:
    """
    Get the response from the batch job output file
    """
    _response: dict = batch_job_output_file.get("response", None) or {}
    _response_body = _response.get("body", None) or {}
    return _response_body

