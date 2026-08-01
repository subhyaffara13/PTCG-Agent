
def validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html__definitions_file_directive_properties_file(data, custom_formats={}, name_prefix=None):
    data_one_of_count8 = 0
    if data_one_of_count8 < 2:
        try:
            if not isinstance(data, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + " must be string", value=data, name="" + (name_prefix or "data") + "", definition={'type': 'string'}, rule='type')
            data_one_of_count8 += 1
        except JsonSchemaValueException: pass
    if data_one_of_count8 < 2:
        try:
            if not isinstance(data, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + " must be array", value=data, name="" + (name_prefix or "data") + "", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data_is_list = isinstance(data, (list, tuple))
            if data_is_list:
                data_len = len(data)
                for data_x, data_item in enumerate(data):
                    if not isinstance(data_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + "[{data_x}]".format(**locals()) + " must be string", value=data_item, name="" + (name_prefix or "data") + "[{data_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
            data_one_of_count8 += 1
        except JsonSchemaValueException: pass
    if data_one_of_count8 != 1:
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be valid exactly by one definition" + (" (" + str(data_one_of_count8) + " matches found)"), value=data, name="" + (name_prefix or "data") + "", definition={'oneOf': [{'type': 'string'}, {'type': 'array', 'items': {'type': 'string'}}]}, rule='oneOf')
    return data

