import os
os.environ['FAST_SIM_MODE'] = 'true'
import json
from collections import Counter
from kaggle_environments import make

env = make('cabt')
steps = env.run(['random', 'random'])

dump = []
for step in steps:
    for i, state in enumerate(step):
        if not state: continue
        obs = state.get('observation', {})
        sel = obs.get('select')
        if sel:
            dump.append({
                'turn': obs.get('current', {}).get('turn', 0),
                'player': i,
                'select_type': sel.get('type'),
                'select_context': sel.get('context'),
                'options': sel.get('option', [])
            })

with open('logs/debug_payload_dump_full.json', 'w') as f:
    json.dump(dump, f, indent=2)
print(f'Simulation ran for {len(steps)} steps.')

types = Counter()
for s in dump:
    types[s['select_type']] += 1
print('Types seen:', types)

for t in types:
    for s in dump:
        if s['select_type'] == t:
            print(f"Type {t} options (context {s.get('select_context')}):")
            for opt in s['options'][:5]:
                print('  ', opt)
            break
