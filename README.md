# Humboldt Visualization

Registered aerial image time series ("flipbooks") for parcels and small watersheds in Humboldt County, California, grouped by drainage.

**Start here:** https://dylan-keel.github.io/humboldt-visualization/

| Drainage | Flipbook | Parcel | Dates |
|---|---|---|---|
| Pacific drainages | [Four Mile Creek](https://dylan-keel.github.io/humboldt-visualization/pacific-drainages/four-mile-creek/) | APN 104-144-018 | 1942 to 2025 |
| Mattole River | [Wild Turkey Creek, Cooskie Ridge](https://dylan-keel.github.io/humboldt-visualization/mattole-river/wild-turkey-creek/) | APN 104-122-019 | 1941 to 2025 |
| Baduwa't (Mad River) | [Fox Crossing](https://dylan-keel.github.io/humboldt-visualization/baduwat-mad-river/fox-crossing/) | APN 314-213-030 | 1942 to 2025 |

## What each flipbook shows

- Every date on one map grid, so flipping between years shows change in place
- 2D views of the watershed and the parcel, and fixed-camera 3D views draped on the 10 m elevation model
- Overlays: parcel boundary, watershed divide, streams, CAL FIRE historical fire perimeters
- Optional layers, off by default with an opacity slider: LiDAR canopy height, legacy trees (LiDAR tops at least 131 ft tall with a full crown), and Topographic Wetness Index
- Play, pause, zoom, and save any frame as a still

## Layout

```
pacific-drainages/four-mile-creek/     viewer, frames, code
mattole-river/wild-turkey-creek/       viewer, frames, code
baduwat-mad-river/fox-crossing/        viewer, frames, code
shared/                                page template, builder, LiDAR and wetness index code
```

In each flipbook folder, `index.html` is the viewer, the `.jpg` files are frames, the `.webp` files are the canopy and wetness layers, `legacy_trees.csv` lists the flagged tree tops (UTM zone 10N, NAD83), and `code/` holds the scripts that located, orthorectified and assembled the imagery.

## Sources

- Historic prints: Humboldt County Aerial Photograph Collection, Cal Poly Humboldt
- 1993 and 1998: USGS National Aerial Photography Program (UCSB Library scans)
- 2005 onward: USDA National Agriculture Imagery Program; latest date from Esri World Imagery
- LiDAR: USGS 3DEP, 2018. Elevation: USGS 3DEP 10 m
- Parcels: Humboldt County GIS. Streams: National Hydrography Dataset. Fire perimeters: CAL FIRE

## Caveats

Historic frames were orthorectified for this project and sit within a few metres of each other, more on steep ground. Parcel boundaries, watershed divides and stream lines are not a survey. The legacy tree layer is a LiDAR screen, not a timber cruise. The wetness index comes from a 10 m elevation model and shows where terrain concentrates drainage, not measured soil moisture.
