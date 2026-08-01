
def _parse_file_object(file_object: Any) -> Any:
    """Prisma may return ``Json`` columns as either a parsed dict or the raw
    JSON string (depending on driver / row source). Mirror the handling used
    elsewhere (see ``openai_files_endpoints/common_utils.py``) so callers can
    treat the result uniformly.
    """
    if isinstance(file_object, str):
        try:
            return json.loads(file_object)
        except (TypeError, ValueError):
            return None
    return file_object

