"""Fix broken generated _prefixed files using text processing."""
import re
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")

def fix_broken_classes(text):
    """Fix broken class/method definitions in generated files."""
    lines = text.splitlines(keepends=True)
    
    # Phase 1: Fix double colons
    fixed = []
    for line in lines:
        # Fix "class X::" or "class X(Y)::"
        line = re.sub(r'^(class\s+\w+(?:\([^)]*\))?)\s*::', r'\1:', line)
        # Fix "def method::" 
        line = re.sub(r'^(def\s+\w+\([^)]*\))\s*::', r'\1:', line)
        fixed.append(line)
    
    # Phase 2: Remove stub return lines like "    return _method(self, ...)"
    text2 = ''.join(fixed)
    text2 = re.sub(r'^(\s*)return _\w+\([^)]*\)\s*\n', '', text2, flags=re.MULTILINE)
    text2 = re.sub(r'^(\s*)return __\w+\([^)]*\)\s*\n', '', text2, flags=re.MULTILINE)
    
    # Phase 3: Find duplicated full method definitions and dedent
    lines2 = text2.splitlines(keepends=True)
    
    # Find where the class head ends and methods begin
    # The broken pattern is:
    # class X:
    <- correct
    #     def method1:   <- this has : (broken) 
    #     return _method(self) <- stub (to delete)
    #     def method2:   <- this has :: (broken)
    #     return _method(self) <- stub (to delete)
    #
    # def method1(...):  <- real full method at wrong indent (4 not 8)
    #     body...
    # def method2(...):  <- real full method at wrong indent
    #     body...
    
    # Strategy: find "def" lines that start with 4 spaces (not 8) - these are the real methods
    # Then rebuild the file with correctly-indented methods
    
    # Find the class definition line
    class_idx = None
    for i, line in enumerate(lines2):
        if re.match(r'^class\s', line):
            class_idx = i
            break
    
    if class_idx is None:
        return text2
    
    # Extract header (everything up to the class definition)  
    header = ''.join(lines2[:class_idx + 1])
    
    # Find all method definitions at 4-space indent (the "real" duplicated ones)
    real_methods = []
    for i, line in enumerate(lines2):
        if re.match(r'^    def\s', line):
            # This is a 4-space method - the real full definition
            # Check if next lines are at 8 spaces
            method_lines = [line]
            j = i + 1
            while j < len(lines2):
                if re.match(r'^\s{4}def\s', lines2[j]) and j != i + 1:
                    break
                if re.match(r'^class\s', lines2[j]):
                    break
                if lines2[j].strip() and not lines2[j].startswith(' ' * 8) and not lines2[j].startswith(' ' * 4):
                    break
                if re.match(r'^\s{4}\w', lines2[j]):
                    method_lines.append(lines2[j])
                elif lines2[j].strip() == '':
                    method_lines.append(lines2[j])
                elif lines2[j].startswith(' ' * 8):
                    method_lines.append(lines2[j])
                elif lines2[j].startswith('\n'):
                    method_lines.append(lines2[j])
                else:
                    break
                j += 1
            real_methods.append(''.join(method_lines))
    
    # Find methods at 8-space indent (these are the original correct methods)
    orig_methods = []
    for i, line in enumerate(lines2):
        if re.match(r'^\s{8}def\s', line) or (re.match(r'^\s+def\s', line) and line.index('d') >= 8):
            # This is a method from the original class body
            method_lines = [line]
            j = i + 1
            indent = len(line) - len(line.lstrip())
            while j < len(lines2):
                stripped = lines2[j].strip()
                if not stripped:
                    method_lines.append(lines2[j])
                elif stripped and (lines2[j].startswith(' ' * indent) or lines2[j].startswith(' ' * (indent + 4))):
                    method_lines.append(lines2[j])
                else:
                    break
                j += 1
            orig_methods.append(''.join(method_lines))
    
    if not orig_methods:
        # Use 4-space methods as fallback
        orig_methods = real_methods
    
    # Rebuild: header + methods at correct indent (8 spaces)
    result = [header.rstrip() + '\n']
    for m_text in orig_methods:
        # The text starts at 8 spaces indent, strip 4 to make it 4
        m_lines = m_text.splitlines(keepends=True)
        for ml in m_lines:
            if ml.strip():
                # Remove 4 leading spaces from the first line (the def)
                # Keep existing indent for body lines
                result.append(ml)
            else:
                result.append(ml)
    
    return ''.join(result)


def process_file(filepath):
    name = filepath.relative_to(ROOT)
    text = filepath.read_text(encoding='utf-8')
    
    # Check if it has the broken pattern
    if '::' not in text:
        return False
    
    fixed = fix_broken_classes(text)
    
    try:
        import ast
        ast.parse(fixed)
    except SyntaxError as e:
        print(f"  {name}: still has syntax error after fix: {e}")
        return False
    
    filepath.write_text(fixed, encoding='utf-8')
    new_lines = len(fixed.splitlines())
    old_lines = len(text.splitlines())
    print(f"  {name}: {old_lines} -> {new_lines} lines (fixed)")
    return True


def main():
    files = []
    for d in ['distributed', 'router', 'tests', 'run_guided_helpers', 'numpy_forward', 'run_audit_pipeline']:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                files.append(f)
    
    # Filter to files with "::" pattern (broken)
    broken = [f for f in files if '::' in f.read_text(encoding='utf-8')]
    
    print(f"Found {len(broken)} files with syntax issues")
    count = 0
    for f in broken:
        try:
            if process_file(f):
                count += 1
        except Exception as e:
            print(f"  ERROR on {f.relative_to(ROOT)}: {e}")
    
    print(f"Fixed {count} files.")

if __name__ == '__main__':
    main()
