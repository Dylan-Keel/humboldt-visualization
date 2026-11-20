import json, os
H=json.load(open('hist.json')) if os.path.exists('hist.json') else []
F=list(H)
F.append(dict(id='1993',file='h1993',label='1993',year=1993,date='June 13, 1993',source='USGS National Aerial Photography Program frames 6248-42 and 6248-44, black and white, 1:40,000 (UCSB Library scans), orthorectified here',res='about 1.7 m',note='The west edge of the drainage view lies outside the frame',bw=True))
for y in (2005,2009,2010): F.append(dict(id=str(y),file=f'county_{y}',label=str(y),year=y,date=f'Summer {y}',source='USDA NAIP natural color (Humboldt County image service)',res='1 m'))
for y,d,r in ((2012,'June 10, 2012','1 m'),(2014,'June 8, 2014','1 m'),(2016,'May 28, 2016','0.6 m'),(2018,'September 23, 2018','0.6 m'),(2020,'July 14, 2020','0.6 m'),(2022,'May 31, 2022','0.6 m'),(2024,'May 31, 2024','0.6 m')):
    F.append(dict(id=str(y),file=f'naip_{y}',label=str(y),year=y,date=d,source='USDA NAIP natural color',res=r))
F.append(dict(id='2025',file='esri',label='2025',year=2025,date='October 31, 2025',source='Satellite image from Esri World Imagery (Vantor)',res='about 0.5 m'))
json.dump(F,open('frames.json','w'),indent=0); print(len(F))
