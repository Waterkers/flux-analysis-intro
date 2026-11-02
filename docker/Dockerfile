# FBA practical: JupyterLab + Octave kernel + GLPK + COBRA Toolbox + E. coli core model
# Multi-arch (linux/amd64, linux/arm64). Build context is this docker/ folder.

FROM quay.io/jupyter/minimal-notebook:2026-10-12

ARG COBRA_TAG=v3.7.1
ARG BIGG_URL=https://bigg.ucsd.edu/static/models
ARG MODEL_MAT_SHA256=478e6fa047ede1b248975d7565208ac9363a44dd64aad1900b63127394f4175b
ARG MODEL_JSON_SHA256=7bedec10576cfe935b19218dc881f3fb14f890a1871448fc19a9b4ee15b448d8

USER root

# Octave (its built-in glpk() is the LP solver), gnuplot + fonts for headless plots.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        octave gnuplot-nox ghostscript fonts-freefont-otf git ca-certificates curl \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Jupyter: Octave kernel and the German JupyterLab interface.
RUN pip install --no-cache-dir octave_kernel==1.1.1 jupyterlab-language-pack-de-DE==4.5.post3 \
 && fix-permissions "${CONDA_DIR}"

# COBRA Toolbox, pinned. Submodules are not needed for LP-based FBA with GLPK.
COPY patch_cobra.py /opt/cobra-setup/patch_cobra.py
RUN git clone --depth 1 --branch "${COBRA_TAG}" https://github.com/opencobra/cobratoolbox.git /opt/cobratoolbox \
 && rm -rf /opt/cobratoolbox/.git \
 && python3 -I /opt/cobra-setup/patch_cobra.py /opt/cobratoolbox

# E. coli core model from BiGG; the checksums make the build fail if BiGG changes the files.
# The .mat file is the model; the .json file only supplies gene names (b2779 -> eno).
COPY model_extras.py /opt/cobra-setup/model_extras.py
RUN mkdir -p /opt/models \
 && curl -fsSL -o /opt/models/e_coli_core.mat  "${BIGG_URL}/e_coli_core.mat" \
 && curl -fsSL -o /opt/models/e_coli_core.json "${BIGG_URL}/e_coli_core.json" \
 && echo "${MODEL_MAT_SHA256}  /opt/models/e_coli_core.mat"  | sha256sum -c - \
 && echo "${MODEL_JSON_SHA256}  /opt/models/e_coli_core.json" | sha256sum -c - \
 && python3 -I /opt/cobra-setup/model_extras.py /opt/models/e_coli_core.json /opt/models/e_coli_core_names.tsv
# The BiGG license requires its notice in every copy of the model, so it ships with it.
COPY LICENSE-BiGG.txt /opt/models/LICENSE-BiGG.txt

# Startup code, compatibility shims and student helpers. Everything under /opt stays
# root-owned and read-only for students.
COPY cobra_startup.m smoke_test.m /opt/cobra-setup/
COPY compat/ /opt/cobra-setup/compat/
COPY helpers/ /opt/cobra-setup/helpers/
COPY octaverc /usr/share/octave/site/m/startup/octaverc
COPY jupyterlab-language.sh /usr/local/bin/before-notebook.d/20-jupyterlab-language.sh
RUN chmod -R a+rX,go-w /opt/cobratoolbox /opt/cobra-setup /opt/models

# Fail the build if FBA does not give the known answers.
USER ${NB_UID}
RUN cd /tmp && octave-cli --norc --eval "source('/usr/share/octave/site/m/startup/octaverc'); run('/opt/cobra-setup/smoke_test.m')"

WORKDIR /home/${NB_USER}
ENV PRACTICAL_LANG=en
