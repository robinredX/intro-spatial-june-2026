import argparse
import os
import sys
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

KIDNEY_PAGE = "https://www.10xgenomics.com/datasets/human-kidney-preview-data-xenium-human-multi-tissue-and-cancer-panel-1-standard"


def default_data_dir():
    env = os.environ.get("SPATIAL_COURSE_DATA")
    if env:
        return env
    shared = Path("/home/shared/spatial_course_data")
    if shared.exists():
        return str(shared)
    return str(Path.home() / "spatial_course_data")


def stage_visium(data_dir):
    out = data_dir / "visium_lymph_node.h5ad"
    if out.exists():
        print("visium: already present")
        return
    import scanpy as sc
    print("visium: downloading human lymph node section ...")
    adata = sc.datasets.visium_sge(sample_id="V1_Human_Lymph_Node")
    adata.var_names_make_unique()
    adata.write(out)
    print("visium: saved", out)


def stage_seqfish(data_dir):
    out = data_dir / "seqfish_embryo.h5ad"
    if out.exists():
        print("seqfish: already present")
        return
    import squidpy as sq
    print("seqfish: downloading mouse embryo section ...")
    adata = sq.datasets.seqfish()
    adata.write(out)
    print("seqfish: saved", out)


def stage_xenium(data_dir, url):
    target = data_dir / "xenium_kidney"
    if (target / "cell_feature_matrix.h5").exists() and (
        (target / "cells.parquet").exists() or (target / "cells.csv.gz").exists()
    ):
        print("xenium: already present")
        return
    target.mkdir(parents=True, exist_ok=True)
    if not url:
        print("xenium: no URL given.")
        print("  Open the dataset page, click 'Xenium Output Bundle', and unzip it into:")
        print("   ", target)
        print("  so that cell_feature_matrix.h5 and cells.parquet sit directly inside.")
        print("  Page:", KIDNEY_PAGE)
        print("  Then pass --xenium-url <link> to download it automatically next time.")
        return
    zpath = data_dir / "xenium_kidney_outs.zip"
    print("xenium: downloading", url)
    urlretrieve(url, zpath)
    print("xenium: extracting ...")
    with zipfile.ZipFile(zpath) as zf:
        zf.extractall(target)
    flat = list(target.rglob("cell_feature_matrix.h5"))
    if flat and flat[0].parent != target:
        src = flat[0].parent
        for item in src.iterdir():
            item.rename(target / item.name)
    zpath.unlink(missing_ok=True)
    print("xenium: ready in", target)


def main():
    ap = argparse.ArgumentParser(description="Stage course datasets into a shared folder.")
    ap.add_argument("--data-dir", default=default_data_dir())
    ap.add_argument("--xenium-url", default="")
    ap.add_argument("--only", choices=["visium", "xenium", "seqfish"], default=None)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    print("staging into:", data_dir)

    steps = {
        "visium": lambda: stage_visium(data_dir),
        "seqfish": lambda: stage_seqfish(data_dir),
        "xenium": lambda: stage_xenium(data_dir, args.xenium_url),
    }
    for name, fn in steps.items():
        if args.only and args.only != name:
            continue
        try:
            fn()
        except Exception as e:
            print(f"{name}: failed: {e}", file=sys.stderr)

    print("done")


if __name__ == "__main__":
    main()
