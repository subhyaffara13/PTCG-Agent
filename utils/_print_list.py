
def _print_list(what):
    if what == 'lexer':
        print()
        print("Lexers:")
        print("~~~~~~~")

        info = []
        for fullname, names, exts, _ in get_all_lexers():
            tup = (', '.join(names)+':', fullname,
                   exts and '(filenames ' + ', '.join(exts) + ')' or '')
            info.append(tup)
        info.sort()
        for i in info:
            print(('* {}\n    {} {}').format(*i))

    elif what == 'formatter':
        print()
        print("Formatters:")
        print("~~~~~~~~~~~")

        info = []
        for cls in get_all_formatters():
            doc = docstring_headline(cls)
            tup = (', '.join(cls.aliases) + ':', doc, cls.filenames and
                   '(filenames ' + ', '.join(cls.filenames) + ')' or '')
            info.append(tup)
        info.sort()
        for i in info:
            print(('* {}\n    {} {}').format(*i))

    elif what == 'filter':
        print()
        print("Filters:")
        print("~~~~~~~~")

        for name in get_all_filters():
            cls = find_filter_class(name)
            print("* " + name + ':')
            print(f"    {docstring_headline(cls)}")

    elif what == 'style':
        print()
        print("Styles:")
        print("~~~~~~~")

        for name in get_all_styles():
            cls = get_style_by_name(name)
            print("* " + name + ':')
            print(f"    {docstring_headline(cls)}")

