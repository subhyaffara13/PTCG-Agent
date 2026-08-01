
def write_type_map(data: WriteBuffer, value: dict[str, Type]) -> None:
    write_tag(data, DICT_STR_GEN)
    write_int_bare(data, len(value))
    for key in sorted(value):
        write_str_bare(data, key)
        value[key].write(data)

