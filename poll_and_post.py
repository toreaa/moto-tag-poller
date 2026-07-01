import os, sys, io, signal, re, contextlib, json, urllib.request
from NovaApi.ExecuteAction.LocateTracker.location_request import get_location_data_for_device

CANONIC = os.environ.get("MOTO_CANONIC_ID", "685e3527-0000-24a6-82a1-34c7e9217343")
NAME = os.environ.get("MOTO_NAME", "moto tag")
POST_URL = os.environ["POST_URL"]              # f.eks. https://motorolatrack.vercel.app/api/position
SECRET = os.environ["SHARE_SECRET"]
TIMEOUT = int(os.environ.get("LOC_TIMEOUT", "120"))

class Timeout(Exception): pass
def _to(sig, frm): raise Timeout()
signal.signal(signal.SIGALRM, _to)
signal.alarm(TIMEOUT)

buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        get_location_data_for_device(CANONIC, NAME)
except Timeout:
    pass
except SystemExit as e:
    print(f"SYSEXIT {e}", file=sys.stderr)
finally:
    signal.alarm(0)

out = buf.getvalue()
print(out, file=sys.stderr)

lats = re.findall(r'Latitude:\s*([-\d.]+)', out)
lngs = re.findall(r'Longitude:\s*([-\d.]+)', out)
if not lats:
    print("NO_LOCATION", file=sys.stderr)
    sys.exit(2)

lat = float(lats[-1]); lng = float(lngs[-1])

body = json.dumps({"lat": lat, "lng": lng}).encode()
url = POST_URL + ("&" if "?" in POST_URL else "?") + "secret=" + urllib.parse.quote(SECRET)
req = urllib.request.Request(url, data=body, headers={"content-type": "application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"POSTED lat={lat} lng={lng} -> HTTP {r.status}")
