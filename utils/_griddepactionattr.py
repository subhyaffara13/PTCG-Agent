
def _griddepactionattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<grid_dep_action {str(x)}>', context=context)

