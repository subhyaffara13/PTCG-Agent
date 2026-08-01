
def adder(augend):
    zero = [0]

    def inner(addend):
        return addend + augend + zero[0]
    return inner

