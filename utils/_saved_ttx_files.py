
def _saved_ttx_files(
    filepath_a: Text,
    filepath_b: Text,
    include_tables: Optional[List[Text]],
    exclude_tables: Optional[List[Text]],
    font_number_a: int,
    font_number_b: int,
    use_multiprocess: bool,
) -> Iterator[Tuple[Text, Text, Text, Text, Text, Text]]:
    with tempfile.TemporaryDirectory() as tmpdirpath:
        yield _get_fonts_and_save_xml(
            filepath_a,
            filepath_b,
            tmpdirpath,
            include_tables,
            exclude_tables,
            font_number_a,
            font_number_b,
            use_multiprocess,
        )

