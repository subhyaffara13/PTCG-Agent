"""Fix indentation errors in Python files where method bodies lost one indent level."""
import os, re, ast

from utils.first_indent import first_indent

from utils.fix_file import fix_file

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
