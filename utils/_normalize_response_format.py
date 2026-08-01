
def _normalize_response_format(selected_params: Dict, vendor: OCIVendors) -> None:
    rf = selected_params.get("responseFormat")
    if not isinstance(rf, dict) or "type" not in rf:
        return

    rf_type = str(rf["type"]).lower()
    raw_schema = rf.get("json_schema")
    json_schema = raw_schema if isinstance(raw_schema, dict) else None

    if rf_type == "text":
        selected_params["responseFormat"] = {"type": "TEXT"}
        return

    if vendor == OCIVendors.COHERE:
        # OCI Cohere has no JSON_SCHEMA type; a schema rides on JSON_OBJECT.
        payload: Dict[str, Any] = {"type": "JSON_OBJECT"}
        if json_schema is not None and json_schema.get("schema") is not None:
            payload["schema"] = json_schema["schema"]
        selected_params["responseFormat"] = payload
        return

    if rf_type == "json_schema":
        if json_schema is None:
            raise OCIError(
                status_code=400,
                message="response_format type 'json_schema' requires a 'json_schema' object",
            )
        # OCI's ResponseJsonSchema accepts only name/description/schema/isStrict.
        # OpenAI sends `strict` instead of `isStrict`; forwarding it (or any
        # other extra key) makes OCI reject the whole request with HTTP 400.
        oci_schema: Dict[str, Any] = {"name": json_schema.get("name") or "response"}
        if json_schema.get("description") is not None:
            oci_schema["description"] = json_schema["description"]
        if json_schema.get("schema") is not None:
            oci_schema["schema"] = json_schema["schema"]
        if json_schema.get("strict") is not None:
            oci_schema["isStrict"] = json_schema["strict"]
        selected_params["responseFormat"] = {
            "type": "JSON_SCHEMA",
            "jsonSchema": oci_schema,
        }
        return

    fmt = rf_type.upper()
    selected_params["responseFormat"] = {
        "type": "JSON_OBJECT" if fmt == "JSON" else fmt
    }

