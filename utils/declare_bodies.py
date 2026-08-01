
def declare_bodies(self, ctx, i, j=None):
    if "{" in ctx.getText():
        if j:
            name1 = ctx.ID().getText().lower() + str(i) + str(j)
        else:
            name1 = ctx.ID().getText().lower() + str(i)
    else:
        name1 = ctx.ID().getText().lower()

    name2 = "body_" + name1
    self.bodies.update({name1: name2})
    masscenter = name2 + "_cm"
    refFrame = name2 + "_f"

    self.symbol_table2.update({name1: name2})
    self.symbol_table2.update({name1 + "o": masscenter})
    self.symbol_table.update({name1 + "1>": refFrame+".x"})
    self.symbol_table.update({name1 + "2>": refFrame+".y"})
    self.symbol_table.update({name1 + "3>": refFrame+".z"})

    self.type2.update({name1: "bodies"})
    self.type2.update({name1+"o": "point"})

    self.write(masscenter + " = " + "_me.Point('" + name1 + "_cm" + "')\n")
    if self.newtonian:
        self.write(masscenter + ".set_vel(" + self.newtonian + ", " + "0)\n")
    self.write(refFrame + " = " + "_me.ReferenceFrame('" + name1 + "_f" + "')\n")
    # We set a dummy mass and inertia here.
    # They will be reset using the setters later in the code anyway.
    self.write(name2 + " = " + "_me.RigidBody('" + name1 + "', " + masscenter + ", " +
                refFrame + ", " + "_sm.symbols('m'), (_me.outer(" + refFrame +
                ".x," + refFrame + ".x)," + masscenter + "))\n")

