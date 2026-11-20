"""Build the historic mosaics from refined poses and write hist.json (frame list entries for the page)."""
import json, glob, os, sys, mos
from cfg import *
Y=[('1942','1942',1942,'February 15, 1942','USDA flight CVL, 1:20,000, black and white','about 0.8 m','CVL-9B','The east edge of the watershed view is filled from the same survey flown October 29, 1941 (frames CVL-1B-62 and CVL-1B-63)'),
   ('1948','1948',1948,'June 22, 1948','California Division of Forestry flight CDF2, 1:20,000, black and white','about 0.8 m',None,None),
   ('1954','1954',1954,'July 22, 1954','USDA flight CVL, 1:20,000, black and white','about 0.8 m',None,None),
   ('1959','1959',1959,'May 22 and June 10, 1959','Humboldt County flight HS, black and white','about 0.6 m',None,None),
   ('1963','1963',1963,'August 14, 1963','Humboldt County flight HC-S-2-3, black and white','about 0.5 m',None,'Some prints carry no date'),
   ('1966','1966',1966,'September 2, 1966','Humboldt County flight HC-66, black and white','about 0.5 m',None,'Some prints carry no date'),
   ('1970','1970',1970,'July 22 and October 8, 1970','Humboldt County flight CH-70, black and white','about 0.5 m',None,None),
   ('1981','1981',1981,'June 15, 1981','California Department of Forestry flight CDF ALL-EU, black and white','about 1 m',None,'I found no frames from the flight line over the middle of the watershed')]
H=[]; todo=sys.argv[1:]
for tag,label,year,date,src,res,pri,note in Y:
    poses=sorted(glob.glob(f'pose2/{tag}_*.npz'))
    frames=[(f"scans/{os.path.basename(p)[:-4]}.jpg",p) for p in poses]
    used=[os.path.basename(p)[:-4].split('_',1)[1].replace('_01','').replace('_',' ') for p in poses if (not pri or pri in p)]
    if not todo or tag in todo:
        cov=mos.mosaic('h'+tag,frames,views=ALLV,ocf=0.05,primary=[pri] if pri else None)
        json.dump(cov,open(f'master/h{tag}_cov.json','w')); print(tag,cov,flush=True)
    cov=json.load(open(f'master/h{tag}_cov.json')); n=[]
    if note: n.append(note)
    if cov['w']<0.97: n.append(f"About {round((1-cov['w'])*100)} percent of the watershed view has no coverage")
    H.append(dict(id=tag,file='h'+tag,label=label,year=year,date=date,source=src+'. Mosaic of full-resolution scans (Cal Poly Humboldt), orthorectified here. Frames: '+', '.join(used),res=res,note='. '.join(n),bw=True))
json.dump(H,open('hist.json','w'),indent=1)
