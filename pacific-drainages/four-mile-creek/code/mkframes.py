"""Write frames.json and site.json (page text) for the Four Mile Creek flipbook."""
import json
H=json.load(open('hist.json')); F=list(H); N='USDA NAIP natural color'
F.append(dict(id='1993',file='h1993',label='1993',year=1993,date='June 13 and June 25, 1993',source='USGS National Aerial Photography Program frames 6247-163 and 6250-11, black and white, 1:40,000 (UCSB Library scans), orthorectified here',res='about 1.7 m',bw=True))
for y in (2005,2009,2010): F.append(dict(id=str(y),file=f'county_{y}',label=str(y),year=y,date=f'Summer {y}',source=N+' (Humboldt County image service)',res='1 m'))
for y,d,r in [(2012,'June 10, 2012','1 m'),(2014,'June 7, 2014','1 m'),(2016,'June 19, 2016','0.6 m'),(2018,'September 20, 2018','0.6 m'),(2020,'July 18, 2020','0.6 m'),(2022,'July 10, 2022','0.6 m')]:
    F.append(dict(id=str(y),file=f'naip_{y}',label=str(y),year=y,date=d,source=N,res=r))
F.append(dict(id='2025',file='esri',label='2025',year=2025,date='May 10, 2025',source='Satellite image from Esri World Imagery',res='about 0.5 m'))
json.dump(F,open('frames.json','w'),indent=1)
rows=''.join(f"<tr><td>{h['label']}</td><td>{h['source'].split('Frames: ')[1]}</td></tr>" for h in H)
lay=json.load(open('/home/claude/flip/layers_note.json')).replace('39 tops','51 tops').replace('2,664 in the drainage','1,557 in the watershed').replace('drainage, parcel and 3D views','watershed, parcel and 3D views')
words={18:'Eighteen',19:'Nineteen',20:'Twenty'}
notes=f'''  <h2>What this covers</h2>
  <p><strong>{words.get(len(F),str(len(F)))} dates, February 1942 to May 2025.</strong> Every frame is on the same UTM zone 10N grid, so the flip is registered. The watershed view is 9 by 4.05 km at 1.5 m per pixel and takes in the ridges on both sides of Fourmile Creek. The parcel view is 1.32 km square at 0.4 m per pixel.</p>
  <p><strong>1942 through 1981 are full-resolution scans.</strong> These eight dates are mosaics of scanned prints from Cal Poly Humboldt, about 0.5 to 1 m per pixel at source. I orthorectified each frame against the 10 m 3DEP elevation model, then tightened each year against the next later year, ending at 1993 and 2005 NAIP. Offsets between adjacent years are a few metres, more on steep ground. Seams show where flight lines meet, tone differs between prints, and some prints carry grease-pencil lines. Black areas have no frame for that year. Several years stop short of the beach on the west side.</p>
  <p><strong>1993</strong> is two USGS frames at about 1.7 m. Chips with dashed borders mark black-and-white dates.</p>
  <p><strong>Color balance varies by year</strong> in the NAIP frames and I left the tones as delivered. Canopy texture, openings and road lines are the reliable signal.</p>
  <p><strong>3D views.</strong> Each year is draped on the 10 m elevation model and rendered from four fixed cameras: the parcel from the south, the watershed from above the surf looking east, the full length of the watershed from the south, and the watershed from above the headwaters looking west. The terrain model is smooth at this resolution, so gullies and road cuts do not show as relief, and steep slopes stretch the photos somewhat. Grey terrain has no photo coverage for that year.</p>
  <p><strong>Gaps.</strong> I found no usable frames between 1981 and 1993, none from 1958, and could not place the 1974 frames. No 2024 NAIP image was available for this area, so the sequence steps from July 2022 to the May 2025 satellite image. The 1981 flight is missing the line over the middle of the watershed.</p>
  <p>Parcel boundary is from Humboldt County GIS. The watershed divide is delineated from the 10 m elevation model above the creek mouth. Stream lines are from the National Hydrography Dataset, which names the creek Fourmile Creek. None of these lines is a survey.</p>
  <p><strong>Fire record.</strong> The optional fire layer shows CAL FIRE historical perimeters. The Beatty Escape Fire of October 16, 1960 (5,720 acres) is mapped across the whole parcel and about 3,150 acres of the 3,333 acre watershed, so the 1959 and 1963 frames bracket it. The 1964 Mattole Fire perimeter takes in about 74 acres of the watershed. A perimeter drawn dashed burned after the date on screen. Older perimeters were often sketched by hand at coarse scale, and the record misses small and early fires, so treat edges as approximate.</p>
{lay}  <h2>Scanned frames used</h2>
  <p>Frame numbers as catalogued in the Humboldt County Aerial Photograph Collection at <a href="https://digitalcommons.humboldt.edu/hcapc_aerial/">Cal Poly Humboldt Digital Commons</a>.</p>
  <div style="overflow-x:auto"><table class="fr"><tbody>{rows}</tbody></table></div>
'''
S=json.load(open('site.json'))
S.update(title='Four Mile Creek Flipbook',h1='Four Mile Creek aerial flipbook, 1942 to 2025',notes=notes,slug='fourmile')
json.dump(S,open('site.json','w'),indent=1); print(len(F),'frames')
