import json
data = json.load(open('skills/card_scoring.json'))
cards = data.get('cards', [])
trainer_names = set()
for c in cards:
    if c.get('card_type') == 'Trainer':
        trainer_names.add(c.get('card_name'))
print(f"Total unique trainer names: {len(trainer_names)}")
for name in sorted(trainer_names):
    print(f"  {name}")
