# Shared code

- `page.tpl`: the viewer page template
- `build.py`: assembles a flipbook site from orthorectified mosaics (run from a site folder holding `cfg.py`, `cams.py`, `frames.json`, `site.json`)
- `layers.py`: Topographic Wetness Index, canopy height coloring, legacy tree detection
- `overlays.py`: writes the canopy and wetness layers and `legacy_trees.csv` for each site
- `lidar.py`: builds 1 m canopy height models from USGS 3DEP LiDAR tiles
- `stage.py`: makes the flat hosted copy of a site

Python 3 with numpy, opencv, rasterio, geopandas, shapely, pysheds, laspy and Pillow.
