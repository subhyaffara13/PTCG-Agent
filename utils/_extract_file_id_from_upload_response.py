from typing import Any

def _extract_file_id_from_upload_response(response: Any) -> str:
    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError(
            "Reducto /upload returned a non-JSON 200 response: {}".format(response.text)
        ) from exc
    file_id = (payload or {}).get("file_id") if isinstance(payload, dict) else None
    if not isinstance(file_id, str) or not file_id:
        raise ValueError(
            "Reducto /upload returned 200 without a file_id; got payload={}".format(
                payload
            )
        )
    return file_id

