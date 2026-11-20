import refine, glob, os, sys, subprocess, numpy as np
def comp(tags):
    out=None
    for t in tags:
        a=refine.load_ref(t)
        if out is None: out=a.copy()
        else: m=out==0; out[m]=a[m]
    return out
for b,refs in (('1970_CH-70-28-67',['h1966','h1962']),('1970_CH-70-28-70',['h1966','h1962']),('1966_HC-66-27-76',['h1962','h1958'])):
    r=refine.refine(f'scans/{b}.jpg',f'pose/{b}.npz',comp(refs),f'pose2/{b}.npz',verbose=False,minscore=0.28); print(b,r,flush=True)
subprocess.run([sys.executable,'hist.py','1970','1966'])
