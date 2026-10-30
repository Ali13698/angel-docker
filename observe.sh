#!/bin/sh
# Read-only snapshot: no restart, exec, env dump or container mutation.
set -eu

if [ "$#" -ne 1 ]; then
  echo "usage: $0 CONTAINER_NAME_OR_ID" >&2
  exit 2
fi

case "$1" in
  -*|'')
    echo "invalid container" >&2
    exit 2
    ;;
esac

command -v docker >/dev/null

docker inspect \
  --format 'status={{.State.Status}} oom={{.State.OOMKilled}} exit={{.State.ExitCode}} restarts={{.RestartCount}} memory={{.HostConfig.Memory}} memorySwap={{.HostConfig.MemorySwap}} nanoCPUs={{.HostConfig.NanoCpus}} pids={{.HostConfig.PidsLimit}}' \
  "$1"

docker stats \
  --no-stream \
  --format 'name={{.Name}} cpu={{.CPUPerc}} memory={{.MemUsage}} pids={{.PIDs}}' \
  "$1"
