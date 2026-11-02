**English** | [Deutsch](README.de.md)

# FBA practical: teacher guide

A ready-to-run setup for a short high-school practical on **flux balance analysis (FBA)**, as a taste of bioinformatics. Students work in **JupyterLab in their browser**. Behind it, a Docker container runs **GNU Octave**, the **GLPK** solver, the **COBRA Toolbox** and the ***E. coli* core model** from [BiGG](http://bigg.ucsd.edu/models/e_coli_core). Everything is available in **English and German**.

Students need about 45–60 minutes for notebooks 00–04; notebook 05 is a bonus.

## What's in this folder

| Path | What it is | Give to students? |
|---|---|---|
| `practical/en/`, `practical/de/` | the notebooks students work in; mounted into the container | yes |
| `practical/README*.md` | short student instructions | yes |
| `start.*`, `stop.*`, `docker-compose.yml`, `docker/` | starting and stopping, image definition | yes |
| `teacher/solutions/{en,de}/` | the same notebooks with solutions and outputs | **no** |
| `tools/` | notebook generator, checks, packaging script | no |

## Before the practical

### 1. Build the image

You need Docker (Docker Desktop on Windows/Mac). In this folder:

```bash
docker compose build
```

This takes a few minutes. It downloads Octave, the COBRA Toolbox and the model, then runs a **smoke test**. The build fails if FBA doesn't give the known results (growth 0.874 h⁻¹ with oxygen, 0.212 h⁻¹ without, 7 essential genes). The image is tagged `fba-practical:1.0`.

### 2. Get the image onto the students' computers

Choose one:

**a) USB stick / shared drive** (works without good internet):

```bash
tools/make_student_package.sh --with-image
```

This writes `dist/fba-practical-students.zip` and `dist/fba-practical-image.tar.gz` (about 1 GB). On each student computer, unzip the zip and load the image once:

```bash
docker load -i fba-practical-image.tar.gz
```

**b) A container registry** (e.g. GitHub Container Registry), so students can download it directly. Build for both Intel/AMD and Apple Silicon computers and push:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/YOUR-ACCOUNT/fba-practical:1.0 --push docker
```

Then copy `.env.example` to `.env`, set `FBA_IMAGE=ghcr.io/YOUR-ACCOUNT/fba-practical:1.0` there, and run `tools/make_student_package.sh` (without `--with-image`). The script puts your `.env` into the zip, so students get the same setting. (`.env` itself is not committed to the repository.) Students run `docker compose pull` once, or the start script pulls it the first time.

> The image built in step 1 only runs on computers with the same processor type as yours. For a class with a mix of Windows PCs and Apple Silicon Macs, use the `buildx` command above. On a Linux build machine, building for `arm64` needs QEMU emulation: `docker run --privileged --rm tonistiigi/binfmt --install arm64`.

### 3. Try it once

```bash
./start.sh       # English
./start.sh de    # Deutsch
```

Then go through the notebooks yourself. The solutions in `teacher/solutions/` show the expected output of every cell.

## During the practical

* **Windows:** double-click `start.bat` (English) or `start_de.bat` (Deutsch).
* **Mac:** double-click `start.command` or `start_de.command`. The first time, macOS may ask for permission: right-click → *Open*.
* **Linux:** `./start.sh` or `./start.sh de`.

The browser opens at `http://localhost:8888` in the right language folder. JupyterLab's own menus are also in that language. To stop: `stop.bat` / `./stop.sh`. Students' work stays in `practical/` on their computer.

JupyterLab is only reachable from the computer itself (`127.0.0.1`), so it runs without a password.

## Changing the notebooks

The notebooks are generated from **`tools/build_notebooks.py`**. Each cell is written in English and German side by side, and each exercise has a student version and a solution. After editing:

```bash
python3 tools/build_notebooks.py     # writes practical/ and teacher/solutions/
python3 tools/check_parity.py        # en and de must run the same code
tools/run_solutions.sh               # runs every solution notebook, so they contain outputs again
```

If you edit notebooks directly in JupyterLab instead, run `check_parity.py` afterwards. It reports any English/German pair whose code has drifted apart. Comments and text in quotes may differ; everything else must match.

`build_notebooks.py` overwrites `practical/`, so don't run it on a computer where students have already saved their work.

## Functions for students

The container adds a few small functions to keep the notebooks short. They are thin wrappers around COBRA Toolbox functions and live in `docker/helpers/`:

| Function | What it does |
|---|---|
| `setLanguage('en'/'de')` | language of everything below |
| `model = loadEcoli()` | load the model (adds gene names such as *eno* for `b2779`) |
| `model = setMedium(model, glucose, oxygen)` | maximum uptake of glucose and oxygen |
| `[growth, sol] = showGrowth(model)` | FBA; prints the growth rate and doubling time |
| `showExchange(model, sol)` | what the cells take up and release, with everyday names |
| `showFluxes(model, sol, n)` | bar chart of the *n* largest fluxes |
| `model = knockOut(model, 'eno')` | switch off a gene, by name or ID |
| `genes = findEssentialGenes(model)` | single-gene deletion: the genes the cells can't grow without |

Students also use the COBRA functions `changeRxnBounds`, `changeObjective`, `optimizeCbModel` and `printRxnFormula` directly. All texts printed by the helpers are in `docker/helpers/private/messages.m` and `exchangeNames.m`.

## How the container works

* **Base:** `quay.io/jupyter/minimal-notebook:2026-10-12` (Ubuntu 26.04, JupyterLab 4.6), with Octave 11 from Ubuntu, `octave_kernel` and the German JupyterLab language pack.
* **Solver:** GLPK, built into Octave as `glpk()`. No licence needed. It is plenty fast for the 95-reaction model.
* **COBRA Toolbox v3.7.1**, in `/opt/cobratoolbox`, read-only. `initCobraToolbox` is **not** used: under Octave it insists on git submodules and calls MATLAB-only functions. Instead, `docker/cobra_startup.m` puts `src/` on the path and sets the solver variables `initCobraToolbox` would set. It runs automatically in every Octave session through the site-wide `octaverc`.
* **Octave fixes:** `docker/patch_cobra.py` changes six lines of COBRA at build time. These cover:
  * NUL-padded text in `descFileRead`
  * reading GLPK's status from Octave's `glpk()`
  * `regexprep` with `${…}` expressions, which Octave doesn't support (four places)

  `docker/compat/` adds `contains()` and the `regexprepfun()` helper used by those fixes. The build fails if a patched line has moved in a newer COBRA version.
* **Model:** `e_coli_core.mat` and `e_coli_core.json` from BiGG, checked against fixed SHA-256 checksums. The JSON file only supplies gene names.
* **Not tested under Octave:** COBRA functions beyond those used in the notebooks. `fluxVariability` and `surfNet` are known not to work.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Docker is not running" | Start Docker Desktop and wait until it says it's running. |
| Windows: Docker Desktop asks for WSL 2 | Follow its instructions to install WSL 2 (needs admin rights once). |
| Port 8888 is already in use | Another Jupyter is running. Stop it, or change `127.0.0.1:8888` in `docker-compose.yml` and the start scripts. |
| `pull access denied for fba-practical` | The image isn't on this computer: `docker load -i fba-practical-image.tar.gz`, or set `FBA_IMAGE` in `.env` (copy it from `.env.example`). |
| Image fails on a Mac with an M chip: `exec format error` | The image was built for Intel only; build with `buildx` for both platforms (see step 2b). |
| Linux: files in `practical/` belong to another user | Start with `./start.sh`, which passes your user ID to the container. |
| Logs | `docker compose logs` |

## Credits and licenses

This practical is built on the work of others:

* **Model:** the *E. coli* core model, Orth JD, Fleming RMT, Palsson BØ (2010), *EcoSal Plus* 4(1), [doi:10.1128/ecosalplus.10.2.1](https://doi.org/10.1128/ecosalplus.10.2.1).
* **Database:** [BiGG Models](http://bigg.ucsd.edu), King ZA et al. (2016), *Nucleic Acids Research* 44(D1):D515–D522, [doi:10.1093/nar/gkv1049](https://doi.org/10.1093/nar/gkv1049).
* **Software:** [COBRA Toolbox](https://github.com/opencobra/cobratoolbox) v3.7.1, Heirendt L et al. (2019), *Nature Protocols* 14:639–702, [doi:10.1038/s41596-018-0098-2](https://doi.org/10.1038/s41596-018-0098-2); [GNU Octave](https://octave.org) with the [GLPK](https://www.gnu.org/software/glpk/) solver; [Jupyter](https://jupyter.org) and [`octave_kernel`](https://github.com/Calysto/octave_kernel).
* **Method:** Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28:245–248, [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614).

None of these are stored in this repository; they are downloaded when the image is built. Their licenses are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

**Note on the model license:** BiGG Models is free for educational, research and non-profit use only. A built image contains the model, so don't use or distribute the image commercially without permission from UC San Diego. The BiGG license text is included in the image as `/opt/models/LICENSE-BiGG.txt`.

## License

This repository uses two licenses:

| What | License |
|---|---|
| Notebooks (`practical/`, `teacher/`), the notebook texts in `tools/build_notebooks.py`, and the documentation (README files, `THIRD_PARTY_NOTICES.md`) | [CC BY 4.0](LICENSE-CC-BY-4.0.txt) |
| Everything else: code, scripts, Docker and Octave files | [MIT](LICENSE) |

Exceptions: `docker/LICENSE-BiGG.txt` is BiGG's license text, and `docker/patch_cobra.py` quotes the six COBRA Toolbox lines it changes (COBRA Toolbox: GPL-3.0). Third-party software and data used by the image keep their own licenses, see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

You're welcome to translate, shorten or adapt the notebooks for your own classes. Under CC BY 4.0, please credit them like this: *"Based on the FBA practical by the fba-practical contributors, CC BY 4.0"*, with a link to this repository.
