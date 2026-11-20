import geo, json, sys, os, glob, numpy as np
D={d['tag']+'_'+d['title'].replace(' ','_'):d for d in json.load(open('dl_list.json'))}
pv={}
for fn in ('pv0.log','pv1.log','pv2.log'):
    for l in open(fn):
        try: r=json.loads(l)
        except: continue
        if r['inl']>=90 and r['score']>0.15: pv[r['tag']+'_'+r['title'].replace(' ','_')]=r['cam']
files=sorted(glob.glob('scans/*.jpg')); part=int(sys.argv[1]); n=int(sys.argv[2])
T=((1,0,0),(0.92,0,0),(1.08,0,0),(1,0,400),(1,0,-400),(1,400,0),(1,-400,0),(1.16,0,0),(0.85,0,0))
for path in files[part::n]:
    b=os.path.basename(path)[:-4]; out=f'pose/{b}.npz'
    if b not in D or os.path.exists(out) or os.path.exists(out.replace('.npz','.rej.npz')): continue
    d=D[b]; x,y,foot=d['x'],d['y'],d['foot']
    if b in pv: x,y=pv[b][0],pv[b][1]
    best=None
    for wf in (640,1200,900):
        geo.WFIT=wf
        try: f=geo.best_fit(path,x,y,foot,0,cf=0.08,tries=T)
        except Exception as e: print(b,'ERR',e,flush=True); f=None
        if f and (best is None or (f['inl'],f['score'])>(best['inl'],best['score'])): best=f
        if best and best['inl']>=60 and best['score']>0.15: break
    f=best
    if f is None: print(b,'FAILED',flush=True); continue
    ok=f['inl']>=35 and f['score']>0.10
    print(b,'inl',f['inl'],'med %.2f'%f['med'],'score %.3f'%f['score'],'cam %.0f %.0f %.0f'%f['cam'],'pred',x,y,'OK' if ok else 'REJECT',flush=True)
    np.savez(out if ok else out.replace('.npz','.rej.npz'),K=f['K_full'],d=f['d'],rv=f['rv'],tv=f['tv'],cam=f['cam'],cf=f['cf'],inl=f['inl'],score=f['score'],med=f['med'])
