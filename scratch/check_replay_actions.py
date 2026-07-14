import json
import glob
import os

for f in glob.glob('*replay*.json')[:3]:
    print(f"\nGame {os.path.basename(f)}")
    try:
        data = json.load(open(f, encoding='utf-8'))
        steps = data.get('steps', [])
        for step in steps[-15:]:
            if isinstance(step, list) and len(step) > 0:
                p0 = step[0]
                p1 = step[1] if len(step) > 1 else {}
                turn = p0.get('observation', {}).get('turn', 0)
                a0 = p0.get('action')
                a1 = p1.get('action')
                if a0 is not None or a1 is not None:
                    print(f"  Turn {turn}: P0 Action -> {a0} | P1 Action -> {a1}")
                if p0.get('status') != 'ACTIVE' or p1.get('status') != 'ACTIVE':
                    print(f"  Status: P0 {p0.get('status')}, P1 {p1.get('status')}")
    except Exception as e:
        print(f"Error parsing {f}: {e}")
