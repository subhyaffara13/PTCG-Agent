
def file_add_header(filepath, header) -> None:
    with openf(filepath, "r+") as f:
        contents = f.read()
        if header[0] != "<" and header[-1] != ">":
            header = f'"{header}"'
        contents = (f'#include {header} \n') + contents
        f.seek(0)
        f.write(contents)
        f.truncate()

