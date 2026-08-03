import os
import re
from pathlib import Path


def readfortrancode(ffile, dowithline=show, istop=1):
    """
    Read fortran codes from files and
     1) Get rid of comments, line continuations, and empty lines; lower cases.
     2) Call dowithline(line) on every line.
     3) Recursively call itself when statement \"include '<filename>'\" is met.
    """
    global gotnextfile, filepositiontext, currentfilename, sourcecodeform, strictf77
    global beginpattern, quiet, verbose, dolowercase, include_paths

    if not istop:
        saveglobals = gotnextfile, filepositiontext, currentfilename, sourcecodeform, strictf77,\
            beginpattern, quiet, verbose, dolowercase
    if ffile == []:
        return
    localdolowercase = dolowercase
    # cont: set to True when the content of the last line read
    # indicates statement continuation
    cont = False
    finalline = ''
    ll = ''
    includeline = re.compile(
        r'\s*include\s*(\'|")(?P<name>[^\'"]*)(\'|")', re.I)
    cont1 = re.compile(r'(?P<line>.*)&\s*\Z')
    cont2 = re.compile(r'(\s*&|)(?P<line>.*)')
    mline_mark = re.compile(r".*?'''")
    if istop:
        dowithline('', -1)
    ll, l1 = '', ''
    spacedigits = [' '] + [str(_m) for _m in range(10)]
    filepositiontext = ''
    fin = fileinput.FileInput(ffile, openhook=openhook)
    while True:
        try:
            l = fin.readline()
        except UnicodeDecodeError as msg:
            raise Exception(
                f'readfortrancode: reading {fin.filename()}#{fin.lineno()}'
                f' failed with\n{msg}.\nIt is likely that installing charset_normalizer'
                ' package will help f2py determine the input file encoding'
                ' correctly.')
        if not l:
            break
        if fin.isfirstline():
            filepositiontext = ''
            currentfilename = fin.filename()
            gotnextfile = 1
            l1 = l
            strictf77 = 0
            sourcecodeform = 'fix'
            ext = os.path.splitext(currentfilename)[1]
            if Path(currentfilename).suffix.lower() in COMMON_FIXED_EXTENSIONS and \
                    not (_has_f90_header(l) or _has_fix_header(l)):
                strictf77 = 1
            elif is_free_format(currentfilename) and not _has_fix_header(l):
                sourcecodeform = 'free'
            if strictf77:
                beginpattern = beginpattern77
            else:
                beginpattern = beginpattern90
            outmess(f"\tReading file {currentfilename!r} "
                    f"(format:{sourcecodeform}{',strict' if strictf77 else ''})\n")

        l = l.expandtabs().replace('\xa0', ' ')
        # Get rid of newline characters
        while not l == '':
            if l[-1] not in "\n\r\f":
                break
            l = l[:-1]
        # Do not lower for directives, gh-2547, gh-27697, gh-26681
        is_f2py_directive = False
        # Unconditionally remove comments
        (l, rl) = split_by_unquoted(l, '!')
        l += ' '
        if rl[:5].lower() == '!f2py':  # f2py directive
            l, _ = split_by_unquoted(l + 4 * ' ' + rl[5:], '!')
            is_f2py_directive = True
        if l.strip() == '':  # Skip empty line
            if sourcecodeform == 'free':
                # In free form, a statement continues in the next line
                # that is not a comment line [3.3.2.4^1], lines with
                # blanks are comment lines [3.3.2.3^1]. Hence, the
                # line continuation flag must retain its state.
                pass
            else:
                # In fixed form, statement continuation is determined
                # by a non-blank character at the 6-th position. Empty
                # line indicates a start of a new statement
                # [3.3.3.3^1]. Hence, the line continuation flag must
                # be reset.
                cont = False
            continue
        if sourcecodeform == 'fix':
            if l[0] in ['*', 'c', '!', 'C', '#']:
                if l[1:5].lower() == 'f2py':  # f2py directive
                    l = '     ' + l[5:]
                    is_f2py_directive = True
                else:  # Skip comment line
                    cont = False
                    is_f2py_directive = False
                    continue
            elif strictf77:
                if len(l) > 72:
                    l = l[:72]
            if l[0] not in spacedigits:
                raise Exception('readfortrancode: Found non-(space,digit) char '
                                'in the first column.\n\tAre you sure that '
                                f'this code is in fix form?\n\tline={l!r}')

            if (not cont or strictf77) and (len(l) > 5 and not l[5] == ' '):
                # Continuation of a previous line
                ll = ll + l[6:]
                finalline = ''
                origfinalline = ''
            else:
                r = cont1.match(l)
                if r:
                    l = r.group('line')  # Continuation follows ..
                if cont:
                    ll = ll + cont2.match(l).group('line')
                    finalline = ''
                    origfinalline = ''
                else:
                    # clean up line beginning from possible digits.
                    l = '     ' + l[5:]
                    # f2py directives are already stripped by this point
                    if localdolowercase:
                        finalline = ll.lower()
                    else:
                        finalline = ll
                    origfinalline = ll
                    ll = l

        elif sourcecodeform == 'free':
            if not cont and ext == '.pyf' and mline_mark.match(l):
                l = l + '\n'
                while True:
                    lc = fin.readline()
                    if not lc:
                        errmess(
                            'Unexpected end of file when reading multiline\n')
                        break
                    l = l + lc
                    if mline_mark.match(lc):
                        break
                l = l.rstrip()
            r = cont1.match(l)
            if r:
                l = r.group('line')  # Continuation follows ..
            if cont:
                ll = ll + cont2.match(l).group('line')
                finalline = ''
                origfinalline = ''
            else:
                if localdolowercase:
                    # only skip lowering for C style constructs
                    # gh-2547, gh-27697, gh-26681, gh-28014
                    finalline = ll.lower() if not (is_f2py_directive and iscstyledirective(ll)) else ll
                else:
                    finalline = ll
                origfinalline = ll
                ll = l
            cont = (r is not None)
        else:
            raise ValueError(
                f"Flag sourcecodeform must be either 'fix' or 'free': {repr(sourcecodeform)}")
        filepositiontext = (f'Line #{fin.filelineno() - 1} '
                            f'in {currentfilename}:"{l1}"\n\t')
        m = includeline.match(origfinalline)
        if m:
            fn = m.group('name')
            if os.path.isfile(fn):
                readfortrancode(fn, dowithline=dowithline, istop=0)
            else:
                include_dirs = [
                    os.path.dirname(currentfilename)] + include_paths
                foundfile = 0
                for inc_dir in include_dirs:
                    fn1 = os.path.join(inc_dir, fn)
                    if os.path.isfile(fn1):
                        foundfile = 1
                        readfortrancode(fn1, dowithline=dowithline, istop=0)
                        break
                if not foundfile:
                    outmess(f'readfortrancode: could not find include file {fn!r} '
                            f'in {os.pathsep.join(include_dirs)}. Ignoring.\n')
        else:
            dowithline(finalline)
        l1 = ll
    # Last line should never have an f2py directive anyway
    if localdolowercase:
        finalline = ll.lower()
    else:
        finalline = ll
    origfinalline = ll
    filepositiontext = f'Line #{fin.filelineno() - 1} in {currentfilename}:"{l1}"\n\t'
    m = includeline.match(origfinalline)
    if m:
        fn = m.group('name')
        if os.path.isfile(fn):
            readfortrancode(fn, dowithline=dowithline, istop=0)
        else:
            include_dirs = [os.path.dirname(currentfilename)] + include_paths
            foundfile = 0
            for inc_dir in include_dirs:
                fn1 = os.path.join(inc_dir, fn)
                if os.path.isfile(fn1):
                    foundfile = 1
                    readfortrancode(fn1, dowithline=dowithline, istop=0)
                    break
            if not foundfile:
                outmess(f'readfortrancode: could not find include file {fn!r} '
                        f'in {os.pathsep.join(include_dirs)}. Ignoring.\n')
    else:
        dowithline(finalline)
    filepositiontext = ''
    fin.close()
    if istop:
        dowithline('', 1)
    else:
        gotnextfile, filepositiontext, currentfilename, sourcecodeform, strictf77,\
            beginpattern, quiet, verbose, dolowercase = saveglobals

