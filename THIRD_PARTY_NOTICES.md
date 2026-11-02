# Third-party software and data

This repository's own files are licensed under MIT and CC BY 4.0, see the License section of [README.md](README.md). It contains only its own files: scripts, Octave helper functions, notebooks and documentation. The software and data below are **not** included in the repository. They are downloaded when the Docker image is built, so they **are** included in every built image (for example one published to a container registry, or the `.tar.gz` file for USB sticks).

| Component | Version | Source | License |
|---|---|---|---|
| *E. coli* core model (`e_coli_core`) | BiGG, 2019 | <http://bigg.ucsd.edu/models/e_coli_core> | BiGG Models license: free for educational, research and non-profit use; **commercial use requires permission from UC San Diego**. The full text ships with the model in the image as `/opt/models/LICENSE-BiGG.txt` (source: [`docker/LICENSE-BiGG.txt`](docker/LICENSE-BiGG.txt)). |
| COBRA Toolbox | v3.7.1 | <https://github.com/opencobra/cobratoolbox> | GPL-3.0. Six lines are changed at build time to work under Octave, see [`docker/patch_cobra.py`](docker/patch_cobra.py). |
| GNU Octave | 11.1 (Ubuntu package) | <https://octave.org> | GPL-3.0-or-later |
| GLPK (GNU Linear Programming Kit) | Ubuntu package, built into Octave | <https://www.gnu.org/software/glpk/> | GPL-3.0-or-later |
| gnuplot | Ubuntu package | <http://gnuplot.info> | gnuplot license (free software) |
| Jupyter Docker Stacks (`minimal-notebook`) | 2026-10-12 | <https://github.com/jupyter/docker-stacks> | BSD-3-Clause |
| JupyterLab and German language pack | 4.6.4 / 4.5.post3 | <https://jupyter.org> | BSD-3-Clause |
| `octave_kernel` | 1.1.1 | <https://github.com/Calysto/octave_kernel> | BSD-3-Clause |
| Ubuntu | 26.04 | <https://ubuntu.com> | various free-software licenses, see `/usr/share/doc/*/copyright` in the image |

The source code of all GPL components is publicly available at the sources above; the COBRA Toolbox version used is the tag `v3.7.1`, plus the changes in `docker/patch_cobra.py`.

## Publications

If you build on this practical, please cite the work it relies on:

* **Model:** Orth JD, Fleming RMT, Palsson BØ (2010). Reconstruction and use of microbial metabolic networks: the core *Escherichia coli* metabolic model as an educational guide. *EcoSal Plus* 4(1). [doi:10.1128/ecosalplus.10.2.1](https://doi.org/10.1128/ecosalplus.10.2.1)
* **Database:** King ZA, Lu JS, Dräger A, Miller PC, Federowicz S, Lerman JA, Ebrahim A, Palsson BO, Lewis NE (2016). BiGG Models: A platform for integrating, standardizing and sharing genome-scale models. *Nucleic Acids Research* 44(D1):D515–D522. [doi:10.1093/nar/gkv1049](https://doi.org/10.1093/nar/gkv1049)
* **Software:** Heirendt L, Arreckx S, Pfau T, et al. (2019). Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0. *Nature Protocols* 14:639–702. [doi:10.1038/s41596-018-0098-2](https://doi.org/10.1038/s41596-018-0098-2)
* **Method:** Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28:245–248. [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614)
