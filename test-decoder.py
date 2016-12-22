#! /usr/bin/env python3
""" Test suite to verify wireshark bitcoin dissector."""

import argparse
import difflib
import json
import logging
import os
import subprocess
import sys

def run_test(test_name):
    pcap_file = os.path.join("test", test_name) + ".pcap"
    json_file = pcap_file.strip(".pcap") + ".json"
    # print(json_file, pcap_file)

    # Parse the .json file
    comparison_out = open(json_file).read()
    comparison_json = json.loads(comparison_out)
    # print(outjson)

    # Use tshark to decode the .pcap file
    process_out = subprocess.run(["tshark","-r", pcap_file, "-T", "json"], stdout = subprocess.PIPE, universal_newlines = True).stdout
    process_json = json.loads(process_out)[0]

    # Compare the two
    if comparison_json != process_json["_source"]["layers"]["bitcoin"]:
        error_message = "Output formatting mismatch for " + test_name + ":\n"
        error_message += "".join(difflib.context_diff([str(comparison_json)],
                                                      [str(process_json["_source"]["layers"]["bitcoin"])],
                                                      fromfile=json_file,
                                                      tofile="returned"))
        logging.error(error_message)
        raise Exception

    # Make sure that the message wasn't malformed
    if "_ws.malformed" in process_json["_source"]["layers"]:
        error_message = "Malformed packet:" + test_name + ":\n"
        error_message += ["_source"]["layers"]["_ws.malformed"]
        raise Exception

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    verbose = args.verbose

    if verbose:
        level = logging.DEBUG
    else:
        level = logging.ERROR
    formatter = '%(asctime)s - %(levelname)s - %(message)s'
    # Add the format/level to the logger
    logging.basicConfig(format = formatter, level=level)

    failed_testcases = []

    for filename in os.listdir("test"):
        # Find all the .pcap files in the /test directory.
        if filename.endswith(".pcap"): 
            try:
                run_test(filename.strip(".pcap"))
                logging.info("PASSED: " + filename)
            except:
                logging.info("FAILED: " + filename)
                failed_testcases.append(filename)

    if failed_testcases:
        logging.error("FAILED TESTCASES: [" + ", ".join(failed_testcases) + "]")
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()
