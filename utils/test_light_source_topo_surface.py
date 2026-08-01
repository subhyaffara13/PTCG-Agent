
def test_light_source_topo_surface():
    """Shades a DEM using different v.e.'s and blend modes."""
    dem = cbook.get_sample_data('jacksboro_fault_dem.npz')
    elev = dem['elevation']
    dx, dy = dem['dx'], dem['dy']
    # Get the true cellsize in meters for accurate vertical exaggeration
    # Convert from decimal degrees to meters
    dx = 111320.0 * dx * np.cos(dem['ymin'])
    dy = 111320.0 * dy

    ls = mcolors.LightSource(315, 45)
    cmap = cm.gist_earth

    fig, axs = plt.subplots(nrows=3, ncols=3)
    for row, mode in zip(axs, ['hsv', 'overlay', 'soft']):
        for ax, ve in zip(row, [0.1, 1, 10]):
            rgb = ls.shade(elev, cmap, vert_exag=ve, dx=dx, dy=dy,
                           blend_mode=mode)
            ax.imshow(rgb)
            ax.set(xticks=[], yticks=[])

