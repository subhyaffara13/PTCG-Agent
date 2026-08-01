
def prettify_stack(stack: list[dict[str, str]], str_to_filename: dict[int, str]) -> str:
    res = ""
    for frame in stack:
        if frame["filename"] not in str_to_filename:
            continue

        res += f"""
        File {str_to_filename[frame["filename"]]}, lineno {frame["line"]}, in {frame["name"]}"""  # type: ignore[index]

    res += f"\n            {stack[-1]['loc']}"
    return res

