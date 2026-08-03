from typing import Dict

def _normalize_tool_choice(selected_params: Dict) -> None:
    tc = selected_params.get("toolChoice")
    if tc is None:
        return
    if isinstance(tc, str):
        tc_map = {
            "auto": {"type": "AUTO"},
            "none": {"type": "NONE"},
            "required": {"type": "REQUIRED"},
            "any": {"type": "REQUIRED"},
        }
        selected_params["toolChoice"] = tc_map.get(
            tc.lower(), {"type": "FUNCTION", "name": tc}
        )
        return
    if isinstance(tc, dict):
        raw_type = tc.get("type")
        if not isinstance(raw_type, str):
            raise OCIError(
                status_code=400,
                message=f"Invalid tool_choice for OCI: missing or non-string 'type' in {tc!r}",
            )
        upper = raw_type.upper()
        if upper == "FUNCTION":
            fn = tc.get("function")
            name = fn.get("name") if isinstance(fn, dict) else tc.get("name")
            if not (isinstance(name, str) and name):
                raise OCIError(
                    status_code=400,
                    message="Invalid tool_choice for OCI: 'FUNCTION' type requires a non-empty function name",
                )
            selected_params["toolChoice"] = {"type": "FUNCTION", "name": name}
        elif upper in {"AUTO", "NONE", "REQUIRED"}:
            selected_params["toolChoice"] = {"type": upper}
        else:
            raise OCIError(
                status_code=400,
                message=(
                    f"Invalid tool_choice for OCI: unsupported type {raw_type!r}; "
                    "expected one of 'FUNCTION', 'AUTO', 'NONE', 'REQUIRED'"
                ),
            )
        return
    raise OCIError(
        status_code=400,
        message=(
            f"Invalid tool_choice for OCI: expected str or dict, got "
            f"{type(tc).__name__}"
        ),
    )

