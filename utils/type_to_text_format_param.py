
def type_to_text_format_param(type_: type) -> ResponseFormatTextConfigParam:
    response_format_dict = type_to_response_format_param(type_)
    assert is_given(response_format_dict)
    response_format_dict = cast(ResponseFormat, response_format_dict)  # pyright: ignore[reportUnnecessaryCast]
    assert response_format_dict["type"] == "json_schema"
    assert "schema" in response_format_dict["json_schema"]

    return {
        "type": "json_schema",
        "strict": True,
        "name": response_format_dict["json_schema"]["name"],
        "schema": response_format_dict["json_schema"]["schema"],
    }

