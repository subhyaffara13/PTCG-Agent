
def should_shutdown(buf: ReadBuffer, expected_tag: Tag) -> bool:
    """Check if the message is a shutdown request."""
    tag = read_tag(buf)
    if tag == SCC_REQUEST_MESSAGE:
        assert not read_int_list(buf)
        return True
    assert tag == expected_tag, f"Unexpected tag: {tag}"
    return False

