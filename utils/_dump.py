import os

def _dump(self, file, protocol=2):
    if hasattr(file, 'write'):
        ctx = nullcontext(file)
    else:
        ctx = open(os.fspath(file), "wb")
    with ctx as f:
        pickle.dump(self, f, protocol=protocol)

