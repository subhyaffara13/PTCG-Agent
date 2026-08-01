
def expect_tag(data: ReadBuffer, tag: Tag) -> None:
    assert (actual := read_tag(data)) == tag, actual

