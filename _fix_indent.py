"""Fix indentation errors in Python files where method bodies lost one indent level."""
import os, re, ast

def first_indent(line):
    return len(line) - len(line.lstrip())

def fix_file(path):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip('\n')
        indent = first_indent(line)
        prev_line = new_lines[-1].rstrip('\n') if new_lines else ''

        # Check if previous line is a def/class/if/for/while/try/with ending with ':'
        # and current line has the SAME indentation (should be MORE)
        if new_lines and prev_line.rstrip().endswith(':'):
            prev_indent = first_indent(new_lines[-1])
            # Keywords that introduce an indented block
            prev_stripped = prev_line.strip()
            is_block_introducer = (
                prev_stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'with ', 'except ', 'finally:', 'else:', 'elif '))
                or prev_stripped.endswith('):')  # method def
                or prev_stripped == ':'
            )
            if is_block_introducer and indent == prev_indent:
                # Body should be indented 4 more spaces
                new_lines.append(' ' * (indent + 4) + stripped.lstrip() + '\n')
                changed = True
                i += 1
                continue

        new_lines.append(line)
        i += 1

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

excl = {'.venv','submission','.git','scratch','__pycache__'}
fixed = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in excl]
    for f in files:
        if not f.endswith('.py'):
            continue
        if fix_file(os.path.join(root, f)):
            fixed += 1

print(f'Fixed {fixed} files')

# Verify
import py_compile
errors = 0
total = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in excl]
    for f in files:
        if not f.endswith('.py'):
            continue
        total += 1
        path = os.path.join(root, f)
        try:
            py_compile.compile(path, doraise=True)
        except py_compile.PyCompileError:
            errors += 1
print(f'Checked {total} files, {errors} still broken')
