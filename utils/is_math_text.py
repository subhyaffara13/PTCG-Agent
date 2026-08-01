
def is_math_text(s):
    """
    Return whether the string *s* contains math expressions.

    This is done by checking whether *s* contains an even number of
    non-escaped dollar signs.
    """
    s = str(s)
    dollar_count = s.count(r'$') - s.count(r'\$')
    even_dollars = (dollar_count > 0 and dollar_count % 2 == 0)
    return even_dollars

