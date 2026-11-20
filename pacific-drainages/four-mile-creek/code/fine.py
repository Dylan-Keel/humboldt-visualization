import loc, json, re, sys, numpy as np, cv2
from multiprocessing import Pool
loc.REFSEL='img'
SC=json.loads(sys.argv[2])
def work(c):
    t,d,a=c
    try:
        fn=loc.preview(a)
        if not fn: return None
        b,z=loc.locate(loc.crop(fn).astype('float32'),scales=SC,drs=(-8,-4,0,4,8))
        return (t,d,round(z,1),b[3],b[4],round(b[5]),round(b[6]))
    except Exception as e: return None
if __name__=='__main__':
    cat=[c for c in loc.catalog() if re.match(sys.argv[1],c[0])]
    key=lambda c:[int(x) if x.isdigit() else x for x in re.split(r'(\d+)',c[0])]
    cat.sort(key=key); cv2.setNumThreads(1); loc.coarse_refs(50.0)
    with Pool(3) as p: R=[r for r in p.imap(work,cat,chunksize=4) if r]
    json.dump(R,open(sys.argv[3],'w'))
    thr=float(sys.argv[4]) if len(sys.argv)>4 else 3.0
    for r in R:
        if r[2]>=thr: print(*r)
