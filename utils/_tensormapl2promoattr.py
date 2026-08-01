
def _tensormapl2promoattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvgpu<l2promo {str(x)}>', context=context)

