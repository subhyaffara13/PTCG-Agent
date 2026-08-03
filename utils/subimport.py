import sys

def subimport(name):
    # We cannot do simply: `return __import__(name)`: Indeed, if ``name`` is
    # the name of a submodule, __import__ will return the top-level root module
    # of this submodule. For instance, __import__('os.path') returns the `os`
    # module.
    __import__(name)
    return sys.modules[name]

