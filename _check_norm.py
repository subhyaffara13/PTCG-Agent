import unicodedata, re

from utils.normalize import normalize

tests = [
    "Boss\u2019s Orders",
    "Boss's Orders",
    "Professor\u2019s Research",
    "Professor's Research",
    "Pok\u00e9 Pad",
    "Pok\u00e9gear 3.0",
    "Iono",
    "Arven",
]
for t in tests:
    n = normalize(t)
    print(f"{repr(t):40s} -> {repr(n)}")
