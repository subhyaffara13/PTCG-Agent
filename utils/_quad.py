
def _quad(func,a,b,args,full_output,epsabs,epsrel,limit,points):
    infbounds = 0
    if (b != np.inf and a != -np.inf):
        pass   # standard integration
    elif (b == np.inf and a != -np.inf):
        infbounds = 1
        bound = a
    elif (b == np.inf and a == -np.inf):
        infbounds = 2
        bound = 0     # ignored
    elif (b != np.inf and a == -np.inf):
        infbounds = -1
        bound = b
    else:
        raise RuntimeError("Infinity comparisons don't work for you.")

    if points is None:
        if infbounds == 0:
            return _quadpack._qagse(func,a,b,args,full_output,epsabs,epsrel,limit)
        else:
            return _quadpack._qagie(func, bound, infbounds, args, full_output, 
                                    epsabs, epsrel, limit)
    else:
        if infbounds != 0:
            raise ValueError("Infinity inputs cannot be used with break points.")
        else:
            #Duplicates force function evaluation at singular points
            the_points = np.unique(points)
            the_points = the_points[a < the_points]
            the_points = the_points[the_points < b]
            the_points = np.concatenate((the_points, (0., 0.)))
            return _quadpack._qagpe(func, a, b, the_points, args, full_output,
                                    epsabs, epsrel, limit)

