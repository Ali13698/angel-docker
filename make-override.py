#!/usr/bin/env python3
"""Generate ONLY a Compose override; never starts or modifies a container."""

import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument(
    "--service",
    required=True,
    help="Exact existing Compose game-host service name",
)
parser.add_argument("--cpus", type=float, default=2)
parser.add_argument("--memory", default="1g")
parser.add_argument("--pids", type=int, default=256)
args = parser.parse_args()

if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", args.service):
    parser.error("Invalid service name")

if not 0 < args.cpus <= 64:
    parser.error("CPU limit must be greater than 0 and at most 64")

if not 32 <= args.pids <= 4096:
    parser.error("PID limit must be between 32 and 4096")

if not re.fullmatch(r"[1-9][0-9]*[mg]", args.memory):
    parser.error("Memory must be e.g. 1g or 768m")

override = {
    "services": {
        args.service: {
            "cpus": str(args.cpus),
            "mem_limit": args.memory,
            "memswap_limit": args.memory,
            "pids_limit": args.pids,
            "cap_drop": ["ALL"],
            "security_opt": ["no-new-privileges:true"],
            "logging": {
                "driver": "json-file",
                "options": {
                    "max-size": "10m",
                    "max-file": "3",
                },
            },
        },
    },
}

print(json.dumps(override, indent=2))
