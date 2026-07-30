"""Fix syntactically broken generated files and split remaining large files."""
import ast
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

class class_to_parts:
    """Split a large class into sub-modules."""

def is_valid_python(text):
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False

def fix_and_split(filepath):
    """Fix syntax errors in a generated file, then split if >50 lines."""
    raw = filepath.read_text(encoding='utf-8')
    lines = raw.splitlines(keepends=True)
    total = len(lines)
    
    if is_valid_python(raw) and total <= TARGET:
        return False
    
    name = filepath.relative_to(ROOT)
    print(f"  {name} ({total} lines)...", end='')
    
    # Fix the broken class definition patterns
    # Pattern 1: "class X::" -> "class X:"
    fixed = re.sub(r'^(class\s+\w+(?:\([^)]*\))?)\s*::', r'\1:', raw, flags=re.MULTILINE)
    # Pattern 2: "def method(self, args)::" -> "def method(self, args):"
    fixed = re.sub(r'^(def\s+\w+\([^)]*\))\s*::', r'\1:', fixed, flags=re.MULTILINE)
    # Pattern 3: Remove stub lines: "        return _method(self, ...)"
    # These are lines with indentation + "return _"
    fixed = re.sub(r'^(\s*)return _\w+\([^)]*\)\s*\n', '', fixed, flags=re.MULTILINE)
    # Pattern 4: Reindent method bodies (they're at wrong indent)
    # Methods under class get 4+4=8 spaces indent, need 4 spaces
    
    # Check if it's valid now
    if not is_valid_python(fixed):
        # If still broken, try to rebuild from scratch
        # Extract the import header (lines before "class ")
        import_lines = []
        class_line = None
        method_starts = []
        in_class = False
        
        for i, line in enumerate(lines):
            if re.match(r'^class\s', line):
                in_class = True
                class_line = line.rstrip()  # Will be fixed later
            elif in_class and re.match(r'^\s+def\s', line):
                # Only take method if it's a full definition (not a stub)
                if 'return _' in line:
                    continue
                method_starts.append(i)
            elif not in_class:
                if not line.startswith('class'):
                    import_lines.append(line)
        
        if class_line and method_starts:
            # Rebuild the file
            class_name = re.match(r'class\s+(\w+)', class_line).group(1)
            base = re.search(r'\((.*?)\)', class_line)
            class_def = f"class {class_name}:" if not base else f"class {class_name}({base.group(1)}):"
            
            new_lines = list(import_lines)
            new_lines.append(class_def + '\n')
            
            for idx in method_starts:
                method_lines = []
                j = idx
                while j < len(lines) and (j == idx or (lines[j].startswith(' ') and not re.match(r'^\s+\w', lines[j]) or j <= idx)):
                    line = lines[j]
                    if re.match(r'^\s+def\s', line) and 'return _' in line:
                        j += 1
                        continue
                    # Fix indentation: if line starts with 8 spaces, reduce to 4
                    stripped = line.rstrip()
                    if stripped:
                        # Count leading spaces
                        indent = len(line) - len(line.lstrip())
                        if indent >= 8:
                            new_indent = indent - 4
                            line = ' ' * new_indent + line.lstrip()
                    new_lines.append(line)
                    j += 1
                    if j < len(lines) and not lines[j].startswith(' ') and not lines[j].startswith('\n'):
                        break
                    if 'class ' in line:
                        break
                
                # Continue until next method or end
                while j < len(lines):
                    if re.match(r'^\s+def\s', lines[j]) or re.match(r'^class\s', lines[j]):
                        break
                    line = lines[j]
                    stripped = line.rstrip()
                    if stripped:
                        indent = len(line) - len(line.lstrip())
                        if indent >= 8:
                            new_indent = indent - 4
                            line = ' ' * new_indent + line.lstrip()
                    new_lines.append(line)
                    j += 1
            
            fixed = ''.join(new_lines)
    
    if not is_valid_python(fixed):
        print(" -> couldn't fix syntax")
        return False
    
    # Check if fixed version is still >50
    fixed_lines = fixed.splitlines()
    if len(fixed_lines) <= TARGET:
        filepath.write_text(fixed, encoding='utf-8')
        print(f" -> fixed ({len(fixed_lines)} lines, OK)")
        return True
    
    # Need to split further
    # Write fixed version first
    filepath.write_text(fixed, encoding='utf-8')
    
    # Now split the class by extracting methods
    try:
        tree = ast.parse(fixed)
    except SyntaxError:
        print(f" -> syntax error after fix")
        return False
    
    # Find the class def
    classes = [n for n in ast.iter_child_nodes(tree) if isinstance(n, ast.ClassDef)]
    if not classes:
        print(f" -> no class, can't split further")
        return False
    
    cls = classes[0]
    cls_lines = fixed.splitlines(keepends=True)
    
    methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
    big_methods = [m for m in methods if (m.end_lineno - m.lineno) > 15]
    small_methods = [m for m in methods if m not in big_methods]
    
    if not big_methods:
        print(f" -> no large methods to extract")
        return False
    
    parent = filepath.parent
    cls_name = cls.name
    
    # For each big method, extract to a helper
    helpers = []
    for m in big_methods:
        m_name = m.name
        helper_name = f"_{m_name}"
        
        # Get method text
        m_lines = cls_lines[m.lineno - 1:m.end_lineno]
        sig = m_lines[0].rstrip()
        sig = re.sub(r'^(\s*)def\s+' + re.escape(m_name), r'\1def ' + helper_name, sig)
        
        # Build helper function
        body = ''.join(m_lines[1:])
        # Dedent by 4 spaces (from class-level indent)
        body_lines = []
        for bl in body.splitlines(keepends=True):
            if bl.startswith('    '):
                body_lines.append(bl[4:])
            else:
                body_lines.append(bl)
        body = ''.join(body_lines)
        
        h_text = sig + '\n' + body
        helpers.append((helper_name, m_name, h_text))
    
    # Write helpers file
    h_mod_name = f"_{cls_name}_helpers"
    h_lines = []
    h_names = []
    for hn, mn, ht in helpers:
        h_lines.append(ht + '\n\n')
        h_names.append(hn)
    (parent / f"{h_mod_name}.py").write_text(''.join(h_lines), encoding='utf-8')
    
    # Rebuild the class file with stubs
    new_cls = []
    new_cls.append(cls_lines[cls.lineno - 1].rstrip() + '\n')
    
    # Add small methods directly
    for m in small_methods:
        for i in range(m.lineno - 1, m.end_lineno):
            new_cls.append(cls_lines[i])
    
    # Add stubs for big methods
    for hn, mn, ht in helpers:
        args = []
        # Extract method signature
        tree2 = ast.parse(''.join(cls_lines))
        for node in ast.walk(tree2):
            if isinstance(node, ast.FunctionDef) and node.name == mn:
                args = [a.arg for a in node.args.args if a.arg != 'self']
                args += [a.arg for a in node.args.kwonlyargs]
                break
        
        call_args = ', '.join(['self'] + args)
        stub = f"    def {mn}(self, {', '.join(args)}):\n"
        stub += f"        return {hn}({call_args})\n"
        new_cls.append(stub)
        new_cls.append('\n')
    
    # Get imports (everything before the class)
    pre_class = ''.join(cls_lines[:cls.lineno - 1])
    
    new_content = pre_class
    if h_names:
        new_content += f"from .{h_mod_name} import {', '.join(h_names)}\n"
    new_content += '\n'
    new_content += ''.join(new_cls)
    
    filepath.write_text(new_content, encoding='utf-8')
    
    total_new = len(new_content.splitlines())
    print(f" -> fixed & split ({total_new} lines + {h_mod_name}.py)")
    return True


def main():
    files = []
    for d in ['distributed', 'router', 'tests', 'run_guided_helpers', 'numpy_forward', 'run_audit_pipeline']:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                files.append(f)
    
    # Also handle standalone files in tests
    count = 0
    for f in sorted(files):
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            if lines <= TARGET:
                continue
            # Skip files we've already generated as _helpers
            if f.name.endswith('_helpers.py'):
                continue
            if fix_and_split(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.relative_to(ROOT)}: {e}")
    
    print(f"\nDone. {count} files fixed/split.")

if __name__ == '__main__':
    main()
