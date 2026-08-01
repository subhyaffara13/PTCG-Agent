
def owner_create_rref_my_script_module(a):
    return rpc.RRef(MyScriptModule(a), type_hint=MyModuleInterface)

