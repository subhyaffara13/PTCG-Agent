
def escapeRegexp(string):
    specialCharacters = (".", "^", "$", "*", "+", "?", "{", "}",
                         "[", "]", "|", "(", ")", "-")
    for char in specialCharacters:
        string = string.replace(char, "\\" + char)

    return string

