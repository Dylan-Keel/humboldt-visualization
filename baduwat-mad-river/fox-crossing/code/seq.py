import json,re,collections,sys
import numpy as np
R={}
for l in open('loc_all.jsonl'):
    r=json.loads(l); R[r['aid']]=r
def key(t):
    m=re.match(r'(.*?)[\s\-_]*(\d+)(?:[ _]\d+)?$',t); return (m.group(1),int(m.group(2))) if m else (t,0)
G=collections.defaultdict(list)
for r in R.values():
    if re.search(r'[ _]0\d$',r['title']) and not r['title'].startswith('HC74'): pass
    k,n=key(r['title']); G[(r['date'][:4],k)].append((n,r))
out=[]
for (yr,k),L in G.items():
    L.sort(key=lambda x:x[0])
    for i in range(len(L)-1):
        (n1,a),(n2,b)=L[i],L[i+1]
        dn=n2-n1
        if dn<1 or dn>4: continue
        dx=b['x']-a['x']; dy=b['y']-a['y']; d=(dx*dx+dy*dy)**0.5/dn
        foot=a['mpp']*336
        if 0.2*foot<d<0.6*foot and abs(a['mpp']-b['mpp'])/a['mpp']<0.2 and min(abs(dx),abs(dy))<0.35*max(abs(dx),abs(dy)) and abs(((a['rot']-b['rot']+180)%360)-180)<15:
            out.append((yr,k,n1,n2,a['x'],a['y'],b['x'],b['y'],a['mpp'],a['rot'],a['dz'],b['dz']))
out.sort()
cx,cy=426150,4502000
for o in out:
    near=min(abs(o[4]-cx)+abs(o[5]-cy),abs(o[6]-cx)+abs(o[7]-cy))
    print(*o,'NEAR' if near<5000 else '')
