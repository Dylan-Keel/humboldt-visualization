import geo, json, sys, os, glob, numpy as np
pred={t:(x,y,f) for t,x,y,f in json.load(open('pv_list.json'))}
pv={}
for l in open('pvfit.log'):
    try: r=json.loads(l)
    except: continue
    if r['inl']>=40: pv[r['title']]=r['cam']
rej=sorted(glob.glob('pose/*.rej.npz')); part=int(sys.argv[1])
for rp in rej[part::2]:
    b=os.path.basename(rp)[:-8]; tag,t=b.split('_',1); x,y,foot=pred[t]
    if t in pv: x,y=pv[t][0],pv[t][1]
    best=None
    for wf in (640,900,480):
        geo.WFIT=wf
        f=geo.best_fit(f'scans/{b}.jpg',x,y,foot,0,cf=0.08,tries=((1,0,0),(0.92,0,0),(1.08,0,0),(1,0,400),(1,0,-400),(1,400,0),(1,-400,0),(1.16,0,0),(0.85,0,0)))
        if f and (best is None or (f['inl'],f['score'])>(best['inl'],best['score'])): best=f
        if best and best['inl']>=60 and best['score']>0.15: break
    f=best; ok=f['inl']>=35 and f['score']>0.10
    print(b,'inl',f['inl'],'med %.2f'%f['med'],'score %.3f'%f['score'],'cam %.0f %.0f %.0f'%f['cam'],'wfit',f['wh'][0],'OK' if ok else 'REJECT',flush=True)
    if ok: np.savez(f'pose/{b}.npz',K=f['K_full'],d=f['d'],rv=f['rv'],tv=f['tv'],cam=f['cam'],cf=f['cf'],inl=f['inl'],score=f['score'],med=f['med']); os.remove(rp)
