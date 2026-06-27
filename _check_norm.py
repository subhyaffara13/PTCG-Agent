import unicodedata, re

def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"[^a-z0-9']+", " ", text.lower())
    return text.strip()

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
