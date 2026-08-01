
def xs_token(s: str) -> str:
    """Make a ``token``, adhering XML spec.

    .. epigraph::
       *token* represents tokenized strings.
       The `·value space· <https://www.w3.org/TR/xmlschema-2/#dt-value-space>`_ of token is the set of strings that do
       not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters, that have no leading or
       trailing spaces (#x20) and that have no internal sequences of two or more spaces.
       The `·lexical space· <https://www.w3.org/TR/xmlschema-2/#dt-lexical-space>`_ of token is the set of strings that
       do not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters, that have no leading or
       trailing spaces (#x20) and that have no internal sequences of two or more spaces.
       The `·base type· <https://www.w3.org/TR/xmlschema-2/#dt-basetype>`_ of token is
       `normalizedString <https://www.w3.org/TR/xmlschema-2/#normalizedString>`_.

       -- the `XML schema spec <http://www.w3.org/TR/xmlschema-2/#token>`_
    """
    return __TOKEN_MULTISTRING_SEARCH.sub(
        __TOKEN_MULTISTRING_REPLACE,
        xs_normalizedString(s).strip())

