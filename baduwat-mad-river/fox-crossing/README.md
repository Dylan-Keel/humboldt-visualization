# Fox Crossing Flipbook

A registered aerial image time series for Humboldt County parcel APN 314-213-030 (37 acres) and the 1,516-acre unnamed drainage it sits in, which meets the Mad River (Baduwa't) at its northeast corner.

**View it:** https://dylan-keel.github.io/humboldt-visualization/baduwat-mad-river/fox-crossing/

## What is in it

- Twenty dates from March 1942 to October 2025
- Four views: the drainage, the parcel, a 3D view of the parcel looking northwest, and a 3D view of the whole drainage
- Play, pause, zoom, and save any frame as a still

## Layers

- Parcel boundary, watershed divide, streams, CAL FIRE historical fire perimeters
- Off by default, with an opacity slider: LiDAR canopy height (2018 USGS 3DEP), legacy trees (LiDAR tops at least 131 ft tall with a full crown), Topographic Wetness Index (from the 10 m elevation model)

## Files

- `index.html`: the viewer
- `.jpg`: frames for each view and date. `.webp`: canopy height and wetness index layers
- `legacy_trees.csv`: flagged tree tops with UTM zone 10N coordinates, longitude, latitude and height
- `code/`: scripts that located, orthorectified and assembled the imagery. Shared page and layer code is in `/shared`

## Caveats

Historic frames were orthorectified for this project and sit within a few metres of each other, more on steep ground. The parcel boundary, watershed divide and stream lines are not a survey. The legacy tree layer is a LiDAR screen, not a timber cruise.
