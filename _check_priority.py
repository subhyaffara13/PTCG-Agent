import json
import unicodedata
import re

def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\x00-\x7F]+", "", text)
    text = re.sub(r"[^a-z0-9']+", " ", text.lower())
    return text.strip()

priority = [
    "Boss's Orders", "Professor's Research", "Iono", "Arven",
    "Super Rod", "Nest Ball", "Quick Ball", "Level Ball",
    "Switch Cart", "Pal Pad",
]
norm_targets = {normalize(n) for n in priority}
print("Normalized targets:", norm_targets)

data = json.load(open('skills/card_scoring.json'))
cards = data.get('cards', [])
trainer_names = set()
for c in cards:
    if c.get('card_type') == 'Trainer':
        trainer_names.add(c.get('card_name'))

for name in sorted(trainer_names):
    nname = normalize(name)
    if nname in norm_targets:
        print(f"MATCH: {repr(name)} -> {nname}")
    elif nname.startswith("boss") or nname.startswith("professor") or nname.startswith("iono") or nname.startswith("super rod") or nname.startswith("nest ball"):
        print(f"NEAR MISS: {repr(name)} -> {nname}")
