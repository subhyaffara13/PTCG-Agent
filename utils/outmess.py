import sys

def outmess(t):
    if options.get('verbose', 1):
        sys.stdout.write(t)


def outmess(line, flag=1):
    global filepositiontext

    if not verbose:
        return
    if not quiet:
        if flag:
            sys.stdout.write(filepositiontext)
        sys.stdout.write(line)

