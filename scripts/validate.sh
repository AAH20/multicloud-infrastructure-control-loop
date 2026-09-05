#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m unittest discover -s tests -v
work_dir="$(mktemp -d "${TMPDIR:-/tmp}/multicloud-control-loop-validation.XXXXXX")"
for fixture in azure-storage-public aws-s3-public gcp-storage-public kubernetes-privileged cloud-logging-disabled; do
  python3 -m control_loop.cli compile --input "examples/$fixture.json" --rules config/rules.json --output "$work_dir/$fixture"
done
python3 -m control_loop.cli verify --proposal "$work_dir/azure-storage-public/proposal.json" --post-change examples/azure-storage-remediated.json --output "$work_dir/azure-storage-public/verification.json"
python3 -m compileall -q src
echo "Validation passed; five proposal bundles are in $work_dir"