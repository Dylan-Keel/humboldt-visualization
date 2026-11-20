# Four Mile Creek Flipbook

A registered aerial image time series for Humboldt County parcel APN 104-144-018 (123 acres) and the 3,333-acre Fourmile Creek watershed, which drains west to the Pacific south of the Mattole River mouth.

**View it:** https://dylan-keel.github.io/humboldt-visualization/pacific-drainages/four-mile-creek/

## What is in it

- Nineteen dates from February 1942 to May 2025
- Six views: the watershed, the parcel, and four fixed-camera 3D views (parcel, from the ocean, from the south, from the headwaters)
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
