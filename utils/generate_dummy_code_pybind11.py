import random

def generate_dummy_code_pybind11(nclasses=10):
    decl = ""
    bindings = ""

    for cl in range(nclasses):
        decl += f"class cl{cl:03};\n"
    decl += "\n"

    for cl in range(nclasses):
        decl += f"class {cl:03} {{\n"
        decl += "public:\n"
        bindings += f'    py::class_<cl{cl:03}>(m, "cl{cl:03}")\n'
        for fn in range(nfns):
            ret = random.randint(0, nclasses - 1)
            params = [random.randint(0, nclasses - 1) for i in range(nargs)]
            decl += f"    cl{ret:03} *fn_{fn:03}("
            decl += ", ".join(f"cl{p:03} *" for p in params)
            decl += ");\n"
            bindings += f'        .def("fn_{fn:03}", &cl{cl:03}::fn_{fn:03})\n'
        decl += "};\n\n"
        bindings += "        ;\n"

    result = "#include <pybind11/pybind11.h>\n\n"
    result += "namespace py = pybind11;\n\n"
    result += decl + "\n"
    result += "PYBIND11_MODULE(example, m) {\n"
    result += bindings
    result += "}"
    return result

