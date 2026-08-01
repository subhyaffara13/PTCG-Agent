
def all_lua_builtins():
    from pygments.lexers._lua_builtins import MODULES
    return [w for values in MODULES.values() for w in values]

