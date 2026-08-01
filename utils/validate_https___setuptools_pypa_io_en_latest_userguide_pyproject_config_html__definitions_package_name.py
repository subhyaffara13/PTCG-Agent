
def validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html__definitions_package_name(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (str)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be string", value=data, name="" + (name_prefix or "data") + "", definition={'$id': '#/definitions/package-name', 'title': 'Valid package name', 'description': 'Valid package name (importable or :pep:`561`).', 'type': 'string', 'anyOf': [{'type': 'string', 'format': 'python-module-name-relaxed'}, {'type': 'string', 'format': 'pep561-stub-name'}]}, rule='type')
    data_any_of_count11 = 0
    if not data_any_of_count11:
        try:
            if not isinstance(data, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + " must be string", value=data, name="" + (name_prefix or "data") + "", definition={'type': 'string', 'format': 'python-module-name-relaxed'}, rule='type')
            if isinstance(data, str):
                if not custom_formats["python-module-name-relaxed"](data):
                    raise JsonSchemaValueException("" + (name_prefix or "data") + " must be python-module-name-relaxed", value=data, name="" + (name_prefix or "data") + "", definition={'type': 'string', 'format': 'python-module-name-relaxed'}, rule='format')
            data_any_of_count11 += 1
        except JsonSchemaValueException: pass
    if not data_any_of_count11:
        try:
            if not isinstance(data, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + " must be string", value=data, name="" + (name_prefix or "data") + "", definition={'type': 'string', 'format': 'pep561-stub-name'}, rule='type')
            if isinstance(data, str):
                if not custom_formats["pep561-stub-name"](data):
                    raise JsonSchemaValueException("" + (name_prefix or "data") + " must be pep561-stub-name", value=data, name="" + (name_prefix or "data") + "", definition={'type': 'string', 'format': 'pep561-stub-name'}, rule='format')
            data_any_of_count11 += 1
        except JsonSchemaValueException: pass
    if not data_any_of_count11:
        raise JsonSchemaValueException("" + (name_prefix or "data") + " cannot be validated by any definition", value=data, name="" + (name_prefix or "data") + "", definition={'$id': '#/definitions/package-name', 'title': 'Valid package name', 'description': 'Valid package name (importable or :pep:`561`).', 'type': 'string', 'anyOf': [{'type': 'string', 'format': 'python-module-name-relaxed'}, {'type': 'string', 'format': 'pep561-stub-name'}]}, rule='anyOf')
    return data

