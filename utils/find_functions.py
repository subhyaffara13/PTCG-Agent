import re

def find_functions(text):
    lines = text.split('\n')
    functions = []
    i = 0
    while i < len(lines):
        l = lines[i]
        stripped = l.strip()
        if not stripped or stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('/*') or stripped == '}':
            i += 1
            continue

        first_word = stripped.split()[0] if stripped.split() else ''
        if first_word in SKIP_WORDS:
            i += 1
            continue

        if stripped.startswith('namespace') and '=' in stripped and stripped.rstrip().endswith(';'):
            i += 1
            continue

        code_line = stripped.split('//')[0].strip()
        if code_line.rstrip().endswith(';'):
            i += 1
            continue

        sig, next_line = merge_sig_lines(lines, i)
        if sig is None:
            i += 1
            continue

        brace_idx = sig.find('{')
        if brace_idx >= 0 and ';' in sig[:brace_idx]:
            i = next_line
            continue

        sig_clean = sig
        for kw in ['static ', 'virtual ', 'inline ', 'explicit ', 'friend ']:
            if sig_clean.startswith(kw):
                sig_clean = sig_clean[len(kw):]

        sig_no_brace = sig_clean.rstrip()
        if sig_no_brace.endswith('{'):
            sig_no_brace = sig_no_brace[:-1].strip()

        paren_idx = sig_no_brace.find('(')
        if paren_idx < 0:
            i = next_line
            continue

        before_paren = sig_no_brace[:paren_idx].strip()
        words = before_paren.split()
        if not words:
            i = next_line
            continue

        name = words[-1]
        if '::' in name:
            simple_name = name.split('::')[-1]
        else:
            simple_name = name

        if not re.match(r'^[A-Za-z_~]\w*$', simple_name):
            i = next_line
            continue

        brace_found = False
        for j in range(i, next_line):
            if '{' in lines[j]:
                func_start = i
                brace_found = True
                break

        if not brace_found:
            i = next_line
            continue

        end = find_closing_brace(lines, func_start)

        if end <= func_start + 1:
            i = next_line
            continue

        func_text = '\n'.join(lines[func_start:end])
        is_static = 'static ' in sig or sig.startswith('static')

        functions.append((simple_name, func_start, end, func_text, is_static))
        i = end

    return functions

