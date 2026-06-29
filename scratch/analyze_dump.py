import json
dump = json.load(open('logs/debug_payload_dump.json'))
for t in [0, 1, 8, 9]:
    for s in dump:
        if s['select_type'] == t:
            print(f"Type {t} options (context {s.get('select_context')}):")
            for opt in s['options'][:3]:
                print('  ', opt)
            break
