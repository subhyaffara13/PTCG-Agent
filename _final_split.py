"""Final pass: split remaining files with single large defs by extracting methods/blocks."""
import ast
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

def _make_mod_name(names):
    if not names: return "part"
    base = names[0] if len(names) == 1 else '_'.join(names[:3])
    base = ''.join(c for c in base if c.isalnum() or c == '_').lower()[:60]
    if not base or base[0].isdigit(): base = "part"
    return base

def split_large_function(source, lines, node):
    """Split a large function (>50 lines) by extracting block-level sections."""
    name = node.name
    f_start = node.lineno - 1
    f_end = node.end_lineno
    
    # Get the function's body (statements at top level of function)
    body = node.body
    
    # Find major blocks that can be extracted
    # Look for try/except, if/elif/else, for, while blocks at top level
    blocks = []
    other_stmts = []
    
    for stmt in body:
        line_len = stmt.end_lineno - stmt.lineno
        if line_len > 20:
            blocks.append(stmt)
        else:
            other_stmts.append(stmt)
    
    if not blocks:
        return None  # Can't split
    
    # Extract each block as a helper function
    helpers = []
    for i, block in enumerate(blocks):
        helper_name = f"_{name}_{i}"
        helper_text = node_text(block, lines)
        # Build the helper function
        h_func = f"def {helper_name}():\n"
        for line in helper_text.splitlines(keepends=True):
            h_func += '    ' + line
        helpers.append((helper_name, h_func.rstrip() + '\n'))
    
    # Build replacement function with calls to helpers
    repl_func = node_text(node, lines).splitlines(keepends=True)[0].rstrip() + ':\n'
    indent = '    '
    
    # Add other stmts first
    for stmt in other_stmts:
        repl_func += indent + node_text(stmt, lines).rstrip()
    
    # Add calls to helpers where the blocks were
    for i, (hn, ht) in enumerate(helpers):
        repl_func += indent + f'{hn}()\n'
    
    return repl_func, helpers

def node_text(node, lines):
    return ''.join(lines[node.lineno - 1:node.end_lineno])

def split_large_class(source, lines, node):
    """Split a large class by extracting methods to helper functions."""
    name = node.name
    body = node.body
    
    methods = [n for n in body if isinstance(n, ast.FunctionDef)]
    other_items = [n for n in body if not isinstance(n, ast.FunctionDef)]
    
    # Find big methods
    big_methods = []
    small_methods = []
    for m in methods:
        m_len = m.end_lineno - m.lineno
        if m_len > 15:
            big_methods.append(m)
        else:
            small_methods.append(m)
    
    if not big_methods:
        return None
    
    # Build helpers
    helpers = []
    for m in big_methods:
        m_text = node_text(m, lines)
        helper_name = f"_{m.name}"
        # Convert method to function with self as first param
        # Get the method signature
        m_lines = m_text.splitlines(keepends=True)
        sig = m_lines[0].rstrip()
        # Replace def method_name(self, ...) with def _method_name(self, ...)
        sig = sig.replace(f'def {m.name}', f'def {helper_name}', 1)
        body_text = ''.join(m_lines[1:])
        h_func = sig + ':\n' + body_text
        helpers.append((helper_name, h_func))
        
        # Get args without self for the call
        args = [a.arg for a in m.args.args if a.arg != 'self']
        args += [a.arg for a in m.args.kwonlyargs]
        call_args = ', '.join(['self'] + args)
        
    # Build replacement class text
    class_line = node_text(node, lines).splitlines(keepends=True)[0].rstrip()
    repl = class_line + ':\n'
    indent = '    '
    
    for item in other_items:
        repl += indent + node_text(item, lines).rstrip() + '\n'
    
    for m in small_methods:
        repl += indent + node_text(m, lines).rstrip() + '\n'
    
    for m in big_methods:
        args = [a.arg for a in m.args.args if a.arg != 'self']
        args += [a.arg for a in m.args.kwonlyargs]
        call_args = ', '.join(['self'] + args)
        # Write stub method
        repl += indent + f'def {m.name}(self, {", ".join(args)}):\n'
        repl += indent * 2 + f'return _{m.name}({call_args})\n'
        repl += '\n'
    
    return repl, helpers


def refactor_file(filepath):
    """Handle a single file with a large def."""
    with open(filepath, encoding='utf-8') as f:
        source = f.read()
    lines = source.splitlines(keepends=True)
    total = len(lines)
    if total <= TARGET:
        return False
    
    print(f"  {filepath.relative_to(ROOT)} ({total} lines)...", end='')
    
    tree = ast.parse(source)
    
    def_nodes = [n for n in ast.iter_child_nodes(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    
    if not def_nodes:
        print(" no defs")
        return False
    
    # Check if any single def is >50 lines
    large_defs = []
    for n in def_nodes:
        dsize = n.end_lineno - n.lineno
        if dsize > TARGET:
            large_defs.append(n)
    
    if not large_defs:
        # No def is individually large, but file is >50 lines
        # Try splitting at def level
        print(" multi-def, handle via grouping")
        return False
    
    # We have a single def >50 lines - try to split it
    node = large_defs[0]
    parent = filepath.parent
    is_prefixed = filepath.name.startswith('_')
    
    result = None
    if isinstance(node, ast.FunctionDef):
        result = split_large_function(source, lines, node)
    elif isinstance(node, ast.ClassDef):
        result = split_large_class(source, lines, node)
    
    if result is None:
        print(" can't split")
        return False
    
    repl_text, helpers = result
    
    # Write the helper to a _prefixed file
    base_name = filepath.stem.replace('_', '', 1) if is_prefixed else filepath.stem
    helper_mod = f"_{base_name}_helpers"
    
    helper_lines = []
    m_names = []
    for hn, ht in helpers:
        # Figure out what imports this helper needs
        helper_lines.append(ht + '\n\n')
        m_names.append(hn)
    
    (parent / f"{helper_mod}.py").write_text(''.join(helper_lines), encoding='utf-8')
    
    # Rewrite the original file
    # Get the pre-import nodes
    shared_nodes = [n for n in ast.iter_child_nodes(tree) if not isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    pre_import = ''.join(node_text(n, lines) for n in shared_nodes).rstrip()
    
    if is_prefixed:
        # The file is already a _prefixed sub-module of a package shim
        # We need to rewrite it with import + replacement + helpers
        # But also update the shim that imports from this file
        new_content = pre_import + '\n\n'
        if m_names:
            new_content += f"from .{helper_mod} import {', '.join(m_names)}\n"
        new_content += '\n'
        new_content += repl_text
        filepath.write_text(new_content, encoding='utf-8')
    else:
        # Standalone file or package file
        new_content = pre_import + '\n\n'
        if m_names:
            # Import from the helper module (relative or absolute)
            new_content += f"from .{helper_mod} import {', '.join(m_names)}\n"
        new_content += '\n'
        new_content += repl_text
        # Save .bak
        bak_path = str(filepath) + '.bak'
        if not filepath.with_suffix('.py.bak').exists():
            shutil.copy2(filepath, bak_path)
        filepath.write_text(new_content, encoding='utf-8')
    
    print(f" -> extracted {len(helpers)} helpers to {helper_mod}.py")
    return True

def main():
    files = []
    for d in ['distributed', 'router', 'tests', 'run_guided_helpers', 'numpy_forward', 'run_audit_pipeline']:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                files.append(f)
    
    count = 0
    for f in sorted(files):
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            if lines <= TARGET:
                continue
            if refactor_file(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.relative_to(ROOT)}: {e}")
            import traceback; traceback.print_exc()
    
    print(f"\nDone. {count} files further refactored.")

if __name__ == '__main__':
    main()
