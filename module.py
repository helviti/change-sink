import time
import json
import subprocess

import main

prev_sink = None

while True:
    sinks = main.get_sinks()
    default_sink = next(
        filter(lambda s: s["name"] == main.get_default_sink_name(), sinks), None
    )

    if default_sink is not None:
        descr = default_sink["description"]

        if prev_sink != descr:
            if "Scarlett" in descr:
                text = "Headphones  "
            elif "Starship" in descr:
                text = "Speakers  "
            else:
                text = "unknown device"
            print(json.dumps({"text":text}), flush=True)

        prev_sink = descr

    time.sleep(0.2)
