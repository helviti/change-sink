#!/usr/bin/env python
import subprocess
import sys
import json


def get_sinks():
    cmd = subprocess.run(
        ["pactl", "--format", "json", "list", "sinks"], capture_output=True
    )
    if cmd.returncode != 0:
        raise Exception(
            f"Failed to run command: {cmd.stdout.decode()} {cmd.stderr.decode()}"
        )

    output = cmd.stdout.decode()
    jsonDecoded = json.loads(output)

    return jsonDecoded


def set_default_sink(sink):
    print(f"Setting default sink to: id={sink['index']} name={sink['properties']['device.product.name']}")
    cmd = subprocess.run(
        ["pactl", "set-default-sink", f"{sink['index']}"], capture_output=True
    )
    if cmd.returncode != 0:
        raise Exception(
            f"Failed to run command: {cmd.stdout.decode()} {cmd.stderr.decode()}"
        )


def get_default_sink_name():
    cmd = subprocess.run(["pactl", "get-default-sink"], capture_output=True)
    if cmd.returncode != 0:
        raise Exception(
            f"Failed to run command: {cmd.stdout.decode()} {cmd.stderr.decode()}"
        )

    return cmd.stdout.decode().rstrip("\n")


def main():
    if len(sys.argv) < 2:
        raise Exception("No mode found. Usage: python main.py (switch|show|list)")

    mode = sys.argv[1]

    sinks = get_sinks()
    default_sink = next(
        filter(lambda s: s["name"] == get_default_sink_name(), sinks), None
    )

    if default_sink is None:
        raise Exception("No default sink found")

    if mode == "switch":
        for idx, _ in enumerate(sinks):
            # continue until default sink is found
            if sinks[idx]["index"] != default_sink["index"]:
                continue
            # no next element, switch to first
            if idx + 1 == len(sinks):
                set_default_sink(sinks[0])
                return
            # next element exists, switch to it
            else:
                set_default_sink(sinks[idx + 1])
                return
    elif mode == "show":
        print(json.dumps(default_sink, indent=2))
    elif mode == "list":
        print(json.dumps(sinks, indent=2))
    else:
        raise Exception(
            f"Unsupported mode: '{mode}'. Usage: python main.py (switch|show|list)"
        )


if __name__ == "__main__":
    raise SystemExit(main())
