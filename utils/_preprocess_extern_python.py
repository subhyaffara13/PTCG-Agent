
def _preprocess_extern_python(csource):
    # input: `extern "Python" int foo(int);` or
    #        `extern "Python" { int foo(int); }`
    # output:
    #     void __cffi_extern_python_start;
    #     int foo(int);
    #     void __cffi_extern_python_stop;
    #
    # input: `extern "Python+C" int foo(int);`
    # output:
    #     void __cffi_extern_python_plus_c_start;
    #     int foo(int);
    #     void __cffi_extern_python_stop;
    parts = []
    while True:
        match = _r_extern_python.search(csource)
        if not match:
            break
        endpos = match.end() - 1
        #print
        #print ''.join(parts)+csource
        #print '=>'
        parts.append(csource[:match.start()])
        if 'C' in match.group(1):
            parts.append('void __cffi_extern_python_plus_c_start; ')
        else:
            parts.append('void __cffi_extern_python_start; ')
        if csource[endpos] == '{':
            # grouping variant
            closing = csource.find('}', endpos)
            if closing < 0:
                raise CDefError("'extern \"Python\" {': no '}' found")
            if csource.find('{', endpos + 1, closing) >= 0:
                raise NotImplementedError("cannot use { } inside a block "
                                          "'extern \"Python\" { ... }'")
            parts.append(csource[endpos+1:closing])
            csource = csource[closing+1:]
        else:
            # non-grouping variant
            semicolon = csource.find(';', endpos)
            if semicolon < 0:
                raise CDefError("'extern \"Python\": no ';' found")
            parts.append(csource[endpos:semicolon+1])
            csource = csource[semicolon+1:]
        parts.append(' void __cffi_extern_python_stop;')
        #print ''.join(parts)+csource
        #print
    parts.append(csource)
    return ''.join(parts)

