# Wild Turkey Creek Flipbook (Cooskie Ridge)

A registered aerial image time series for 440 Cooskie Ridge Road, Petrolia (APN 104-122-019, 163.6 acres) and the 494-acre Wild Turkey Creek Watershed it drains to, a tributary of the Mattole River. Wild Turkey Creek is the owner's name for an unnamed tributary.

**View it:** https://dylan-keel.github.io/humboldt-visualization/mattole-river/wild-turkey-creek/

## What is in it

- Twenty-two dates from October 1941 to July 2025
- Three views: the watershed, the parcel, and a 3D view looking due south
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
