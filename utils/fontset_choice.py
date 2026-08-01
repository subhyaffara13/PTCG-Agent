
def fontset_choice(arg):
    return directives.choice(arg, mathtext.MathTextParser._font_type_mapping)

