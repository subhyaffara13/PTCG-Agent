
def xs_normalizedString(s: str) -> str:
    """Make a ``normalizedString``, adhering XML spec.

    .. epigraph::
       *normalizedString* represents white space normalized strings.
       The `·value space· <https://www.w3.org/TR/xmlschema-2/#dt-value-space>`_ of normalizedString is the set of
       strings that do not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters.
       The `·lexical space· <https://www.w3.org/TR/xmlschema-2/#dt-lexical-space>`_ of normalizedString is the set of
       strings that do not contain the carriage return (#xD), line feed (#xA) nor tab (#x9) characters.
       The `·base type· <https://www.w3.org/TR/xmlschema-2/#dt-basetype>`_ of normalizedString is
       `string <https://www.w3.org/TR/xmlschema-2/#string>`_.

       -- the `XML schema spec <http://www.w3.org/TR/xmlschema-2/#normalizedString>`_
    """
    return __NORMALIZED_STRING_FORBIDDEN_SEARCH.sub(
        __NORMALIZED_STRING_FORBIDDEN_REPLACE,
        s)

