from typing import Tuple

def _get_pre_post_paths(
    filepath_a: Text,
    filepath_b: Text,
) -> Tuple[Text, Text, Text, Text]:
    prepath = filepath_a
    postpath = filepath_b
    pre_pathname = filepath_a
    post_pathname = filepath_b
    return post_pathname, postpath, pre_pathname, prepath

