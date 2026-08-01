
def _gpu_dimensionattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<dim {str(x)}>', context=context)

