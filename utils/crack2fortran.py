
def crack2fortran(block):
    global f2py_version

    pyf = crack2fortrangen(block) + '\n'
    header = """!    -*- f90 -*-
! Note: the context of this file is case sensitive.
"""
    footer = f"""
! This file was auto-generated with f2py (version:{f2py_version}).
! See:
! https://web.archive.org/web/20140822061353/http://cens.ioc.ee/projects/f2py2e
"""
    return header + pyf + footer

