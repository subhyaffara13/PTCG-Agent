from typing import Any, Dict

def _validate_token_response(
    token_response: Dict[str, Any],
    validation_rules: Dict[str, Any],
    server_id: str,
) -> None:
    """Raise HTTPException 403 if any validation rule doesn't match the token response.

    Supports dot-notation for nested fields (e.g. ``"team.enterprise_id"`` checks
    ``token_response["team"]["enterprise_id"]``).  Top-level keys are tried first,
    then dot-split traversal.  All comparisons are string-coerced so that numeric
    values in the response (e.g. ``"org_id": 12345``) match string rules
    (``"org_id": "12345"``).  Booleans are normalised to JSON-style ``"true"`` /
    ``"false"`` so admin rules written as ``{"verified": "true"}`` match upstream
    responses of ``{"verified": true}``.
    """
    for key, expected in validation_rules.items():
        actual: Any = token_response.get(key)
        # Try dot-notation traversal when top-level lookup returns None
        if actual is None and "." in key:
            obj: Any = token_response
            for part in key.split("."):
                if isinstance(obj, dict):
                    obj = obj.get(part)
                else:
                    obj = None
                    break
            actual = obj
        # Treat absent fields as a distinct failure from a mismatched value
        if actual is None:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "token_validation_failed",
                    "server_id": server_id,
                    "field": key,
                    "message": (
                        f"OAuth token rejected: required field '{key}' is absent"
                    ),
                },
            )
        if _normalize_for_token_comparison(actual) != _normalize_for_token_comparison(
            expected
        ):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "token_validation_failed",
                    "server_id": server_id,
                    "field": key,
                    "message": (
                        f"OAuth token rejected: '{key}' = '{actual}', "
                        f"expected '{expected}'"
                    ),
                },
            )

