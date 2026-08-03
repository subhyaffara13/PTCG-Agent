import re

def get_batch_id_from_unified_batch_id(file_id: str) -> str:
    ## use regex to get the batch_id from the file_id
    # Ensure file_id is a string and not a mock object
    if not isinstance(file_id, str):
        return ""
    if "llm_batch_id" in file_id:
        batch_id = file_id.split("llm_batch_id:", 1)[1]
    else:
        batch_id = file_id.split("generic_response_id:", 1)[1]
    return re.split(r"[;,]", batch_id, maxsplit=1)[0]

