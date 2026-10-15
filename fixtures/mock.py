# Scripted OpenAI-compatible /chat/completions mock. Usage: mock.py PORT SCRIPT.json LOGDIR
import json,sys,time,uuid,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
PORT=int(sys.argv[1]); SCRIPT=json.load(open(sys.argv[2])); LOG=sys.argv[3]; os.makedirs(LOG,exist_ok=True)
state={"n":0}
class H(BaseHTTPRequestHandler):
  def log_message(self,*a): pass
  def do_GET(self):
    b=json.dumps({"object":"list","data":[{"id":"mock-model","object":"model"}]}).encode()
    self.send_response(200);self.send_header("content-type","application/json");self.end_headers();self.wfile.write(b)
  def do_POST(self):
    body=json.loads(self.rfile.read(int(self.headers.get("content-length",0))) or b"{}")
    i=state["n"]; state["n"]+=1
    json.dump({"path":self.path,"body":body},open(f"{LOG}/req{i:02d}.json","w"),indent=1)
    step=SCRIPT[min(i,len(SCRIPT)-1)]
    cid="chatcmpl-"+uuid.uuid4().hex[:8]
    if "tool" in step:
      tc=[{"index":0,"id":"call_"+uuid.uuid4().hex[:8],"type":"function","function":{"name":step["tool"],"arguments":step["args"] if isinstance(step["args"],str) else json.dumps(step["args"])}}]
      msg={"role":"assistant","content":None,"tool_calls":tc}; fin="tool_calls"
    else: msg={"role":"assistant","content":step["text"]}; fin="stop"
    if body.get("stream"):
      self.send_response(200);self.send_header("content-type","text/event-stream");self.end_headers()
      def ev(d): self.wfile.write(f"data: {json.dumps(d)}\n\n".encode()); self.wfile.flush()
      base={"id":cid,"object":"chat.completion.chunk","created":int(time.time()),"model":"mock-model"}
      ev({**base,"choices":[{"index":0,"delta":{"role":"assistant",**({"content":msg["content"]} if msg.get("content") else {}),**({"tool_calls":msg["tool_calls"]} if msg.get("tool_calls") else {})},"finish_reason":None}]})
      ev({**base,"choices":[{"index":0,"delta":{},"finish_reason":fin}],"usage":{"prompt_tokens":10,"completion_tokens":5,"total_tokens":15}})
      self.wfile.write(b"data: [DONE]\n\n"); self.wfile.flush()
    else:
      b=json.dumps({"id":cid,"object":"chat.completion","created":int(time.time()),"model":"mock-model","choices":[{"index":0,"message":msg,"finish_reason":fin}],"usage":{"prompt_tokens":10,"completion_tokens":5,"total_tokens":15}}).encode()
      self.send_response(200);self.send_header("content-type","application/json");self.end_headers();self.wfile.write(b)
ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
