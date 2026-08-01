
def _tensormapinterleavelayoutattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tensormap_interleave_layout<{str(x)}>', context=context)

