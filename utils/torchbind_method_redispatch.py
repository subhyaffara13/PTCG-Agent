
def torchbind_method_redispatch(self, *args, **kwargs):
    if _is_script_object(self.raw_owner):
        return call_torchbind(self.raw_owner, self.name, *args, **kwargs)
    return _orig_scriptmethod_call(self, *args, **kwargs)

