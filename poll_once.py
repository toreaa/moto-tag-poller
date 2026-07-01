import sys, io, signal, re, contextlib
from NovaApi.ExecuteAction.LocateTracker.location_request import get_location_data_for_device

CANONIC = "685e3527-0000-24a6-82a1-34c7e9217343"
NAME = "moto tag"
TIMEOUT = int(sys.argv[1]) if len(sys.argv) > 1 else 120

class Timeout(Exception):
    pass

def _to(sig, frm):
    raise Timeout()

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
print(out, file=sys.stderr)   # full logg til stderr

lats = re.findall(r'Latitude:\s*([-\d.]+)', out)
lngs = re.findall(r'Longitude:\s*([-\d.]+)', out)
times = re.findall(r'Time:\s*([\d-]+\s[\d:]+)', out)

if not lats:
    print("NO_LOCATION")
    sys.exit(2)

# nyeste = siste utskrevne blokk
print(f"RESULT\tlat={lats[-1]}\tlng={lngs[-1]}\ttime={times[-1] if times else '?'}")
