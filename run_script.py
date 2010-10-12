import sys, os
from batman_app import db, app

conn = app.test_request_context()
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if len(sys.argv) > 1:
    conn.push()
    script_name = sys.argv[1]
    sys.argv = sys.argv[1:]
    execfile(script_name)
    conn.pop()
else:
    sys.exit()

