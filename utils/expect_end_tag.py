
def expect_end_tag(data: ReadBuffer) -> None:
    assert read_tag(data) == END_TAG

