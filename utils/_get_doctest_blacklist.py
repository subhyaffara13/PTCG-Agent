
def _get_doctest_blacklist():
    '''Get the default blacklist for the doctests'''
    blacklist = []

    blacklist.extend([
        "doc/src/modules/plotting.rst",  # generates live plots
        "doc/src/modules/physics/mechanics/autolev_parser.rst",
        "sympy/codegen/array_utils.py", # raises deprecation warning
        "sympy/core/compatibility.py", # backwards compatibility shim, importing it triggers a deprecation warning
        "sympy/core/trace.py", # backwards compatibility shim, importing it triggers a deprecation warning
        "sympy/galgebra.py", # no longer part of SymPy
        "sympy/parsing/autolev/_antlr/autolevlexer.py", # generated code
        "sympy/parsing/autolev/_antlr/autolevlistener.py", # generated code
        "sympy/parsing/autolev/_antlr/autolevparser.py", # generated code
        "sympy/parsing/latex/_antlr/latexlexer.py", # generated code
        "sympy/parsing/latex/_antlr/latexparser.py", # generated code
        "sympy/plotting/pygletplot/__init__.py", # crashes on some systems
        "sympy/plotting/pygletplot/plot.py", # crashes on some systems
        "sympy/printing/ccode.py", # backwards compatibility shim, importing it breaks the codegen doctests
        "sympy/printing/cxxcode.py", # backwards compatibility shim, importing it breaks the codegen doctests
        "sympy/printing/fcode.py", # backwards compatibility shim, importing it breaks the codegen doctests
        "sympy/testing/randtest.py", # backwards compatibility shim, importing it triggers a deprecation warning
        "sympy/this.py", # prints text
    ])
    # autolev parser tests
    num = 12
    for i in range (1, num+1):
        blacklist.append("sympy/parsing/autolev/test-examples/ruletest" + str(i) + ".py")
    blacklist.extend(["sympy/parsing/autolev/test-examples/pydy-example-repo/mass_spring_damper.py",
                      "sympy/parsing/autolev/test-examples/pydy-example-repo/chaos_pendulum.py",
                      "sympy/parsing/autolev/test-examples/pydy-example-repo/double_pendulum.py",
                      "sympy/parsing/autolev/test-examples/pydy-example-repo/non_min_pendulum.py"])

    if import_module('numpy') is None:
        blacklist.extend([
            "sympy/plotting/experimental_lambdify.py",
            "sympy/plotting/plot_implicit.py",
            "examples/advanced/autowrap_integrators.py",
            "examples/advanced/autowrap_ufuncify.py",
            "examples/intermediate/sample.py",
            "examples/intermediate/mplot2d.py",
            "examples/intermediate/mplot3d.py",
            "doc/src/modules/numeric-computation.rst",
            "doc/src/explanation/best-practices.md",
            "doc/src/tutorials/physics/biomechanics/biomechanical-model-example.rst",
            "doc/src/tutorials/physics/biomechanics/biomechanics.rst",
        ])
    else:
        if import_module('matplotlib') is None:
            blacklist.extend([
                "examples/intermediate/mplot2d.py",
                "examples/intermediate/mplot3d.py"
            ])
        else:
            # Use a non-windowed backend, so that the tests work on CI
            import matplotlib
            matplotlib.use('Agg')

    if ON_CI or import_module('pyglet') is None:
        blacklist.extend(["sympy/plotting/pygletplot"])

    if import_module('aesara') is None:
        blacklist.extend([
            "sympy/printing/aesaracode.py",
            "doc/src/modules/numeric-computation.rst",
        ])

    if import_module('cupy') is None:
        blacklist.extend([
            "doc/src/modules/numeric-computation.rst",
        ])

    if import_module('jax') is None:
        blacklist.extend([
            "doc/src/modules/numeric-computation.rst",
        ])

    if import_module('antlr4') is None:
        blacklist.extend([
            "sympy/parsing/autolev/__init__.py",
            "sympy/parsing/latex/_parse_latex_antlr.py",
        ])

    if import_module('lfortran') is None:
        #throws ImportError when lfortran not installed
        blacklist.extend([
            "sympy/parsing/sym_expr.py",
        ])

    if import_module("scipy") is None:
        # throws ModuleNotFoundError when scipy not installed
        blacklist.extend([
            "doc/src/guides/solving/solve-numerically.md",
            "doc/src/guides/solving/solve-ode.md",
        ])

    if import_module("numpy") is None:
        # throws ModuleNotFoundError when numpy not installed
        blacklist.extend([
                "doc/src/guides/solving/solve-ode.md",
                "doc/src/guides/solving/solve-numerically.md",
        ])

    # disabled because of doctest failures in asmeurer's bot
    blacklist.extend([
        "sympy/utilities/autowrap.py",
        "examples/advanced/autowrap_integrators.py",
        "examples/advanced/autowrap_ufuncify.py"
        ])

    blacklist.extend([
        "sympy/conftest.py", # Depends on pytest
    ])

    # These are deprecated stubs to be removed:
    blacklist.extend([
        "sympy/utilities/tmpfiles.py",
        "sympy/utilities/pytest.py",
        "sympy/utilities/runtests.py",
        "sympy/utilities/quality_unicode.py",
        "sympy/utilities/randtest.py",
    ])

    blacklist = convert_to_native_paths(blacklist)
    return blacklist

