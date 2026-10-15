import sys,types
m=types.ModuleType('daytona_sdk'); m.__getattr__=lambda n: type(n,(),{})
sys.modules['daytona_sdk']=m  # stub: unrelated optional runtime dep with a broken pin
import inspect, json
from litellm import ModelResponse
from openhands.agenthub.codeact_agent import function_calling as fc
print("signature:", inspect.signature(fc.response_to_actions))
resp = ModelResponse(id="x", model="devstral", choices=[{"index":0,"finish_reason":"tool_calls","message":{"role":"assistant","content":"Running it.","tool_calls":[{"id":"call_1","type":"function","function":{"name":"execute_code","arguments":json.dumps({"code":"print(1)"})}}]}}])
try:
    a = fc.response_to_actions(resp)
    print("ACTIONS:", a)
except Exception as e:
    print("EXCEPTION:", type(e).__name__, "|", e)
