
def _fontfile(cls, suffix, texname):
    return cls(find_tex_file(texname + suffix))

