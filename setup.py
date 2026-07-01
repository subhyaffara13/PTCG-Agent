from setuptools import setup
try:
    from pybind11.setup_helpers import Pybind11Extension, build_ext
except ImportError:
    # If pybind11 is not yet installed in the environment, fallback to standard Extension
    from setuptools import Extension as Pybind11Extension
    from setuptools.command.build_ext import build_ext

ext_modules = [
    Pybind11Extension(
        "ptcg_core",
        [
            "src/bindings.cpp",
            "src/ptcg_simulator.cpp",
            "src/cpp_mcts.cpp",
        ],
        cxx_std=17,
    ),
]

setup(
    name="ptcg_core",
    version="1.0.0",
    author="TCG Expert",
    description="High-performance Pokemon TCG simulator and MCTS engine in C++",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.7",
)
