import refine, mos, glob, os, subprocess, numpy as np, sys
from cfg import *
def comp(tags):
    out=None
    for t in tags:
        a=refine.load_ref(t)
        if out is None: out=a.copy()
        else: m=out==0; out[m]=a[m]
    return out
def do(tagglob,reftags):
    ref=comp(reftags); res=[]
    for pf in sorted(glob.glob(f'pose/{tagglob}*.npz')):
        if pf.endswith('.rej.npz'): continue
        b=os.path.basename(pf)[:-4]
        r=refine.refine(f'scans/{b}.jpg',pf,ref,f'pose2/{b}.npz',verbose=False); print(b,'->',r,flush=True)
mos.mosaic('h1993',[('ucsb/napp-2c_6248-42.tif','pose2/napp-2c_6248-42.npz'),('ucsb/napp-2c_6248-44.tif','pose2/napp-2c_6248-44.npz')],views=ALLV,ocf=0.035)
steps=[('1970',['h1993','county_2005']),('1966',['h1970','h1993']),('1962',['h1966','h1970','h1993']),('1958',['h1962','h1966','h1993']),('1954',['h1958','h1962','h1993']),('1948',['h1954','h1958']),('1942',['h1948','h1954'])]
for tag,refs in steps:
    do(tag,refs)
    subprocess.run([sys.executable,'hist.py']+(['1942a','1942b'] if tag=='1942' else [tag]))
