
def module(name: str, config: Config = DEFAULT_CONFIG) -> str:
    """Returns the section placement for the given module name."""
    return module_with_reason(name, config)[0]


def module(
    *,
    sym_name=None,
    sym_visibility=None,
    attrs: Optional[Dict[str, Attribute]] = None,
    loc=None,
    ip=None,
):
    mod = ModuleOp.__base__(
        sym_name=sym_name, sym_visibility=sym_visibility, loc=loc, ip=ip
    )
    if attrs is None:
        attrs = {}
    for attr_name, attr in attrs.items():
        mod.operation.attributes[attr_name] = attr

    return mod


def module(*, sym_name: _Optional[_Union[str, _ods_ir.StringAttr]] = None, sym_visibility: _Optional[_Union[str, _ods_ir.StringAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ModuleOp:
  return ModuleOp(sym_name=sym_name, sym_visibility=sym_visibility, loc=loc, ip=ip)


def module(sym_name: _Union[str, _ods_ir.StringAttr], *, targets: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, offloading_handler: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> GPUModuleOp:
  return GPUModuleOp(sym_name=sym_name, targets=targets, offloadingHandler=offloading_handler, loc=loc, ip=ip)

