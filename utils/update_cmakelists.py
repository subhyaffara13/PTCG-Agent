
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

