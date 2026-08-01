
def parse_rmd_options(line):
    """
    Given a R markdown option line, returns a list of pairs name,value
    :param line:
    :return:
    """
    parsing_context = ParsingContext(line)

    result = []
    prev_char = ""

    name = ""
    value = ""

    for char in "," + line + ",":
        if parsing_context.in_global_expression():
            if char == ",":
                if name != "" or value != "":
                    if result and name == "":
                        raise RMarkdownOptionParsingError(f'Option line "{line}" has no name for option value {value}')
                    result.append((name.strip(), value.strip()))
                    name = ""
                    value = ""
            elif char == "=":
                if name == "":
                    name = value
                    value = ""
                else:
                    value += char
            else:
                parsing_context.count_special_chars(char, prev_char)
                value += char
        else:
            parsing_context.count_special_chars(char, prev_char)
            value += char
        prev_char = char

    if not parsing_context.in_global_expression():
        raise RMarkdownOptionParsingError(f'Option line "{line}" is not properly terminated')

    return result

