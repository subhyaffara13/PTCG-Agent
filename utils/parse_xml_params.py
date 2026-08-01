
def parse_xml_params(xml_content, json_schema: Optional[dict] = None):
    """
    Compare the xml output to the json schema

    check if a value is a list - if so, get it's child elements
    """
    root = ET.fromstring(xml_content)
    params = {}

    if json_schema is not None:  # check if we have a json schema for this function call
        # iterate over all properties in the schema
        for prop in json_schema["properties"]:
            # If property is an array, get the nested items
            _element = root.find(f"parameters/{prop}")
            if json_schema["properties"][prop]["type"] == "array":
                items = []
                if _element is not None:
                    for value in _element:
                        try:
                            if value.text is not None:
                                _value = json.loads(value.text)
                            else:
                                continue
                        except json.JSONDecodeError:
                            _value = value.text
                        items.append(_value)
                    params[prop] = items
            # If property is not an array, append the value directly
            elif _element is not None and _element.text is not None:
                try:
                    _value = json.loads(_element.text)
                except json.JSONDecodeError:
                    _value = _element.text
                params[prop] = _value
    else:
        for child in root.findall(".//parameters/*"):
            if child is not None and child.text is not None:
                try:
                    # Attempt to decode the element's text as JSON
                    params[child.tag] = json.loads(child.text)  # type: ignore
                except json.JSONDecodeError:
                    # If JSON decoding fails, use the original text
                    params[child.tag] = child.text  # type: ignore

    return params

