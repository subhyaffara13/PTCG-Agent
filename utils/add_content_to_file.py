import os

def add_content_to_file(file_name: str | os.PathLike, new_content: str, add_after: str):
    """
    A utility to add some content inside a given file.

    Args:
        file_name (`str` or `os.PathLike`):
            The name of the file in which we want to insert some content.
        new_content (`str`):
            The content to add.
       add_after (`str`):
           The new content is added just after the first instance matching it.
    """
    with open(file_name, "r", encoding="utf-8") as f:
        old_content = f.read()

    before, after = old_content.split(add_after, 1)
    new_content = before + add_after + new_content + after

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(new_content)

