
def read_field(reader, field):
    if field not in reader.fields:
        return []
    value = reader.fields[field]
    return [_gguf_parse_value(value.parts[_data_index], value.types) for _data_index in value.data]

