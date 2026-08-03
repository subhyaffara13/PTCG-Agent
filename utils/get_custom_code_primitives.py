from typing import Any, Dict

def get_custom_code_primitives() -> Dict[str, Any]:
    """
    Get all primitives to inject into the custom code environment.

    Returns:
        Dict of function name to function
    """
    return {
        # Result types
        "allow": allow,
        "block": block,
        "modify": modify,
        # Regex
        "regex_match": regex_match,
        "regex_match_all": regex_match_all,
        "regex_replace": regex_replace,
        "regex_find_all": regex_find_all,
        # JSON
        "json_parse": json_parse,
        "json_stringify": json_stringify,
        "json_schema_valid": json_schema_valid,
        # URL
        "extract_urls": extract_urls,
        "is_valid_url": is_valid_url,
        "all_urls_valid": all_urls_valid,
        "get_url_domain": get_url_domain,
        # HTTP (async)
        "http_request": http_request,
        "http_get": http_get,
        "http_post": http_post,
        # Code detection
        "detect_code": detect_code,
        "detect_code_languages": detect_code_languages,
        "contains_code_language": contains_code_language,
        # Text utilities
        "contains": contains,
        "contains_any": contains_any,
        "contains_all": contains_all,
        "word_count": word_count,
        "char_count": char_count,
        "lower": lower,
        "upper": upper,
        "trim": trim,
        # Python builtins (safe subset)
        "len": len,
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "list": list,
        "dict": dict,
        "True": True,
        "False": False,
        "None": None,
    }

