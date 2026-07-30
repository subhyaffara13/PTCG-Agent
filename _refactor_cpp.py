"""Split large C++ files into ~50-line modules with proper cross-file handling."""
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

SKIP_WORDS = {'if', 'else', 'while', 'for', 'switch', 'catch', 'try', 'case', 'return',
              'delete', 'new', 'sizeof', 'throw', 'template', 'class', 'struct',
              'enum', 'namespace', 'using', 'typedef', 'public:', 'private:', 'protected:'}

def find_closing_brace(lines, start):
    depth = 0
    for i in range(start, len(lines)):
        for c in lines[i]:
            if c == '{': depth += 1
            elif c == '}': depth -= 1
        if depth == 0:
            return i + 1
    return len(lines)

def merge_sig_lines(lines, start):
    merged = ''
    paren_depth = 0
    i = start
    while i < len(lines):
        l = lines[i]
        clean = l.split('//')[0]
        merged += ' ' + clean.strip() if merged else clean.strip()
        for c in clean:
            if c == '(': paren_depth += 1
            elif c == ')': paren_depth -= 1
        if paren_depth == 0:
            if '{' in clean:
                return merged, i + 1
            next_i = i + 1
            while next_i < len(lines) and not lines[next_i].strip():
                next_i += 1
            if next_i < len(lines) and '{' in lines[next_i].split('//')[0]:
                merged += ' {\n'
                return merged, next_i + 1
        i += 1
    return None, len(lines)

def extract_globals(lines, first_func_line):
    """Extract global variable declarations from the preamble."""
    globals_list = []
    for line in lines[:first_func_line]:
        stripped = line.strip()
        # Match: [static] type name = ... ;
        if stripped.startswith('static ') and '=' in stripped and stripped.rstrip().endswith(';'):
            # Get text before '='
            before_eq = stripped.split('=')[0].strip()
            # Remove 'static'
            if before_eq.startswith('static '):
                before_eq = before_eq[7:].strip()
            # Split into words - last word is the variable name
            words = before_eq.split()
            if len(words) >= 2:
                name = words[-1].rstrip('*&')
                type_str = ' '.join(words[:-1])
                globals_list.append((type_str, name, stripped))
    return globals_list

def extract_static_func_decls(funcs):
    """Get declarations for static functions that are called across sub-files."""
    # funcs is list of (name, start, end, text, is_static)
    # We need to know which static functions are called by non-static functions
    # For simplicity, declare all static functions in the internal header
    decls = []
    for f in funcs:
        if f[4]:  # is_static
            # Extract signature (first line up to {)
            text = f[3]
            first_line = text.split('\n')[0]
            # Remove { at end
            sig = first_line.rstrip()
            if sig.endswith('{'):
                sig = sig[:-1].strip()
            # Replace leading 'static ' with nothing
            sig = re.sub(r'^static\s+', '', sig)
            decls.append((f[0], sig + ';'))
    return decls

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

def update_cmakelists(original_path, sub_files):
    cmake_path = ROOT / 'CMakeLists.txt'
    if not cmake_path.exists():
        return

    text = cmake_path.read_text(encoding='utf-8')
    orig_name = str(original_path.relative_to(ROOT)).replace('\\', '/')

    lines = text.split('\n')
    new_lines = []
    replaced = False
    for line in lines:
        if not replaced and orig_name in line and '#' not in line.split(orig_name)[0]:
            new_lines.append(f'    src/{sub_files[0][0]}')
            for sf in sub_files[1:]:
                new_lines.append(f'    src/{sf[0]}')
            replaced = True
        else:
            new_lines.append(line)

    cmake_path.write_text('\n'.join(new_lines), encoding='utf-8')

def main():
    src_dir = ROOT / 'src'
    files = sorted(src_dir.glob("*.cpp"))
    count = 0
    for f in files:
        try:
            if refactor_cpp(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.name}: {e}")
            import traceback; traceback.print_exc()
    print(f"\nProcessed {count}/{len(files)} files.")

if __name__ == '__main__':
    main()
