import unicodedata, re

t = "Boss\u2019s Orders"
print(f"Original: {repr(t)}")
t2 = unicodedata.normalize("NFKD", t)
print(f"After NFKD: {repr(t2)} (len={len(t2)})")
for i, ch in enumerate(t2):
    print(f"  [{i}] {repr(ch)} U+{ord(ch):04X}")
