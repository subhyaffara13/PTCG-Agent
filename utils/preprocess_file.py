
def preprocess_file(filename, cpp_path="cpp", cpp_args=""):
    """Preprocess a file using cpp.

    filename:
        Name of the file you want to preprocess.

    cpp_path:
    cpp_args:
        Refer to the documentation of parse_file for the meaning of these
        arguments.

    When successful, returns the preprocessed file's contents.
    Errors from cpp will be printed out.
    """
    path_list = [cpp_path]
    if isinstance(cpp_args, list):
        path_list += cpp_args
    elif cpp_args != "":
        path_list += [cpp_args]
    path_list += [filename]

    try:
        # Note the use of universal_newlines to treat all newlines
        # as \n for Python's purpose
        text = check_output(path_list, universal_newlines=True)
    except OSError as e:
        raise RuntimeError(
            "Unable to invoke 'cpp'.  "
            + "Make sure its path was passed correctly\n"
            + f"Original error: {e}"
        )

    return text

