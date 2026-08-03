import re

def _skip_regex(lines_enum, options):
    skip_regex = options.skip_requirements_regex if options else None
    if skip_regex:
        pattern = re.compile(skip_regex)
        lines_enum = _filterfalse(lambda e: pattern.search(e[1]), lines_enum)
    return lines_enum

