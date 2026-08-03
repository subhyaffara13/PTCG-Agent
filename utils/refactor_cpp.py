import re

def refactor_cpp(filepath):
    with open(filepath, encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')
    total = len(lines)
    if total <= 100:
        return False

    print(f"  {filepath.name} ({total} lines)...", end='')

    funcs = find_functions(text)
    if not funcs:
        print(" -> no functions found, skipping")
        return False

    first_func_line = funcs[0][1]

    # Extract global variables from preamble
    globals_list = extract_globals(lines, first_func_line)

    # Check if there are cross-file issues
    has_static_funcs = any(f[4] for f in funcs)
    has_globals = bool(globals_list)

    # Check if cross-file group is needed
    # Group functions
    groups = []
    current = []
    cur_size = 0
    for f in funcs:
        size = f[2] - f[1]
        if cur_size + size > TARGET and current:
            groups.append(current)
            current = [f]
            cur_size = size
        else:
            current.append(f)
            cur_size += size
    if current:
        groups.append(current)

    if len(groups) <= 1:
        print(f" -> only 1 group ({len(funcs)} funcs), skipping")
        return False

    needs_internal_header = has_static_funcs or has_globals

    # Build internal header
    stem = filepath.stem
    internal_header = stem + '_internal.h'
    header_lines = [
        f'#ifndef {stem.upper()}_INTERNAL_H_',
        f'#define {stem.upper()}_INTERNAL_H_',
        '',
    ]
    orig_header_path = filepath.parent / (stem + '.h')
    if orig_header_path.exists():
        header_lines.append(f'#include "{stem}.h"')
    header_lines.append('')

    if has_globals:
        header_lines.append('// Global variables (defined in first sub-file)')
        for type_str, name, orig_line in globals_list:
            header_lines.append(f'extern {type_str} {name};')
        header_lines.append('')

    if has_static_funcs:
        decls = extract_static_func_decls(funcs)
        if decls:
            header_lines.append('// Function declarations (was static in original)')
            for name, decl in decls:
                header_lines.append(decl)
            header_lines.append('')

    header_lines.append('#endif')
    header_content = '\n'.join(header_lines)

    # Write sub-files
    sub_files = []
    for i, group in enumerate(groups):
        names = [f[0] for f in group]
        pn = names[0] if len(names) == 1 else '_'.join(names[:3])
        pn = re.sub(r'[^a-zA-Z0-9_]', '_', pn).lower()[:60]
        if not pn or pn[0].isdigit():
            pn = f"part_{i+1:02d}"

        sub_name = stem + '_' + pn + '.cpp'
        group_has_static = any(f[4] for f in group)

        sub_lines = []
        # Include original header
        orig_header = stem + '.h'
        if (filepath.parent / orig_header).exists():
            sub_lines.append(f'#include "{orig_header}"')
        if needs_internal_header:
            sub_lines.append(f'#include "{internal_header}"')
        # Other includes
        for l in lines[:first_func_line]:
            if l.strip().startswith('#include'):
                inc = l.strip()
                if orig_header not in inc:
                    sub_lines.append(inc)
        sub_lines.append('')

        # Add global variable definitions in the first sub-file (without 'static')
        if i == 0 and has_globals:
            sub_lines.append('// Global variable definitions')
            for type_str, name, orig_line in globals_list:
                clean_def = re.sub(r'^\s*static\s+', '', orig_line)
                sub_lines.append(clean_def)
            sub_lines.append('')

        for f in group:
            ft = f[3]
            if group_has_static:
                ft = re.sub(r'^\s*static\s+', '  ', ft, flags=re.MULTILINE)
            sub_lines.append(ft)

        content = '\n'.join(sub_lines)
        sub_files.append((sub_name, content))

    shutil.copy2(filepath, str(filepath) + '.bak')

    # Write internal header if needed
    if needs_internal_header:
        (filepath.parent / internal_header).write_text(header_content, encoding='utf-8')

    for sub_name, sub_content in sub_files:
        (filepath.parent / sub_name).write_text(sub_content, encoding='utf-8')

    # Update CMakeLists.txt
    update_cmakelists(filepath, sub_files)
    filepath.unlink()

    print(f" -> {len(sub_files)} files" + (" + header" if needs_internal_header else ""))
    return True

