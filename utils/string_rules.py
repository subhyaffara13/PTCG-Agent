
def string_rules(quote_mark):
    return [
        (rf"[^{quote_mark}\\]+", String),
        (r"\\.", String.Escape),
        (r"\\", Punctuation),
        (quote_mark, String, '#pop'),
    ]


def string_rules(quote_mark):
    return [
        (rf"[^{quote_mark}\\]", String),
        (r"\\.", String.Escape),
        (quote_mark, String, '#pop'),
    ]

