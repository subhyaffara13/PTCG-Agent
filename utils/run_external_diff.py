
def run_external_diff(
    diff_tool: Text,
    diff_args: List[Text],
    filepath_a: Text,
    filepath_b: Text,
    include_tables: Optional[List[Text]] = None,
    exclude_tables: Optional[List[Text]] = None,
    font_number_a: int = -1,
    font_number_b: int = -1,
    use_multiprocess: bool = True,
) -> Iterator[Text]:
    """Performs a unified diff on a TTX serialized data format dump of font binary data using
    an external diff executable that is requested by the caller via `command`

    diff_tool: (string) command line executable string
    diff_args: (list of strings) arguments for the diff tool
    filepath_a: (string) pre-file local file path
    filepath_b: (string) post-file local file path
    include_tables: (list of str) Python list of OpenType tables to include in the diff
    exclude_tables: (list of str) Python list of OpentType tables to exclude from the diff
    use_multiprocess: (bool) use multi-processor optimizations (default=True)

    include_tables and exclude_tables are mutually exclusive arguments.  Only one should
    be defined

    :returns: Generator of ordered diff line strings that include newline line endings
    :raises: KeyError if include_tables or exclude_tables includes a mis-specified table
    that is not included in filepath_a OR filepath_b
    :raises: IOError if exception raised during execution of `command` on TTX files
    """

    def _create_external_diff(
        left_ttxpath: Text,
        right_ttxpath: Text,
        _pre_pathname: Text,
        _prepath: Text,
        _post_pathname: Text,
        _postpath: Text,
    ) -> Iterable[Text]:
        command = [diff_tool] + diff_args + [left_ttxpath, right_ttxpath]
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf8",
        )

        for line in process.stdout:
            yield line
        err = process.stderr.read()
        if err:
            raise IOError(err)

    yield from _diff_with_saved_ttx_files(
        filepath_a,
        filepath_b,
        include_tables,
        exclude_tables,
        font_number_a,
        font_number_b,
        use_multiprocess,
        _create_external_diff,
    )

