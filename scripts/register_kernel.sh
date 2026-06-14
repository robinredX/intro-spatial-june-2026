#!/usr/bin/env bash
# Register the course conda environment as a Jupyter kernel, so it shows up in the
# JupyterLab launcher / "Change Kernel" menu as "Python (env-spatial-course)".
#
# Run this once after creating the environment:
#   conda env create -f environment.yml
#   conda activate env-spatial-course
#   bash scripts/register_kernel.sh
#
# It installs the kernel for your user only (no admin rights needed). To make the
# kernel available to every user on a shared JupyterHub instead, drop --user (you
# then need write access to the shared kernels directory).
set -euo pipefail

ENV_NAME="env-spatial-course"
DISPLAY_NAME="Python (env-spatial-course)"

if ! python -c "import ipykernel" 2>/dev/null; then
  echo "ipykernel is not importable in the active environment."
  echo "Activate the course environment first:  conda activate ${ENV_NAME}"
  exit 1
fi

python -m ipykernel install --user --name "${ENV_NAME}" --display-name "${DISPLAY_NAME}"

echo
echo "Done. In JupyterLab pick the '${DISPLAY_NAME}' kernel"
echo "(launcher tile, or Kernel > Change Kernel inside a notebook)."
echo "List installed kernels with:  jupyter kernelspec list"
