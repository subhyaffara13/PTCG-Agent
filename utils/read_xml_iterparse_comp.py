
def read_xml_iterparse_comp(comp_path, compression_only, temp_path, **kwargs):
    with get_handle(comp_path, "r", compression=compression_only) as handles:
        temp_path.write_text(handles.handle.read(), encoding="utf-8")
        return read_xml(temp_path, **kwargs)

