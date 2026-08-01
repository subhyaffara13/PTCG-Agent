
def _batch_response_was_successful(batch_job_output_file: dict) -> bool:
    """
    Check if the batch job response status == 200
    """
    _response: dict = batch_job_output_file.get("response", None) or {}
    return _response.get("status_code", None) == 200

