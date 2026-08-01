
def _tpu_pipelinemodeenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.pipeline_mode<{str(x)}>', context=context)

