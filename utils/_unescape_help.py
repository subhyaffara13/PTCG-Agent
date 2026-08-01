
def _unescape_help(text):
    result = []
    slash = False

    for char in text:
        if slash:
            if char == '\\':
                result.append('\\')
            elif char == '"':
                result.append('"')
            elif char == 'n':
                result.append('\n')
            else:
                result.append('\\' + char)
            slash = False
        else:
            if char == '\\':
                slash = True
            else:
                result.append(char)

    if slash:
        result.append('\\')

    return ''.join(result)

