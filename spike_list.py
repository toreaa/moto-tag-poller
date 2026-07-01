import sys
from NovaApi.ListDevices.nbe_list_devices import request_device_list
from ProtoDecoders.decoder import parse_device_list_protobuf, get_canonic_ids

# Foerste kjoering: trigger auth (Chrome-innlogging), deretter list enheter.
result_hex = request_device_list()
device_list = parse_device_list_protobuf(result_hex)
canonic_ids = get_canonic_ids(device_list)

print("=== DEVICES START ===", flush=True)
for i, (name, cid) in enumerate(canonic_ids):
    print(f"{i}\t{name}\t{cid}", flush=True)
print("=== DEVICES END ===", flush=True)
