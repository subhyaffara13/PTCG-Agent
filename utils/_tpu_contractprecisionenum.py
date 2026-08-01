
def _tpu_contractprecisionenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.contract_precision<{str(x)}>', context=context)

