import os
from pathlib import Path


def test_cython_wrapper_compile_flags():
    from sympy.core.relational import Equality
    x, y, z = symbols('x,y,z')
    routine = make_routine("test", Equality(z, x + y))

    code_gen = CythonCodeWrapper(CCodeGen())

    expected = """\
from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize
cy_opts = {'compiler_directives': {'language_level': '3'}}

ext_mods = [Extension(
    'wrapper_module_%(num)s', ['wrapper_module_%(num)s.pyx', 'wrapped_code_%(num)s.c'],
    include_dirs=[],
    library_dirs=[],
    libraries=[],
    extra_compile_args=['-std=c99'],
    extra_link_args=[]
)]
setup(ext_modules=cythonize(ext_mods, **cy_opts))
""" % {'num': CodeWrapper._module_counter}

    temp_dir = tempfile.mkdtemp()
    TmpFileManager.tmp_folder(temp_dir)
    setup_file_path = os.path.join(temp_dir, 'setup.py')

    code_gen._prepare_files(routine, build_dir=temp_dir)
    setup_text = Path(setup_file_path).read_text()
    assert setup_text == expected

    code_gen = CythonCodeWrapper(CCodeGen(),
                                 include_dirs=['/usr/local/include', '/opt/booger/include'],
                                 library_dirs=['/user/local/lib'],
                                 libraries=['thelib', 'nilib'],
                                 extra_compile_args=['-slow-math'],
                                 extra_link_args=['-lswamp', '-ltrident'],
                                 cythonize_options={'compiler_directives': {'boundscheck': False}}
                                 )
    expected = """\
from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize
cy_opts = {'compiler_directives': {'boundscheck': False}}

ext_mods = [Extension(
    'wrapper_module_%(num)s', ['wrapper_module_%(num)s.pyx', 'wrapped_code_%(num)s.c'],
    include_dirs=['/usr/local/include', '/opt/booger/include'],
    library_dirs=['/user/local/lib'],
    libraries=['thelib', 'nilib'],
    extra_compile_args=['-slow-math', '-std=c99'],
    extra_link_args=['-lswamp', '-ltrident']
)]
setup(ext_modules=cythonize(ext_mods, **cy_opts))
""" % {'num': CodeWrapper._module_counter}

    code_gen._prepare_files(routine, build_dir=temp_dir)
    setup_text = Path(setup_file_path).read_text()
    assert setup_text == expected

    expected = """\
from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize
cy_opts = {'compiler_directives': {'boundscheck': False}}
import numpy as np

ext_mods = [Extension(
    'wrapper_module_%(num)s', ['wrapper_module_%(num)s.pyx', 'wrapped_code_%(num)s.c'],
    include_dirs=['/usr/local/include', '/opt/booger/include', np.get_include()],
    library_dirs=['/user/local/lib'],
    libraries=['thelib', 'nilib'],
    extra_compile_args=['-slow-math', '-std=c99'],
    extra_link_args=['-lswamp', '-ltrident']
)]
setup(ext_modules=cythonize(ext_mods, **cy_opts))
""" % {'num': CodeWrapper._module_counter}

    code_gen._need_numpy = True
    code_gen._prepare_files(routine, build_dir=temp_dir)
    setup_text = Path(setup_file_path).read_text()
    assert setup_text == expected

    TmpFileManager.cleanup()

