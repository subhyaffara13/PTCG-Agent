
def hexdump(octets):
    return ' '.join(
        ['%s%.2X' % (n % 16 == 0 and ('\n%.5d: ' % n) or '', x)
         for n, x in zip(range(len(octets)), octets)]
    )

