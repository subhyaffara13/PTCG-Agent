
def add_uppercase_char(char_list: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """ Given a replacement char list, this adds uppercase chars to the list """

    for item in char_list:
        char, xlate = item
        upper_dict = char.upper(), xlate.capitalize()
        if upper_dict not in char_list and char != upper_dict[0]:
            char_list.insert(0, upper_dict)
    return char_list

