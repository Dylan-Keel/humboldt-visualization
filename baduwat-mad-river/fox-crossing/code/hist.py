import json, glob, os, sys, mos
from cfg import *
Y=[('1942a','1942 Mar',1942,'March 4, 1942','USDA flight CVL, 1:20,000, black and white','about 0.8 m','CVL-11B',None),
   ('1942b','1942 Jul',1942,'July 30, 1942','USDA flight CVL, 1:20,000, black and white','about 0.8 m','CVL-14B',None),
   ('1948','1948',1948,'June 22, 1948','California Division of Forestry flight CDF2, 1:20,000, black and white','about 0.8 m',None,None),
   ('1954','1954',1954,'August 22, 1954','USDA flight CVL, 1:20,000, black and white','about 0.8 m',None,None),
   ('1958','1958',1958,'July 28, 1958','Humboldt County flight HU, about 1:14,000, black and white','about 0.6 m',None,None),
   ('1962','1962-63',1962,'August or September of 1962 or 1963','Humboldt County flight HCN-2, about 1:12,000, black and white','about 0.5 m',None,'The prints carry no date. Dated frames from this flight are from August and September of 1962 and 1963'),
   ('1966','1966',1966,'1966','Humboldt County flight HC-66, about 1:12,000, black and white','about 0.5 m',None,'The prints carry no date'),
   ('1970','1970',1970,'August 2, 1970','Humboldt County flight CH-70, about 1:12,000, black and white','about 0.5 m',None,None)]
H=[]
todo=sys.argv[1:]
for tag,label,year,date,src,res,pri,note in Y:
    if tag.startswith('1942'):
        poses=sorted(glob.glob('pose/1942[ab]_*.npz'))
    else: poses=sorted(glob.glob(f'pose/{tag}_*.npz'))
    poses=[p for p in poses if not p.endswith('.rej.npz')]
    frames=[(f"scans/{os.path.basename(p)[:-4]}.jpg",(p.replace('pose/','pose2/') if os.path.exists(p.replace('pose/','pose2/')) else p)) for p in poses]
    used=[os.path.basename(p)[:-4].split('_',1)[1] for p in poses if (not pri or pri in p)]
    if not todo or tag in todo:
        cov=mos.mosaic('h'+tag,frames,views=ALLV,primary=[pri] if pri else None)
        json.dump(cov,open(f'master/h{tag}_cov.json','w'))
    cov=json.load(open(f'master/h{tag}_cov.json'))
    n=[]
    if note: n.append(note)
    if tag=='1942a': n.append('Ground east of this flight line is filled from the July 30, 1942 line')
    if tag=='1942b': n.append('Ground west of this flight line is filled from the March 4, 1942 line')
    if cov['w']<0.97: n.append(f"About {round((1-cov['w'])*100)} percent of the drainage view has no coverage")
    H.append(dict(id=tag,file='h'+tag,label=label,year=year,date=date,source=src+'. Mosaic of full-resolution scans (Cal Poly Humboldt), orthorectified here. Frames: '+', '.join(used),res=res,note='. '.join(n),bw=True))
json.dump(H,open('hist.json','w'))
