
def buildusevars(m, r):
    ret = {}
    outmess(
        f"\t\tBuilding use variable hooks for module \"{m['name']}\" (feature only for F90/F95)...\n")
    varsmap = {}
    revmap = {}
    if 'map' in r:
        for k in r['map'].keys():
            mapped_name = r['map'][k]
            if mapped_name in revmap:
                outmess(f'\t\t\tVariable "{mapped_name}<={k}" is already mapped by '
                        f'"{revmap[mapped_name]}". Skipping.\n')
            else:
                revmap[mapped_name] = k
    if r.get('only'):
        for v in r['map'].keys():
            if r['map'][v] in m['vars']:

                if revmap[r['map'][v]] == v:
                    varsmap[v] = r['map'][v]
                else:
                    outmess(f"\t\t\tIgnoring map \"{v}=>{r['map'][v]}\". See above.\n")
            else:
                outmess(
                    f"\t\t\tNo definition for variable \"{v}=>{r['map'][v]}\". Skipping.\n")
    else:
        for v in m['vars'].keys():
            varsmap[v] = revmap.get(v, v)
    for v in varsmap.keys():
        ret = dictappend(ret, buildusevar(v, varsmap[v], m['vars'], m['name']))
    return ret

