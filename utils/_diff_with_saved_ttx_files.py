from typing import Callable, List, Optional

def _diff_with_saved_ttx_files(
    filepath_a: Text,
    filepath_b: Text,
    include_tables: Optional[List[Text]],
    exclude_tables: Optional[List[Text]],
    font_number_a: int,
    font_number_b: int,
    use_multiprocess: bool,
    create_differ: Callable[[Text, Text, Text, Text, Text, Text], Iterable[Text]],
) -> Iterator[Text]:
    with _saved_ttx_files(
        filepath_a,
        filepath_b,
        include_tables,
        exclude_tables,
        font_number_a,
        font_number_b,
        use_multiprocess,
    ) as (
        left_ttxpath,
        right_ttxpath,
        pre_pathname,
        prepath,
        post_pathname,
        postpath,
    ):
        yield from create_differ(
            left_ttxpath,
            right_ttxpath,
            pre_pathname,
            prepath,
            post_pathname,
            postpath,
        )

