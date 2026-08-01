
def _restrict_to_columns(group, columns, suffix):
    found = [
        c for c in group.columns if c in columns or c.replace(suffix, "") in columns
    ]

    # filter
    group = group.loc[:, found]

    # get rid of suffixes, if any
    group = group.rename(columns=lambda x: x.replace(suffix, ""))

    # put in the right order...
    group = group.loc[:, columns]

    return group

