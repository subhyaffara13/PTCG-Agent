
def test_categories():
    from sympy.categories import (Object, IdentityMorphism,
                                  NamedMorphism, Category, Diagram,
                                  DiagramGrid)

    A1 = Object("A1")
    A2 = Object("A2")
    A3 = Object("A3")

    f1 = NamedMorphism(A1, A2, "f1")
    f2 = NamedMorphism(A2, A3, "f2")
    id_A1 = IdentityMorphism(A1)

    K1 = Category("K1")

    assert latex(A1) == r"A_{1}"
    assert latex(f1) == r"f_{1}:A_{1}\rightarrow A_{2}"
    assert latex(id_A1) == r"id:A_{1}\rightarrow A_{1}"
    assert latex(f2*f1) == r"f_{2}\circ f_{1}:A_{1}\rightarrow A_{3}"

    assert latex(K1) == r"\mathbf{K_{1}}"

    d = Diagram()
    assert latex(d) == r"\emptyset"

    d = Diagram({f1: "unique", f2: S.EmptySet})
    assert latex(d) == r"\left\{ f_{2}\circ f_{1}:A_{1}" \
        r"\rightarrow A_{3} : \emptyset, \  id:A_{1}\rightarrow " \
        r"A_{1} : \emptyset, \  id:A_{2}\rightarrow A_{2} : " \
        r"\emptyset, \  id:A_{3}\rightarrow A_{3} : \emptyset, " \
        r"\  f_{1}:A_{1}\rightarrow A_{2} : \left\{unique\right\}, " \
        r"\  f_{2}:A_{2}\rightarrow A_{3} : \emptyset\right\}"

    d = Diagram({f1: "unique", f2: S.EmptySet}, {f2 * f1: "unique"})
    assert latex(d) == r"\left\{ f_{2}\circ f_{1}:A_{1}" \
        r"\rightarrow A_{3} : \emptyset, \  id:A_{1}\rightarrow " \
        r"A_{1} : \emptyset, \  id:A_{2}\rightarrow A_{2} : " \
        r"\emptyset, \  id:A_{3}\rightarrow A_{3} : \emptyset, " \
        r"\  f_{1}:A_{1}\rightarrow A_{2} : \left\{unique\right\}," \
        r" \  f_{2}:A_{2}\rightarrow A_{3} : \emptyset\right\}" \
        r"\Longrightarrow \left\{ f_{2}\circ f_{1}:A_{1}" \
        r"\rightarrow A_{3} : \left\{unique\right\}\right\}"

    # A linear diagram.
    A = Object("A")
    B = Object("B")
    C = Object("C")
    f = NamedMorphism(A, B, "f")
    g = NamedMorphism(B, C, "g")
    d = Diagram([f, g])
    grid = DiagramGrid(d)

    assert latex(grid) == r"\begin{array}{cc}" + "\n" \
        r"A & B \\" + "\n" \
        r" & C " + "\n" \
        r"\end{array}" + "\n"


def test_categories():
    from sympy.categories import (Object, NamedMorphism,
        IdentityMorphism, Category)

    A = Object("A")
    B = Object("B")

    f = NamedMorphism(A, B, "f")
    id_A = IdentityMorphism(A)

    K = Category("K")

    assert str(A) == 'Object("A")'
    assert str(f) == 'NamedMorphism(Object("A"), Object("B"), "f")'
    assert str(id_A) == 'IdentityMorphism(Object("A"))'

    assert str(K) == 'Category("K")'


def test_categories():
    from sympy.categories import (Object, IdentityMorphism,
        NamedMorphism, Category, Diagram, DiagramGrid)

    A1 = Object("A1")
    A2 = Object("A2")
    A3 = Object("A3")

    f1 = NamedMorphism(A1, A2, "f1")
    f2 = NamedMorphism(A2, A3, "f2")
    id_A1 = IdentityMorphism(A1)

    K1 = Category("K1")

    assert pretty(A1) == "A1"
    assert upretty(A1) == "A₁"

    assert pretty(f1) == "f1:A1-->A2"
    assert upretty(f1) == "f₁:A₁——▶A₂"
    assert pretty(id_A1) == "id:A1-->A1"
    assert upretty(id_A1) == "id:A₁——▶A₁"

    assert pretty(f2*f1) == "f2*f1:A1-->A3"
    assert upretty(f2*f1) == "f₂∘f₁:A₁——▶A₃"

    assert pretty(K1) == "K1"
    assert upretty(K1) == "K₁"

    # Test how diagrams are printed.
    d = Diagram()
    assert pretty(d) == "EmptySet"
    assert upretty(d) == "∅"

    d = Diagram({f1: "unique", f2: S.EmptySet})
    assert pretty(d) == "{f2*f1:A1-->A3: EmptySet, id:A1-->A1: " \
        "EmptySet, id:A2-->A2: EmptySet, id:A3-->A3: " \
        "EmptySet, f1:A1-->A2: {unique}, f2:A2-->A3: EmptySet}"

    assert upretty(d) == "{f₂∘f₁:A₁——▶A₃: ∅, id:A₁——▶A₁: ∅, " \
        "id:A₂——▶A₂: ∅, id:A₃——▶A₃: ∅, f₁:A₁——▶A₂: {unique}, f₂:A₂——▶A₃: ∅}"

    d = Diagram({f1: "unique", f2: S.EmptySet}, {f2 * f1: "unique"})
    assert pretty(d) == "{f2*f1:A1-->A3: EmptySet, id:A1-->A1: " \
        "EmptySet, id:A2-->A2: EmptySet, id:A3-->A3: " \
        "EmptySet, f1:A1-->A2: {unique}, f2:A2-->A3: EmptySet}" \
        " ==> {f2*f1:A1-->A3: {unique}}"
    assert upretty(d) == "{f₂∘f₁:A₁——▶A₃: ∅, id:A₁——▶A₁: ∅, id:A₂——▶A₂: " \
        "∅, id:A₃——▶A₃: ∅, f₁:A₁——▶A₂: {unique}, f₂:A₂——▶A₃: ∅}" \
        " ══▶ {f₂∘f₁:A₁——▶A₃: {unique}}"

    grid = DiagramGrid(d)
    assert pretty(grid) == "A1  A2\n      \nA3    "
    assert upretty(grid) == "A₁  A₂\n      \nA₃    "

