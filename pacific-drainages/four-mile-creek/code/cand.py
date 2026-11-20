import loc, json, re, sys, numpy as np
loc.REFSEL=''
cat={t:(a,d) for t,d,a in loc.catalog()}
def run(prefix,nums,scales=None,pad=2):
    out=[]
    for n in nums:
        t=None
        for fmt in (f'{prefix}{n}',f'{prefix}{n:02d}',f'{prefix}{n:03d}'):
            if fmt in cat: t=fmt; break
        if not t: out.append((n,None)); continue
        fn=loc.preview(cat[t][0])
        if not fn: out.append((n,None)); continue
        a=loc.crop(fn).astype('float32'); best=None
        res=[]
        for ref in ('img','hs'):
            loc.REFSEL=ref
            b,z=loc.locate(a,scales=scales or loc.SCALES,drs=(-8,-4,0,4,8)); res.append((ref,round(z,1),b[3],b[4],round(b[5]),round(b[6])))
        out.append((n,t,cat[t][1],res))
    return out
if __name__=='__main__':
    spec=json.loads(sys.argv[1])
    for prefix,a,b,sc in spec:
        print('==',prefix)
        for o in run(prefix,range(a,b+1),sc): print(o,flush=True)
