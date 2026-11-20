import geo, json, os, numpy as np
from cfg import *
pred={t:(x,y,f) for t,x,y,f in json.load(open('pv_list.json'))}
pv={}
for l in open('pvfit.log'):
    try: r=json.loads(l)
    except: continue
    if r['inl']>=100 and r['score']>0.2: pv[r['title']]=r['cam']
geo.REFS={('img',1966):geo.image_ref('master/h1966_x.tif',VX,RX),('img',1962):geo.image_ref('master/h1962_x.tif',VX,RX)}
for b in ('1970_CH-70-28-67','1970_CH-70-28-68','1970_CH-70-28-69','1970_CH-70-28-70','1958_HU20-09'):
    t=b.split('_',1)[1]; x,y,foot=pred[t]
    if t in pv: x,y=pv[t][0],pv[t][1]
    best=None
    for wf in (640,900):
        geo.WFIT=wf
        f=geo.best_fit(f'scans/{b}.jpg',x,y,foot,0,cf=0.08,tries=((1,0,0),(0.92,0,0),(1.08,0,0),(1,0,400),(1,0,-400),(1,300,0),(1,-300,0)))
        if f and (best is None or (f['inl'],f['score'])>(best['inl'],best['score'])): best=f
        if best and best['inl']>=80 and best['score']>0.2: break
    f=best; ok=f['inl']>=40 and f['score']>0.15
    print(b,'inl',f['inl'],'med %.2f'%f['med'],'score %.3f'%f['score'],'cam %.0f %.0f %.0f'%f['cam'],'pred',x,y,'OK' if ok else 'REJECT',flush=True)
    if ok:
        np.savez(f'pose/{b}.npz',K=f['K_full'],d=f['d'],rv=f['rv'],tv=f['tv'],cam=f['cam'],cf=f['cf'],inl=f['inl'],score=f['score'],med=f['med'])
        if os.path.exists(f'pose/{b}.rej.npz'): os.remove(f'pose/{b}.rej.npz')
