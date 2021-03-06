try:
    # Note the relative import!
    from .action_place_footprints import PlaceFootprintsInCircle
    # Instantiate and register to Pcbnew
    PlaceFootprintsInCircle().register()
except Exception as e:
    import os
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'place_footprints_error.log')
    with open(log_file, 'w') as f:
        f.write(repr(e))
    from .no_wxpython import NoWxpython as PlaceFootprintsInCircle
    PlaceFootprintsInCircle().register()
