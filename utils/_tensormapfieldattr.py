
def _tensormapfieldattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm<tensormap_field {str(x)}>', context=context)

