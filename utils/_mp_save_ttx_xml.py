from typing import Any, List, Optional

def _mp_save_ttx_xml(
    tt_left: Any,
    tt_right: Any,
    left_ttxpath: Text,
    right_ttxpath: Text,
    exclude_tables: Optional[List[Text]],
    include_tables: Optional[List[Text]],
    use_multiprocess: bool,
) -> None:
    if use_multiprocess and cpu_count() > 1:
        # Use parallel fontTools.ttLib.TTFont.saveXML dump
        # by default on multi CPU systems.  This is a performance
        # optimization. Profiling demonstrates that this can reduce
        # execution time by up to 30% for some fonts
        mp_args_list = [
            (tt_left, left_ttxpath, include_tables, exclude_tables),
            (tt_right, right_ttxpath, include_tables, exclude_tables),
        ]
        with Pool(processes=2) as pool:
            pool.starmap(_ttfont_save_xml, mp_args_list)
    else:
        # use sequential fontTools.ttLib.TTFont.saveXML dumps
        # when use_multiprocess is False or single CPU system
        # detected
        _ttfont_save_xml(tt_left, left_ttxpath, include_tables, exclude_tables)
        _ttfont_save_xml(tt_right, right_ttxpath, include_tables, exclude_tables)

