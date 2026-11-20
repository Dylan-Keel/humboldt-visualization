import chain_fn as C, geo, refine, numpy as np, os
from cfg import *
b='1959_HS2-34'; C.D[b]['x']=389700; C.D[b]['y']=4459230
best=None
for refs in (['h1963'],['h1954'],['h1966']):
    geo.REFS={('img',0):geo.image_ref(f'master/{refs[0]}_x.tif',VX,RX)}
    for wf in (640,900):
        geo.WFIT=wf
        for foot in (2820,3100,2550):
            for dx,dy in ((0,0),(0,300),(0,-300),(300,0),(-300,0)):
                try: f=geo.fit_file(f'scans/{b}.jpg',389700+dx,4459230+dy,foot,0,0.08,verbose=False)
                except Exception as e: continue
                h=f['cam'][2]-geo.zat(np.array([f['cam'][0]]),np.array([f['cam'][1]]))[0]
                ok=1500<h<6000 and abs(f['cam'][0]-389700)<900 and abs(f['cam'][1]-4459230)<900
                if ok and (best is None or (f['inl'],f['score'])>(best['inl'],best['score'])): best=f; print(refs,wf,foot,dx,dy,f['inl'],round(f['score'],3),[round(c) for c in f['cam']],flush=True)
            if best and best['inl']>=150 and best['score']>0.3: break
        if best and best['inl']>=150 and best['score']>0.3: break
    if best and best['inl']>=150 and best['score']>0.3: break
if best:
    f=best; np.savez(f'pose/{b}.npz',K=f['K_full'],d=f['d'],rv=f['rv'],tv=f['tv'],cam=f['cam'],cf=f['cf'],inl=f['inl'],score=f['score'],med=f['med'])
    ref=C.comp(['h1963','h1966','h1993']); r=refine.refine(f'scans/{b}.jpg',f'pose/{b}.npz',ref,f'pose2/{b}.npz',verbose=False); print('refine',r, C.sane(b,f'pose2/{b}.npz') if os.path.exists(f'pose2/{b}.npz') else None)
