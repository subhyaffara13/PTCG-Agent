
def normalize_mark_list(
    mark_list: Iterable[Mark | MarkDecorator],
) -> Iterable[Mark]:
    """
    Normalize an iterable of Mark or MarkDecorator objects into a list of marks
    by retrieving the `mark` attribute on MarkDecorator instances.

    :param mark_list: marks to normalize
    :returns: A new list of the extracted Mark objects
    """
    for mark in mark_list:
        mark_obj = getattr(mark, "mark", mark)
        if not isinstance(mark_obj, Mark):
            raise TypeError(f"got {mark_obj!r} instead of Mark")
        yield mark_obj

