
def apply_tag(tag, cases):
    """
    Add the given tag (a string) to each of the cases (a list of LinalgCase
    objects)
    """
    assert tag in all_tags, "Invalid tag"
    for case in cases:
        case.tags = case.tags | {tag}
    return cases

