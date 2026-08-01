
def check_examples():
    example_files = sorted(glob.glob('../../examples/*.cpp'))
    markdown_files = sorted(glob.glob('**/*.md', recursive=True))

    # check if every example file is used in at least one markdown file
    for example_file in example_files:
        example_file = os.path.join('examples', os.path.basename(example_file))

        found = False
        for markdown_file in markdown_files:
            content = ' '.join(open(markdown_file).readlines())
            if example_file in content:
                found = True
                break

        if not found:
            report('examples/missing', f'{example_file}', 'example file is not used in any documentation file')

