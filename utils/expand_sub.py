
def expand_sub(substr, names):
    substr = substr.replace(r'\>', '@rightarrow@')
    substr = substr.replace(r'\<', '@leftarrow@')
    lnames = find_repl_patterns(substr)
    substr = named_re.sub(r"<\1>", substr)  # get rid of definition templates

    def listrepl(mobj):
        thelist = conv(mobj.group(1).replace(r'\,', '@comma@'))
        if template_name_re.match(thelist):
            return f"<{thelist}>"
        name = None
        for key in lnames.keys():    # see if list is already in dictionary
            if lnames[key] == thelist:
                name = key
        if name is None:      # this list is not in the dictionary yet
            name = unique_key(lnames)
            lnames[name] = thelist
        return f"<{name}>"

    # convert all lists to named templates
    # new names are constructed as needed
    substr = list_re.sub(listrepl, substr)

    numsubs = None
    base_rule = None
    rules = {}
    for r in template_re.findall(substr):
        if r not in rules:
            thelist = lnames.get(r, names.get(r, None))
            if thelist is None:
                raise ValueError(f'No replicates found for <{r}>')
            if r not in names and not thelist.startswith('_'):
                names[r] = thelist
            rule = [i.replace('@comma@', ',') for i in thelist.split(',')]
            num = len(rule)

            if numsubs is None:
                numsubs = num
                rules[r] = rule
                base_rule = r
            elif num == numsubs:
                rules[r] = rule
            else:
                rules_base_rule = ','.join(rules[base_rule])
                print("Mismatch in number of replacements "
                      f"(base <{base_rule}={rules_base_rule}>) "
                      f"for <{r}={thelist}>. Ignoring.")
    if not rules:
        return substr

    def namerepl(mobj):
        name = mobj.group(1)
        return rules.get(name, (k + 1) * [name])[k]

    newstr = ''
    for k in range(numsubs):
        newstr += template_re.sub(namerepl, substr) + '\n\n'

    newstr = newstr.replace('@rightarrow@', '>')
    newstr = newstr.replace('@leftarrow@', '<')
    return newstr

