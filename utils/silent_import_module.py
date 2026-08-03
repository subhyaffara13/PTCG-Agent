import os

def silent_import_module(module_name: str) -> types.ModuleType:
    with open(os.devnull, "w") as devnull:
        with warnings.catch_warnings(), redirect_stdout(devnull), redirect_stderr(devnull):
            warnings.simplefilter("ignore")
            runtime = importlib.import_module(module_name)
            # Also run the equivalent of `from module import *`
            # This could have the additional effect of loading not-yet-loaded submodules
            # mentioned in __all__
            __import__(module_name, fromlist=["*"])
    return runtime

