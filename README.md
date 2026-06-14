# Introduction to analysis of (single-cell) spatial transcriptomics data

A three-session hands-on course on spatial transcriptomics analysis with the
`scverse` stack (`scanpy`, `anndata`, `squidpy`, `spatialdata`).

Author: Dr. Robin Khatri, Institute of Medical Systems Bioinformatics, UKE.

## Schedule

| Day | Topic | Resources |
| --- | --- | --- |
| 1 | Foundations and a full Visium workflow | ~25 GB RAM, no GPU |
| 2 | Imaging-based data: Xenium | ~25 GB RAM, no GPU |
| 3 | Tissue organisation and interpretation (standalone) | ~6 GB RAM |

Each session is about 45 minutes of lecture (`slides_dayX.pdf`), a short hands-on
briefing, then two hours at the keyboard. The decks cover the workflow, the method
landscape (with citations), challenges, and further reading. The notebooks hold more
than fits in two hours by design, so they double as a take-home reference.

## Repository layout

```
environment.yml              conda environment for all three days
requirements.txt             pip equivalent for laptop / Colab
scripts/prefetch_data.py     stages datasets into the data folder
scripts/register_kernel.sh   registers the env as a JupyterLab kernel
theme/imsb_beamer.tex        shared Beamer style for the slides
day_0_setup/00_smoke_test.ipynb
day_1/  slides_day1.(tex|pdf)  01_tutorial.ipynb  01_solutions.ipynb
day_2/  slides_day2.(tex|pdf)  02_tutorial.ipynb  02_solutions.ipynb
day_3/  slides_day3.(tex|pdf)  03_tutorial.ipynb  03_solutions.ipynb
day_3/data/ligand_receptor_pairs.csv
```

## Tutorials and exercises

Each day has a **tutorial** notebook and a matching **solutions** notebook. The
tutorial has worked steps (the "spine") that run top to bottom, short method notes
that frame the choices at each step, and exercises left blank for you. The solutions
notebook is the same content with the exercises filled in. Exercises operate on
copies, so the spine still runs end to end even before you tackle them.

## Setup

Create the environment (its name is `env-spatial-course`):

```bash
conda env create -f environment.yml        # or: pip install -r requirements.txt
conda activate env-spatial-course
```

The first cell of every notebook ("Setup") also installs anything missing, so the
notebooks are safe to run on a fresh machine or in Colab.

### Use it in JupyterLab (kernel)

On a JupyterLab server, register the environment once so it appears as a selectable
kernel:

```bash
conda activate env-spatial-course
bash scripts/register_kernel.sh
```

That runs `python -m ipykernel install --user --name env-spatial-course
--display-name "Python (env-spatial-course)"`. Refresh JupyterLab, then pick
**Python (env-spatial-course)** from the launcher or via *Kernel ▸ Change Kernel*
inside a notebook. Check it is registered with `jupyter kernelspec list`.

If you would rather run a standalone JupyterLab from this environment instead:

```bash
conda activate env-spatial-course
jupyter lab
```

## Data

Every notebook resolves a data directory in this order: the `SPATIAL_COURSE_DATA`
environment variable, then `/home/shared/spatial_course_data` if it exists, then
`~/spatial_course_data` as a local fallback. Set `SPATIAL_COURSE_DATA` if your path
differs.

- **Visium** (Day 1) and **seqFISH** (Day 3) download automatically the first time a
  notebook needs them.
- **Xenium** (Day 2) is gated behind a button on the 10x dataset page, so it is the
  only dataset you stage manually (see below).

To stage everything up front (optional for Days 1 and 3):

```bash
python scripts/prefetch_data.py            # add --data-dir <path> to choose a location
```

### Downloading the Xenium dataset (Day 2)

1. Open the dataset page: Human Kidney (non-diseased), Xenium Human Multi-Tissue and
   Cancer panel —
   `https://www.10xgenomics.com/datasets/human-kidney-preview-data-xenium-human-multi-tissue-and-cancer-panel-1-standard`
   (you may need to sign in or accept terms).
2. Download the **Xenium Output Bundle** (a `.zip`).
3. Unzip it and place these two files **directly** inside `<data-dir>/xenium_kidney/`:
   - `cell_feature_matrix.h5`
   - the cell table: `cells.parquet` (or `cells.csv.gz` on older exports)

   If unzipping created a nested subfolder, move the two files up so they sit directly
   in `xenium_kidney/`. The bundle also contains large transcript and image files that
   this course does not load; you can delete them.

`<data-dir>` is your data folder (`~/spatial_course_data` locally or on Colab, or
whatever `SPATIAL_COURSE_DATA` points to). So locally the target is
`~/spatial_course_data/xenium_kidney/cell_feature_matrix.h5`, and so on.

## Running in three places

**Laptop.** A machine with 16 GB RAM is comfortable for Days 1 and 3; Day 2 wants
more headroom. Install once (above), then `jupyter lab` and open the notebooks.

**Shared server.** Put the data in a shared folder and point `SPATIAL_COURSE_DATA`
(or use `/home/shared/spatial_course_data`) so all accounts read the same copy.

**Google Colab.** Open a notebook, run the first "Setup" cell to install packages,
then run the rest. Visium and seqFISH download into the session automatically. For
Day 2, stage the Xenium bundle into the session (upload it, or download with
`gdown`/`curl`) and point `SPATIAL_COURSE_DATA` at it; Colab's ~12 GB RAM handles the
table-level Xenium read, but the bundle download is large.

## Run order

1. `day_0_setup/00_test.ipynb` at the start of each session (checks imports,
   runs two squidpy calls, and reports which datasets are reachable).
2. That day's `0X_tutorial.ipynb`. The `0X_solutions.ipynb` is the reference.

Processed objects are written to a local `results/` folder, not to the shared data
folder.

## Notes on memory and compute

- Day 2 reads only the Xenium cell-by-feature matrix and the cell table. It does not
  load `transcripts.parquet` or the morphology images; that is what exceeds 25 GB.
  Work on one section at a time.
- Day 3 is deliberately small and self-contained so it fits 6 GB and does not depend
  on Days 1 to 2.
- No GPU is required. Methods that practically need a GPU (e.g. scVI, cell2location)
  are discussed in the slides, not trained live.

## Datasets

- Visium human lymph node (10x, public).
- Xenium non-diseased human kidney, 377-gene Multi-Tissue panel (10x, public).
- seqFISH mouse embryo (via `squidpy.datasets.seqfish`, pre-annotated).

Xenium data can be downloaded [here](https://cf.10xgenomics.com/samples/xenium/1.5.0/Xenium_V1_hKidney_nondiseased_section/Xenium_V1_hKidney_nondiseased_section_outs.zip`).
All are public.

## Building the slides

The PDFs are included. To rebuild a deck from source:

```bash
cd day_1 && pdflatex slides_day1.tex && pdflatex slides_day1.tex
```

Run `pdflatex` twice so the footer frame counts resolve. The other decks build the
same way.
