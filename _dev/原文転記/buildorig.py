import json,re,sys
sys.path.insert(0,'.')
from t1b import T1
from t2b import T2
from t3b import T3
old=json.load(open('old_data.json'))
def groups(text):
    out=[];i=0
    while True:
        j=text.find('（1．',i)
        if j<0: break
        d=0;k=j
        while k<len(text):
            if text[k]=='（': d+=1
            elif text[k]=='）':
                d-=1
                if d==0: break
            k+=1
        inner=text[j+1:k]
        parts=[p.strip(' 　\n') for p in re.split(r'(?:^|[\s　\n]+)\d{1,2}．',inner) if p.strip(' 　\n')]
        out.append((j,k+1,parts)); i=k+1
    return out
def norm(s): return re.sub(r'[\s　]','',s).replace('靱','靭').replace('<sub>','').replace('</sub>','').replace('<sup>','').replace('</sup>','')
ORIG={}; problems=[]
for setno,T,Qold in [(1,T1,old['Q1']),(2,T2,old['Q2']),(3,T3,old['Q3'])]:
    ORIG[setno]={}
    for q in Qold:
        t=T[q['id']]; oq={'ins':t['ins'],'type':t['type'],'bl':t.get('bl',''),'html':bool(t.get('html'))}
        olditems=q['sections'] and [it for s in q['sections'] for it in s['items']] if q.get('sections') else q['items']
        oldkeys=[it['k'] for it in olditems]
        if t['type']=='tf':
            oq['tf']=t['tf']; keys=list(t['tf'].keys())
        else:
            secs=[];keys=[];opts={}
            for s in t['secs']:
                lab,text,ks=s[0],s[1],s[2]
                sd={'lab':lab,'text':text,'keys':list(ks)}
                if len(s)>3: sd['words']=s[3]
                secs.append(sd); keys+=list(ks)
                if t['type']=='para':
                    gs=groups(text); used=set()
                    blanks=[(m.start(),m.end(),m.group(1)) for m in re.finditer(r'\[([A-L])\]',text)]
                    if not blanks:
                        assert len(ks)==1; 
                        if gs: opts[ks]=gs[0][2]
                    for (bs,be,k) in blanks:
                        if k in opts: continue
                        g=[x for x in gs if x[0]==be]
                        if not g:
                            g=[x for x in gs if x[0]>be and id(x) not in used and not any(b2[1]==x[0] for b2 in blanks)]
                        if g: opts[k]=g[0][2]; used.add(id(g[0]))
            opts.update(t.get('opts',{}))
            oq['secs']=secs; oq['opts']=opts
            if 'itemx' in t: oq['itemx']=t['itemx']
            if t.get('nolab'): oq['nolab']=True
            if 'wl' in t: oq['wl']=t['wl']
        if keys!=oldkeys: problems.append((setno,q['id'],'keys',keys,oldkeys))
        # compare options
        for it in olditems:
            k=it['k']
            if t['type']=='tf': continue
            if t['type']=='para':
                o=oq['opts'].get(k)
                if o is None: problems.append((setno,q['id'],k,'NO OPTS')); continue
                if len(o)!=len(it['o']): problems.append((setno,q['id'],k,'len',o,it['o']))
                elif [norm(x) for x in o]!=[norm(x) for x in it['o']]: print('DIFF',setno,q['id'],k,o,'| old:',it['o'])
            else:
                s=[s for s in oq['secs'] if k in s['keys']][0]
                ow=[ss for ss in q['sections'] if any(i2['k']==k for i2 in ss['items'])][0]['words']
                if len(s['words'])!=len(ow): problems.append((setno,q['id'],k,'wlen',len(s['words']),len(ow)))
                elif [norm(x) for x in s['words']]!=[norm(x) for x in ow]: print('WDIFF',setno,q['id'],k)
        ORIG[setno][q['id']]=oq
print('PROBLEMS',problems)
for s in ORIG:
    for qid in ['q5','q6','q8']:
        if qid in ORIG[s] and ORIG[s][qid]['type']=='shared': ORIG[s][qid].setdefault('wl','［語群］')
for s in ORIG:
    for q in ORIG[s].values():
        if q['type']=='shared': q.setdefault('wl','［語群］')
ORIG[3]['q5']['wl']='';ORIG[3]['q8']['wl']=''
json.dump(ORIG,open('orig.json','w'),ensure_ascii=False)
print('ok')
