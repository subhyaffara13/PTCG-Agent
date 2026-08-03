from typing import Any, Dict

def _filter_anyof_fields(schema_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    When anyof is present, only keep the anyof field and its contents - otherwise VertexAI will throw an error - https://github.com/BerriAI/litellm/issues/11164
    Filter out other fields in the same dict.

    E.g. {"anyOf": [{"type": "string"}, {"type": "null"}], "default": "test"} -> {"anyOf": [{"type": "string"}, {"type": "null"}]}

    Case 2: If additional metadata is present, try to keep it
    E.g. {"anyOf": [{"type": "string"}, {"type": "null"}], "default": "test", "title": "test"} -> {"anyOf": [{"type": "string", "title": "test"}, {"type": "null", "title": "test"}]}
    """
    title = schema_dict.get("title", None)
    description = schema_dict.get("description", None)

    if isinstance(schema_dict, dict) and schema_dict.get("anyOf"):
        any_of = schema_dict["anyOf"]
        if (
            (title or description)
            and isinstance(any_of, list)
            and all(isinstance(item, dict) for item in any_of)
        ):
            for item in any_of:
                if title:
                    item["title"] = title
                if description:
                    item["description"] = description
        return {"anyOf": any_of}
    return schema_dict

