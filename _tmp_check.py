import csv
with open('cb_agents/deck_new.csv') as f:
    total = 0
    for r in csv.DictReader(f):
        c = int(r['count'])
        total += c
        print(f'{r["card_id"]:>4} {r["card_name"][:30]:<30} x{c}')
    print(f'Total: {total}')
