
def _compose_tarfile_filters(*filters):
    def compose_two(f1, f2):
        return lambda member, path: f1(f2(member, path), path)

    return functools.reduce(compose_two, filters, lambda member, path: member)

