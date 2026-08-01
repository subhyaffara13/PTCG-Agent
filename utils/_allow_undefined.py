
def _allow_undefined(schema):
    schema["definitions"]["cell"]["oneOf"].append({"$ref": "#/definitions/unrecognized_cell"})
    schema["definitions"]["output"]["oneOf"].append({"$ref": "#/definitions/unrecognized_output"})
    return schema

