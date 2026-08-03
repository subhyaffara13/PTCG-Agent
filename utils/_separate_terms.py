from typing import List

def _separate_terms(word: str) -> List[str]:
    """
    >>> _separate_terms("FooBar-foo")
    ['foo', 'bar', 'foo']
    """
    return [w.lower() for w in _CAMEL_CASE_SPLITTER.split(word) if w]

