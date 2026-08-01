
def inertia_func(self, v1, v2, l, frame):

    if self.type2[v1] == "particle":
        l.append("_me.inertia_of_point_mass(" + self.bodies[v1] + ".mass, " + self.bodies[v1] +
                 ".point.pos_from(" + self.symbol_table2[v2] + "), " + frame + ")")

    elif self.type2[v1] == "bodies":
        # Inertia has been defined about center of mass.
        if self.inertia_point[v1] == v1 + "o":
            # Asking point is cm as well
            if v2 == self.inertia_point[v1]:
                l.append(self.symbol_table2[v1] + ".inertia[0]")

            # Asking point is not cm
            else:
                l.append(self.bodies[v1] + ".inertia[0]" + " + " +
                         "_me.inertia_of_point_mass(" + self.bodies[v1] +
                         ".mass, " + self.bodies[v1] + ".masscenter" +
                         ".pos_from(" + self.symbol_table2[v2] +
                         "), " + frame + ")")

        # Inertia has been defined about another point
        else:
            # Asking point is the defined point
            if v2 == self.inertia_point[v1]:
                l.append(self.symbol_table2[v1] + ".inertia[0]")
            # Asking point is cm
            elif v2 == v1 + "o":
                l.append(self.bodies[v1] + ".inertia[0]" + " - " +
                         "_me.inertia_of_point_mass(" + self.bodies[v1] +
                         ".mass, " + self.bodies[v1] + ".masscenter" +
                         ".pos_from(" + self.symbol_table2[self.inertia_point[v1]] +
                         "), " + frame + ")")
            # Asking point is some other point
            else:
                l.append(self.bodies[v1] + ".inertia[0]" + " - " +
                         "_me.inertia_of_point_mass(" + self.bodies[v1] +
                         ".mass, " + self.bodies[v1] + ".masscenter" +
                         ".pos_from(" + self.symbol_table2[self.inertia_point[v1]] +
                         "), " + frame + ")" + " + " +
                         "_me.inertia_of_point_mass(" + self.bodies[v1] +
                         ".mass, " + self.bodies[v1] + ".masscenter" +
                         ".pos_from(" + self.symbol_table2[v2] +
                         "), " + frame + ")")

