from typing import Any, Dict

def _clean_dict(d):
    """
    Sanitize dictionary for JSON by converting all keys to strings.

    Parameters
    ----------
    d : dict
        The dictionary to convert.

    Returns
    -------
    cleaned_dict : dict
    """
    return {str(k): v for k, v in d.items()}


def _clean_dict(source: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in source.items() if v is not None}

