
def read_xml_iterparse(data, temp_path, **kwargs):
    temp_path.write_text(data, encoding="utf-8")
    return read_xml(temp_path, **kwargs)


def read_xml_iterparse(data, temp_file, **kwargs):
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(data)
    return read_xml(temp_file, **kwargs)

