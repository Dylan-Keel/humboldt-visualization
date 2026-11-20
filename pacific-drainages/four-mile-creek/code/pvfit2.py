import geo, loc, json, sys, time
geo.WFIT=640
L=json.load(open(sys.argv[2] if len(sys.argv)>2 else 'cand_list.json')); part=int(sys.argv[1])
for c in L[part::2]:
    try:
        fn=loc.preview(c['aid'])
        f=geo.best_fit(fn,c['x'],c['y'],c['foot'],0,cf=0.08,tries=((1,0,0),(0.92,0,0),(1.08,0,0),(1,0,500),(1,0,-500),(1.18,0,0)))
        print(json.dumps(dict(tag=c['tag'],title=c['title'],aid=c['aid'],inl=f['inl'],score=round(f['score'],3),cam=[round(float(v)) for v in f['cam']])),flush=True)
    except Exception as e: print(json.dumps(dict(title=c['title'],err=str(e)[:80])),flush=True)
