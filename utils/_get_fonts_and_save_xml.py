import os
from typing import List, Optional, Tuple

def _get_fonts_and_save_xml(
    filepath_a: Text,
    filepath_b: Text,
    tmpdirpath: Text,
    include_tables: Optional[List[Text]],
    exclude_tables: Optional[List[Text]],
    font_number_a: int,
    font_number_b: int,
    use_multiprocess: bool,
) -> Tuple[Text, Text, Text, Text, Text, Text]:
    post_pathname, postpath, pre_pathname, prepath = _get_pre_post_paths(
        filepath_a, filepath_b
    )
    # instantiate left and right fontTools.ttLib.TTFont objects
    tt_left = TTFont(prepath, fontNumber=font_number_a)
    tt_right = TTFont(postpath, fontNumber=font_number_b)
    left_ttxpath = os.path.join(tmpdirpath, "left.ttx")
    right_ttxpath = os.path.join(tmpdirpath, "right.ttx")
    _mp_save_ttx_xml(
        tt_left,
        tt_right,
        left_ttxpath,
        right_ttxpath,
        exclude_tables,
        include_tables,
        use_multiprocess,
    )
    return left_ttxpath, right_ttxpath, pre_pathname, prepath, post_pathname, postpath

