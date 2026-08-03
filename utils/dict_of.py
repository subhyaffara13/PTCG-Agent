from typing import Dict

def dict_of(key: ParserElement, value: ParserElement) -> Dict:
    """Helper to easily and clearly define a dictionary by specifying
    the respective patterns for the key and value.  Takes care of
    defining the :class:`Dict`, :class:`ZeroOrMore`, and
    :class:`Group` tokens in the proper order.  The key pattern
    can include delimiting markers or punctuation, as long as they are
    suppressed, thereby leaving the significant key text.  The value
    pattern can include named results, so that the :class:`Dict` results
    can include named token fields.

    Example:

    .. doctest::

       >>> text = "shape: SQUARE posn: upper left color: light blue texture: burlap"

       >>> data_word = Word(alphas)
       >>> label = data_word + FollowedBy(':')
       >>> attr_expr = (
       ...    label
       ...    + Suppress(':')
       ...    + OneOrMore(data_word, stop_on=label)
       ...    .set_parse_action(' '.join))
       >>> print(attr_expr[1, ...].parse_string(text).dump())
       ['shape', 'SQUARE', 'posn', 'upper left', 'color', 'light blue', 'texture', 'burlap']

       >>> attr_label = label
       >>> attr_value = Suppress(':') + OneOrMore(data_word, stop_on=label
       ...   ).set_parse_action(' '.join)

       # similar to Dict, but simpler call format
       >>> result = dict_of(attr_label, attr_value).parse_string(text)
       >>> print(result.dump())
       [['shape', 'SQUARE'], ['posn', 'upper left'], ['color', 'light blue'], ['texture', 'burlap']]
       - color: 'light blue'
       - posn: 'upper left'
       - shape: 'SQUARE'
       - texture: 'burlap'
       [0]:
         ['shape', 'SQUARE']
       [1]:
         ['posn', 'upper left']
       [2]:
         ['color', 'light blue']
       [3]:
         ['texture', 'burlap']

       >>> print(result['shape'])
       SQUARE
       >>> print(result.shape)  # object attribute access works too
       SQUARE
       >>> print(result.as_dict())
       {'shape': 'SQUARE', 'posn': 'upper left', 'color': 'light blue', 'texture': 'burlap'}
    """
    return Dict(OneOrMore(Group(key + value)))


def dictOf(key, value):
    """Helper to easily and clearly define a dictionary by specifying
    the respective patterns for the key and value.  Takes care of
    defining the :class:`Dict`, :class:`ZeroOrMore`, and
    :class:`Group` tokens in the proper order.  The key pattern
    can include delimiting markers or punctuation, as long as they are
    suppressed, thereby leaving the significant key text.  The value
    pattern can include named results, so that the :class:`Dict` results
    can include named token fields.

    Example::

        text = "shape: SQUARE posn: upper left color: light blue texture: burlap"
        attr_expr = (label + Suppress(':') + OneOrMore(data_word, stopOn=label).setParseAction(' '.join))
        print(OneOrMore(attr_expr).parseString(text).dump())

        attr_label = label
        attr_value = Suppress(':') + OneOrMore(data_word, stopOn=label).setParseAction(' '.join)

        # similar to Dict, but simpler call format
        result = dictOf(attr_label, attr_value).parseString(text)
        print(result.dump())
        print(result['shape'])
        print(result.shape)  # object attribute access works too
        print(result.asDict())

    prints::

        [['shape', 'SQUARE'], ['posn', 'upper left'], ['color', 'light blue'], ['texture', 'burlap']]
        - color: light blue
        - posn: upper left
        - shape: SQUARE
        - texture: burlap
        SQUARE
        SQUARE
        {'color': 'light blue', 'shape': 'SQUARE', 'posn': 'upper left', 'texture': 'burlap'}
    """
    return Dict(OneOrMore(Group(key + value)))

