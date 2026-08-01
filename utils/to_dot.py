
def to_dot(nodes):
    lines = ["digraph GraphName {", "node [shape=rect];", 'rankdir=LR;']
    for i, n in enumerate(nodes):
        lines.append(f'{i} [label={escape(n.label)}, color={"red" if n.root else "black"}];')

    for i, f in enumerate(nodes):
        for label, j in f.referrents:
            lines.append(f'{i} -> {j} [label = {escape(label)}]')
    lines.append("}\n")
    return '\n'.join(lines)

