
def file_specific_replacement(filepath, search_string, replace_string, strict=False) -> None:
    with openf(filepath, "r+") as f:
        contents = f.read()
        if strict:
            contents = re.sub(fr'\b({re.escape(search_string)})\b', lambda x: replace_string, contents)
        else:
            contents = contents.replace(search_string, replace_string)
        f.seek(0)
        f.write(contents)
        f.truncate()

