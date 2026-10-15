import json,subprocess,sys
p=subprocess.Popen(["node","tools/pkmn/dist/index.js"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
def rpc(i,m,pa=None):
  msg={"jsonrpc":"2.0","id":i,"method":m}; 
  if pa is not None: msg["params"]=pa
  p.stdin.write(json.dumps(msg)+"\n"); p.stdin.flush()
  return json.loads(p.stdout.readline())
print(json.dumps(rpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"repro","version":"0"}}))[:300])
p.stdin.write(json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"})+"\n"); p.stdin.flush()
tl=rpc(2,"tools/list",{})
t=[x for x in tl["result"]["tools"] if x["name"]=="calculate_status"][0]
print("SCHEMA calculate_status:",json.dumps(t["inputSchema"])[:1500])
props=t["inputSchema"]["properties"]; json.dump(t,open("AFE-0017/schema.json","w"),indent=1)
iv={"hp":31,"atk":31,"def1":31,"spa":31,"spd":31,"spe":31}; ev={"hp":0,"atk":0,"def1":0,"spa":0,"spd":0,"spe":0}
args={"pokemonName":"フシギダネ","level":50,"nature":"がんばりや","ivs":iv,"evs":ev}
for i in range(3):
  r=rpc(10+i,"tools/call",{"name":"calculate_status","arguments":args})
  print(f"CALL{i+1} args.ivs/evs use def1 ->",json.dumps(r,ensure_ascii=False)[:700])
good={**args,"ivs":{**{k:v for k,v in iv.items() if k!="def1"},"def":31},"evs":{**{k:v for k,v in ev.items() if k!="def1"},"def":0}}
r=rpc(20,"tools/call",{"name":"calculate_status","arguments":good}); print("CONTROL def ->",json.dumps(r,ensure_ascii=False)[:400])
