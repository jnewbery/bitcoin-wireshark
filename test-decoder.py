#! /usr/bin/env python3
""" Test suite to verify wireshark bitcoin dissector."""

import json
import os
import subprocess

for filename in os.listdir("test"):
    if filename.endswith(".pcap"): 
        # Find all the .pcap files in the /test directory. There should be a matching .json file.
        pcap_file = os.path.join("test", filename)
        json_file = pcap_file.strip(".pcap") + ".json"
        # print(json_file, pcap_file)

        # Parse the .json file
        comparison_json = json.loads(open(json_file).read())
        # print(outjson)

        # Use tshark to decode the .pcap file
        process_out = subprocess.run(["tshark","-r", pcap_file, "-T", "json"], stdout = subprocess.PIPE, universal_newlines = True).stdout
        process_json = json.loads(process_out)[0]

        # Compare the two
        if comparison_json != process_json["_source"]["layers"]["bitcoin"]:
            raise Exception

        # Make sure that the message wasn't malformed
        if "_ws.malformed" in process_json["_source"]["layers"]:
            print("Malformed packet:")
            print(process_json["_source"]["layers"]["_ws.malformed"])
            raise Exception
        continue
    else:
        continue

