import re

def has_non_roman_characters(input_string):
    # Find any character outside the ASCII range
    non_roman_pattern = re.compile(r"[^\x00-\x7F]")

    # Search the input string for non-Roman characters
    match = non_roman_pattern.search(input_string)
    has_non_roman = match is not None
    return has_non_roman

