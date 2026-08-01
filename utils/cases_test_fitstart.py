
def cases_test_fitstart():
    for distname, shapes in dict(distcont).items():
        if (not isinstance(distname, str) or
                distname in {'studentized_range', 'recipinvgauss'}):  # slow
            continue
        yield distname, shapes

