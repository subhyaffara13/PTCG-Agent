
def load_op_profiles(f: FileLike) -> dict[str, set[OpProfile]]:
    """
    Loads the saved operator profiles from `save_op_profiles`.
    """
    if isinstance(f, (str, os.PathLike)):
        f = os.fspath(f)

        with open(f) as file:
            yaml_str = file.read()

    elif isinstance(f, io.BytesIO):
        yaml_str = f.read().decode("utf-8")

    else:
        raise ValueError(f"Invalid type of file {f}")

    return read_profiles_from_yaml(yaml_str)

