
def to_decimal(values, context=None):
    return DecimalArray([decimal.Decimal(x) for x in values], context=context)

