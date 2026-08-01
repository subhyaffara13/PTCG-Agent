
def analyzecommon(block):
    if not hascommon(block):
        return block
    commonvars = []
    for k in list(block['common'].keys()):
        comvars = []
        for e in block['common'][k]:
            m = re.match(
                r'\A\s*\b(?P<name>.*?)\b\s*(\((?P<dims>.*?)\)|)\s*\Z', e, re.I)
            if m:
                dims = []
                if m.group('dims'):
                    dims = [x.strip()
                            for x in markoutercomma(m.group('dims')).split('@,@')]
                n = rmbadname1(m.group('name').strip())
                if n in block['vars']:
                    if 'attrspec' in block['vars'][n]:
                        block['vars'][n]['attrspec'].append(
                            f"dimension({','.join(dims)})")
                    else:
                        block['vars'][n]['attrspec'] = [
                            f"dimension({','.join(dims)})"]
                elif dims:
                    block['vars'][n] = {
                        'attrspec': [f"dimension({','.join(dims)})"]}
                else:
                    block['vars'][n] = {}
                if n not in commonvars:
                    commonvars.append(n)
            else:
                n = e
                errmess(
                    f'analyzecommon: failed to extract "<name>[(<dims>)]" from "{e}" in common /{k}/.\n')
            comvars.append(n)
        block['common'][k] = comvars
    if 'commonvars' not in block:
        block['commonvars'] = commonvars
    else:
        block['commonvars'] = block['commonvars'] + commonvars
    return block

