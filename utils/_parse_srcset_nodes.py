
def _parse_srcsetNodes(st):
    """
    parse srcset...
    """
    entries = st.split(',')
    srcset = {}
    for entry in entries:
        spl = entry.strip().split(' ')
        if len(spl) == 1:
            srcset[0] = spl[0]
        elif len(spl) == 2:
            mult = spl[1][:-1]
            srcset[float(mult)] = spl[0]
        else:
            raise ExtensionError(f'srcset argument "{entry}" is invalid.')
    return srcset

