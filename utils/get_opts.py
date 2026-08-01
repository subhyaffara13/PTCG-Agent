
def get_opts(param):
    '''Extract options from a parameter name.'''
    if param.startswith('-'):
        opts = []
        names = []
        meta = None
        for long, name, meta in ARG_RE.findall(param):
            prefix = ['-', '--'][len(long)]
            opts.append('{0}{1}'.format(prefix, name))
            names.append(name)
        return max(names, key=len), opts, meta
    opt, meta = (list(filter(None, POS_RE.findall(param))) + [''])[:2]
    return opt, [opt], meta

