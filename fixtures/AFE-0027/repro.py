from sweagent.tools.parsing import ThoughtActionParser
from sweagent.tools.commands import Command
import subprocess, json
p = ThoughtActionParser()
# model output shaped as in the issue: prose thought + a fenced block whose content is a JSON object
out = 'I will view the file.\n```\n{\n  "command": "view",\n  "path": "/test-repo/tests/missing_colon.py"\n}\n```'
thought, action = p({"message": out}, [])
print("PARSED_ACTION:", repr(action))
r = subprocess.run(["bash","-c",action],capture_output=True,text=True)
print("BASH_RC:", r.returncode); print("STDERR:", r.stderr)
