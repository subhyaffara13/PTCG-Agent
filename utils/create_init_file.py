
def create_init_file(old_lowercase_name: str, new_lowercase_name: str, filenames_to_add: list[tuple[str, bool]]):
    """
    Create the `__init__.py` file to add in the new model folder.

    Args:
        old_lowercase_name (`str`):
            The old lowercase model name.
        new_lowercase_name (`str`):
            The new lowercase model name.
        filenames_to_add (`list[tuple[str, bool]]`):
            A list of tuples of all potential filenames to add for a new model, along a boolean flag describing if we
            should add this file or not. For example, [(`modeling_xxx.px`, True), (`configuration_xxx.py`, True), (`tokenization_xxx.py`, False),...]
    """
    filenames_to_add = [
        (filename.replace(old_lowercase_name, new_lowercase_name).replace(".py", ""), to_add)
        for filename, to_add in filenames_to_add
    ]
    imports = "\n            ".join(f"from .{file} import *" for file, to_add in filenames_to_add if to_add)
    init_file = COPYRIGHT + textwrap.dedent(
        f"""
        from typing import TYPE_CHECKING

        from ...utils import _LazyModule
        from ...utils.import_utils import define_import_structure


        if TYPE_CHECKING:
            {imports}
        else:
            import sys

            _file = globals()["__file__"]
            sys.modules[__name__] = _LazyModule(__name__, _file, define_import_structure(_file), module_spec=__spec__)
        """
    )
    return init_file

