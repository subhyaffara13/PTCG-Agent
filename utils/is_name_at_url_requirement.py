
def is_name_at_url_requirement(reqstr: str) -> bool:
    """
    Return True if this requirement is in the "name@url" format.
    For example:
    >>> is_name_at_url_requirement("foo@https://foo.com")
    True
    >>> is_name_at_url_requirement("foo@ https://foo.com")
    True
    >>> is_name_at_url_requirement("foo @ https://foo.com")
    True
    """
    return bool(reqstr and split_as_name_at_url(reqstr))

