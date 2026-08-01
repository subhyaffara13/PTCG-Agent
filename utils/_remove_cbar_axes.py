
def _remove_cbar_axes(ax, cbar):
    """
    Replacement remove method for a colorbar's axes, so that the colorbar is
    properly removed.

    Note we define this at the module level to preserve pickling. A lambda or
    local def within the Colorbar.__init__ method will not work.
    """
    cbar.remove()

