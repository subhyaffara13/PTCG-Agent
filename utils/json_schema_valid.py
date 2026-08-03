from typing import Any, Dict

def json_schema_valid(obj: Any, schema: Dict[str, Any]) -> bool:
    """
    Validate an object against a JSON schema.

    Args:
        obj: The object to validate
        schema: The JSON schema to validate against

    Returns:
        True if valid, False otherwise
    """
    try:
        # Try to import jsonschema, fall back to basic validation if not available
        try:
            import jsonschema

            jsonschema.validate(instance=obj, schema=schema)
            return True
        except ImportError:
            # Basic validation without jsonschema library
            return _basic_json_schema_validate(obj, schema)
        except Exception as validation_error:
            # Catch jsonschema.ValidationError and other validation errors
            if "ValidationError" in type(validation_error).__name__:
                return False
            raise
    except Exception as e:
        verbose_proxy_logger.warning(f"Custom code json_schema_valid error: {e}")
        return False

