
def modify_python(content: str, change_type: str) -> tuple[str, list[int], str]:
    # verify AST correctness
    ast.parse(content)
    lines = content.splitlines()
    modified = False
    lines_modified = []
    desc = ""
    
    for idx, line in enumerate(lines):
        if "threshold" in line.lower() and "=" in line and not modified:
            parts = line.split("=")
            try:
                val = float(parts[1].strip())
                lines[idx] = f"{parts[0]}= {val + 0.1}"
                lines_modified.append(idx + 1)
                desc = f"Incremented logic threshold parameter on line {idx + 1}"
                modified = True
            except ValueError:
                pass
    
    if not modified:
        lines.append(f"\n# BuilderAgent: Adjusted {change_type} threshold parameters")
        lines_modified = [len(lines)]
        desc = f"Appended {change_type} adjustment marker to bottom of file"
        
    return "\n".join(lines), lines_modified, desc

