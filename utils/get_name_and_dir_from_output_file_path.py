
def get_name_and_dir_from_output_file_path(
    file_path: str,
) -> tuple[str, str]:
    """
    This function help prepare parameters to new cpp_builder.
    Example:
        input_code: /tmp/tmpof1n5g7t/5c/c5crkkcdvhdxpktrmjxbqkqyq5hmxpqsfza4pxcf3mwk42lphygc.cpp
        name, dir = get_name_and_dir_from_output_file_path(input_code)
    Run result:
        name = c5crkkcdvhdxpktrmjxbqkqyq5hmxpqsfza4pxcf3mwk42lphygc
        dir = /tmp/tmpof1n5g7t/5c/

    put 'name' and 'dir' to CppBuilder's 'name' and 'output_dir'.
    CppBuilder --> get_target_file_path will format output path according OS:
    Linux: /tmp/tmppu87g3mm/zh/czhwiz4z7ca7ep3qkxenxerfjxy42kehw6h5cjk6ven4qu4hql4i.so
    Windows: [Windows temp path]/tmppu87g3mm/zh/czhwiz4z7ca7ep3qkxenxerfjxy42kehw6h5cjk6ven4qu4hql4i.dll
    """
    name_and_ext = os.path.basename(file_path)
    name, _ext = os.path.splitext(name_and_ext)
    dir = os.path.dirname(file_path)

    return name, dir

