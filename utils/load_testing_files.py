import os

def load_testing_files():
    for fn in _filenames:
        name = fn.replace(".txt", "").replace("-ml", "")
        fqfn = os.path.join(os.path.dirname(__file__), 'data', fn)
        fp = open(fqfn)
        eo[name] = np.loadtxt(fp)
        fp.close()
    eo['pdist-boolean-inp'] = np.bool_(eo['pdist-boolean-inp'])
    eo['random-bool-data'] = np.bool_(eo['random-bool-data'])
    eo['random-float32-data'] = np.float32(eo['random-double-data'])
    eo['random-int-data'] = np.long(eo['random-int-data'])
    eo['random-uint-data'] = np.ulong(eo['random-uint-data'])

