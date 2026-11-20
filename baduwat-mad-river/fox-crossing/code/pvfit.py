import geo, loc, json, sys, numpy as np, time
geo.WFIT=640
cat={t:(a,d) for t,d,a in loc.catalog()}
def pv(t,cx,cy,foot,rot=0):
    fn=loc.preview(cat[t][0]); t0=time.time()
    f=geo.best_fit(fn,cx,cy,foot,rot,cf=0.08,tries=((1,0,0),(0.92,0,0),(1.08,0,0),(1,0,500),(1,0,-500)))
    return dict(title=t,aid=cat[t][0],inl=f['inl'],score=round(f['score'],3),cam=[round(float(c)) for c in f['cam']],sec=round(time.time()-t0))
if __name__=='__main__':
    for t,cx,cy,foot in json.loads(sys.argv[1]):
        try: print(json.dumps(pv(t,cx,cy,foot)),flush=True)
        except Exception as e: print(t,'ERR',str(e)[:80],flush=True)
