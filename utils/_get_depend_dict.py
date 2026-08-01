
def _get_depend_dict(name, vars, deps):
    if name in vars:
        words = vars[name].get('depend', [])

        if '=' in vars[name] and not isstring(vars[name]):
            for word in word_pattern.findall(vars[name]['=']):
                # The word_pattern may return values that are not
                # only variables, they can be string content for instance
                if word not in words and word in vars and word != name:
                    words.append(word)
        for word in words[:]:
            for w in deps.get(word, []) \
                    or _get_depend_dict(word, vars, deps):
                if w not in words:
                    words.append(w)
    else:
        outmess(f'_get_depend_dict: no dependence info for {repr(name)}\n')
        words = []
    deps[name] = words
    return words

