
def replace_word_size(text: list[str]) -> list[str]:
    """Replace WORDSIZE with platform specific word sizes"""
    result = []
    for line in text:
        index = line.find("WORD_SIZE")
        if index != -1:
            # get 'WORDSIZE*n' token
            word_size_token = line[index:].split()[0]
            n = int(word_size_token[10:])
            replace_str = str(PLATFORM_SIZE * n)
            result.append(line.replace(word_size_token, replace_str))
        else:
            result.append(line)
    return result

