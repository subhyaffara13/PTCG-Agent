
def write_type_list(data: WriteBuffer, value: Sequence[Type]) -> None:
    write_tag(data, LIST_GEN)
    write_int_bare(data, len(value))
    for item in value:
        item.write(data)

