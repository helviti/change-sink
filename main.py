#!/usr/bin/env python
import subprocess
import sys
import json

def get_sinks():
    cmd = subprocess.run(["pactl","--format","json","list","short","sinks"],capture_output=True)
    if cmd.returncode != 0:
        raise Exception(f"Failed to run command: {cmd.stdout.decode()} {cmd.stderr.decode()}")

    output = cmd.stdout.decode()
    jsonDecoded = json.loads(output)

    return jsonDecoded

def set_default_sink(sink):
    print(f"Setting default sink to: id={sink['index']} name={sink['name']}")
    cmd = subprocess.run(["pactl","set-default-sink",f"{sink['index']}"],capture_output=True)
    if cmd.returncode != 0:
        raise Exception(f"Failed to run command: {cmd.stdout.decode()} {cmd.stderr.decode()}")

def main():
    if len(sys.argv) < 2:
        raise Exception("No mode found. Usage: python main.py (switch|show)")

    mode = sys.argv[1]

    sinks = get_sinks()
    default_sink_list = [sink for sink in sinks if sink['state'] == 'RUNNING']
    if len(default_sink_list) == 0:
        raise Exception('No default sink found')

    default_sink = default_sink_list[0]
    default_sink_id = default_sink['index']

    if mode == 'switch':
        for idx, _ in enumerate(sinks):
            # continue until default sink is found
            if sinks[idx]['state'] != 'RUNNING':
                continue

            # no next element, switch to first
            if idx+1 == len(sinks):
                set_default_sink(sinks[0])
            # next element exists, switch to it
            else:
                set_default_sink(sinks[idx+1])
    elif mode == 'show':
        print(json.dumps(default_sink,indent=2))
    else:
        raise Exception(f"Unsupported mode: '{mode}'. Usage: python main.py (switch|show)")

if __name__ == '__main__':
    raise SystemExit(main())
