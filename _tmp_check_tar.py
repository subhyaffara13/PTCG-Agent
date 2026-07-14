import tarfile, csv, io
with tarfile.open('submission.tar.gz', 'r:gz') as t:
    f = t.extractfile('deck.csv')
    r = csv.DictReader(io.StringIO(f.read().decode('utf-8')))
    c = 0
    for row in r:
        cnt = int(row['count'])
        c += cnt
        print('%4s %-30s x%d' % (row['card_id'], row['card_name'][:30], cnt))
    print('Total: %d' % c)
