import geo, json, sys, os, glob, numpy as np
pred={t:(x,y,f) for t,x,y,f in json.load(open('pv_list.json'))}
pv={}
for l in open('pvfit.log'):
    try: r=json.loads(l)
    except: continue
    if r['inl']>=90 and r['score']>0.15: pv[r['title']]=r['cam']
files=sorted(glob.glob('scans/*.jpg')); part=int(sys.argv[1]); n=int(sys.argv[2])
for path in files[part::n]:
    b=os.path.basename(path)[:-4]; tag,t=b.split('_',1); out=f'pose/{b}.npz'
    if os.path.exists(out): continue
    x,y,foot=pred[t]
    if t in pv: x,y=pv[t][0],pv[t][1]
    f=geo.best_fit(path,x,y,foot,0,cf=0.08)
    if f is None: print(b,'FAILED',flush=True); continue
    ok=f['inl']>=35 and f['score']>0.10
    print(b,'inl',f['inl'],'med %.2f'%f['med'],'score %.3f'%f['score'],'cam %.0f %.0f %.0f'%f['cam'],'OK' if ok else 'REJECT',flush=True)
    np.savez(out if ok else out.replace('.npz','.rej.npz'),K=f['K_full'],d=f['d'],rv=f['rv'],tv=f['tv'],cam=f['cam'],cf=f['cf'],inl=f['inl'],score=f['score'],med=f['med'])
