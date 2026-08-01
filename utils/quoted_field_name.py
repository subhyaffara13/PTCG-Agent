
def quoted_field_name(quote_mark):
    return [
        (rf'([^{quote_mark}\\]|\\.)*{quote_mark}',
         Name.Variable, ('#pop', 'object_value'))
    ]


def quoted_field_name(quote_mark):
    return [
        (rf'([^{quote_mark}\\]|\\.)*{quote_mark}',
         Name.Variable, 'field_separator')
    ]

