"""Tighten each year against the next later mosaics (ending at 1993 and 2005 NAIP), retry frames whose terrain fit failed
against those mosaics, then build the year's mosaic."""
import refine, mos, geo, glob, os, sys, json, numpy as np
from cfg import *
D={d['tag']+'_'+d['title'].replace(' ','_'):d for d in json.load(open('dl_list.json'))+json.load(open('dl_east.json'))}
import cv2
def camof(pf):
    z=np.load(pf,allow_pickle=True); C=-cv2.Rodrigues(z['rv'])[0].T@z['tv'].ravel(); return C[0]+geo.X0,C[1]+geo.Y0,C[2]
def sane(b,pf):
    c=camof(pf); d=D[b]; return np.hypot(c[0]-d['x'],c[1]-d['y'])<1300 and 0.55*d['foot']<c[2]-geo.zat(np.array([c[0]]),np.array([c[1]]))[0]<2.2*d['foot']
def comp(tags):
    out=None
    for t in tags:
        a=refine.load_ref(t)
        if out is None: out=a.copy()
        else: m=out==0; out[m]=a[m]
    return out
def reffit(b,reftags):
    d=D[b]; best=None
    geo.REFS={('img',i):geo.image_ref(f'master/{t}_x.tif',VX,RX) for i,t in enumerate(reftags)}
    for wf in (640,900):
        geo.WFIT=wf
        f=geo.best_fit(f'scans/{b}.jpg',d['x'],d['y'],d['foot'],0,cf=0.08,tries=((1,0,0),(0.92,0,0),(1.08,0,0),(1,0,400),(1,0,-400),(1,400,0),(1,-400,0),(1,800,0),(1,-800,0),(1,0,800),(1,0,-800),(1,600,600),(1,-600,-600),(1,600,-600),(1,-600,600)))
        if f and (best is None or (f['inl'],f['score'])>(best['inl'],best['score'])): best=f
        if best and best['inl']>=80 and best['score']>0.2: break
    geo.REFS=None; f=best
    ok=f is not None and f['inl']>=40 and f['score']>0.15
    if ok:
        h=f['cam'][2]-geo.zat(np.array([f['cam'][0]]),np.array([f['cam'][1]]))[0]; ok=0.55*d['foot']<h<2.2*d['foot']
    print('  reffit',b,f and (f['inl'],round(f['score'],3),[round(c) for c in f['cam']]),'OK' if ok else 'REJECT',flush=True)
    if ok: np.savez(f'pose/{b}.npz',K=f['K_full'],d=f['d'],rv=f['rv'],tv=f['tv'],cam=f['cam'],cf=f['cf'],inl=f['inl'],score=f['score'],med=f['med'])
    return ok
steps=[('1981',['h1993','county_2005']),('1970',['h1981','h1993','county_2005']),('1966',['h1970','h1993','county_2005']),('1963',['h1966','h1970','h1993']),
       ('1959',['h1963','h1966','h1993']),('1954',['h1959','h1963','h1993']),('1948',['h1954','h1959','h1993']),('1942',['h1948','h1954','h1993'])]
todo=sys.argv[1:]
for tag,refs in steps:
    if todo and tag not in todo: continue
    ref=comp(refs); frames=[]; used=[]
    for sp in sorted(glob.glob(f'scans/{tag}_*.jpg')):
        b=os.path.basename(sp)[:-4]; pf=f'pose/{b}.npz'; p2=f'pose2/{b}.npz'
        if b not in D: continue
        if os.path.exists(p2) and sane(b,p2): frames.append((sp,p2)); used.append(b); continue
        if os.path.exists(p2): os.remove(p2)
        def tryref():
            try: return refine.refine(sp,pf,ref,p2,verbose=False)
            except Exception as e: return None
        r=None
        if os.path.exists(pf) and float(np.load(pf)['score'])>=0.2 and sane(b,pf): r=tryref()
        if r is None:
            if os.path.exists(p2): os.remove(p2)
            if reffit(b,refs): r=tryref()
        print(b,'->',r,flush=True)
        if r is None or not os.path.exists(p2) or not sane(b,p2):
            if os.path.exists(p2): os.remove(p2)
            print(b,'DROPPED',flush=True); continue
        frames.append((sp,p2)); used.append(b)
    cov=mos.mosaic('h'+tag,frames,views=ALLV); cov=dict(cov) if cov else {}; cov['used']=used
    json.dump(cov,open(f'master/h{tag}_cov.json','w')); print(tag,'mosaic',cov,flush=True)
