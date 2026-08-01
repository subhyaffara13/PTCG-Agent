
def get_code_generator(language, project=None, standard=None, printer = None):
    if language == 'C':
        if standard is None:
            pass
        elif standard.lower() == 'c89':
            language = 'C89'
        elif standard.lower() == 'c99':
            language = 'C99'
    CodeGenClass = {"C": CCodeGen, "C89": C89CodeGen, "C99": C99CodeGen,
                    "F95": FCodeGen, "JULIA": JuliaCodeGen,
                    "OCTAVE": OctaveCodeGen,
                    "RUST": RustCodeGen}.get(language.upper())
    if CodeGenClass is None:
        raise ValueError("Language '%s' is not supported." % language)
    return CodeGenClass(project, printer)

