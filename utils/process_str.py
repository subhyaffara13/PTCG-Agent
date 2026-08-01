
def process_str(allstr):
    newstr = allstr
    writestr = ''

    struct = parse_structure(newstr)

    oldend = 0
    names = {}
    names.update(_special_names)
    for sub in struct:
        cleanedstr, defs = find_and_remove_repl_patterns(newstr[oldend:sub[0]])
        writestr += cleanedstr
        names.update(defs)
        writestr += expand_sub(newstr[sub[0]:sub[1]], names)
        oldend = sub[1]
    writestr += newstr[oldend:]

    return writestr

