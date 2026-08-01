
def get_binary_exclude_tables(
    file1: str,
    file2: str,
    include_tables: Optional[List[str]] = None,
    exclude_tables: Optional[List[str]] = None,
    font_number_1: int = -1,
    font_number_2: int = -1,
) -> Tuple[bool, str]:
    from fontTools.ttLib import TTFont

    with (
        TTFont(file1, lazy=True, fontNumber=font_number_1) as font1,
        TTFont(file2, lazy=True, fontNumber=font_number_2) as font2,
    ):
        tags1 = {str(tag) for tag in font1.reader.keys()}
        tags2 = {str(tag) for tag in font2.reader.keys()}

        all_tags = sorted(
            set(
                _iter_filtered_table_tags(
                    tags1 | tags2,
                    include_tables=include_tables,
                    exclude_tables=exclude_tables,
                )
            )
        )

        both = [tag for tag in all_tags if tag in tags1 and tag in tags2]
        out = set()

        for tag in both:
            data1 = font1.reader[tag]
            data2 = font2.reader[tag]
            if data1 == data2:
                out.add(tag)

        return out

