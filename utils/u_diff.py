
def u_diff(
    filepath_a: Text,
    filepath_b: Text,
    context_lines: int = 3,
    include_tables: Optional[List[Text]] = None,
    exclude_tables: Optional[List[Text]] = None,
    font_number_a: int = -1,
    font_number_b: int = -1,
    use_multiprocess: bool = True,
) -> Iterator[Text]:
    """Performs a unified diff on a TTX serialized data format dump of font binary data using
    a modified version of the Python standard libary difflib module.

    filepath_a: (string) pre-file local file path
    filepath_b: (string) post-file local file path
    context_lines: (int) number of context lines to include in the diff (default=3)
    include_tables: (list of str) Python list of OpenType tables to include in the diff
    exclude_tables: (list of str) Python list of OpentType tables to exclude from the diff
    use_multiprocess: (bool) use multi-processor optimizations (default=True)

    include_tables and exclude_tables are mutually exclusive arguments.  Only one should
    be defined

    :returns: Generator of ordered diff line strings that include newline line endings
    :raises: KeyError if include_tables or exclude_tables includes a mis-specified table
    that is not included in filepath_a OR filepath_b
    """

    def _create_unified_diff(
        left_ttxpath: Text,
        right_ttxpath: Text,
        pre_pathname: Text,
        prepath: Text,
        post_pathname: Text,
        postpath: Text,
    ) -> Iterable[Text]:
        with open(left_ttxpath) as ff:
            fromlines = ff.readlines()
        with open(right_ttxpath) as tf:
            tolines = tf.readlines()

        fromdate = get_file_modtime(prepath)
        todate = get_file_modtime(postpath)

        yield from unified_diff(
            fromlines,
            tolines,
            pre_pathname,
            post_pathname,
            fromdate,
            todate,
            n=context_lines,
        )

    yield from _diff_with_saved_ttx_files(
        filepath_a,
        filepath_b,
        include_tables,
        exclude_tables,
        font_number_a,
        font_number_b,
        use_multiprocess,
        _create_unified_diff,
    )

