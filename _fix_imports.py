"""Fix concatenated imports and broken syntax from refactoring agents."""
import re, os, py_compile

fixes = [
    (r'(from \. import [^\n]+?)(import \w+)', r'\1\n\2'),
    (r'(import \w+)(import \w+)', r'\1\n\2'),
    (r'(def \w+\([^)]*\):)\s{4,}(\S)', r'\1\n    \2'),
    (r'(class \w+(?:\([^)]*\))?:)\s{4,}(\S)', r'\1\n    \2'),
    (r'(\d+)([A-Z]\w+\s*=)', r'\1\n\2'),
    (r'("""[^"]*""")import', r'\1\nimport'),
    (r'("""[^"]*""")from', r'\1\nfrom'),
]

excl = {'.venv','submission','.git','scratch','__pycache__'}
fixed = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in excl]
    for f in files:
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        try:
            orig = open(path, encoding='utf-8').read()
        except Exception:
            continue
        new = orig
        for pat, repl in fixes:
            new = re.sub(pat, repl, new)
        if new != orig:
            open(path, 'w', encoding='utf-8').write(new)
            fixed += 1

print(f'Fixed {fixed} files')

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
            if errors <= 5:
                with open(path) as fh:
                    print(f'STILL BROKEN: {path}: {fh.read()[:120]}')
print(f'Checked {total} files, {errors} still broken')
