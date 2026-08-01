
def dump_yaml_blocks(data, compact=True):
    """Where possible, we try to use a more compact metadata style.

    For blocks with no nested dicts, the block is denoted by starting colons::

        :other: true
        :tags: [hide-output, show-input]

    For blocks with nesting the block is enlosed by ``---``::

        ---
        other:
            more: true
        tags: [hide-output, show-input]
        ---
    """
    # Allow unicode characters for taking accents into account
    string = yaml.dump(data, Dumper=CompactDumper, sort_keys=False, allow_unicode=True)
    lines = string.splitlines()
    if compact and all(line and line[0].isalpha() for line in lines):
        return "\n".join([f":{line}" for line in lines]) + "\n\n"
    return f"---\n{string}---\n"

