% Set up the COBRA Toolbox for this container without running initCobraToolbox.
% initCobraToolbox insists on git submodules and uses MATLAB-only functions, so we
% put the toolbox on the path and set the solver globals it would have set ourselves.

warning('off', 'Octave:shadowed-function');
warning('off', 'Octave:language-extension');
warning('off', 'Octave:possible-matlab-short-circuit-operator');
warning('off', 'Octave:str-to-num');

global CBTDIR SOLVERS OPT_PROB_TYPES ENV_VARS
global CBT_LP_SOLVER CBT_MILP_SOLVER CBT_QP_SOLVER CBT_MIQP_SOLVER
global CBT_NLP_SOLVER CBT_EP_SOLVER CBT_CLP_SOLVER

CBTDIR = '/opt/cobratoolbox';

% Only src/ and the one external utility it needs: external/ also contains a
% MATLAB-only glpk.m that would hide Octave's built-in glpk().
addpath(genpath(fullfile(CBTDIR, 'src')), ...
        fullfile(CBTDIR, 'external', 'base', 'utilities', 'textprogressbar'));
addpath('/opt/cobra-setup/compat', '/opt/cobra-setup/helpers');

OPT_PROB_TYPES = {'LP', 'MILP', 'QP', 'MIQP', 'NLP', 'EP', 'CLP'};
SOLVERS = struct();
SOLVERS.glpk = struct('type', {{'LP', 'MILP'}}, 'categ', 'active', ...
                      'installed', true, 'working', true);
ENV_VARS.printLevel = false;
ENV_VARS.STATUS = 1;

% GLPK is built into Octave and solves both LP and MILP problems.
CBT_LP_SOLVER = 'glpk';
CBT_MILP_SOLVER = 'glpk';
CBT_QP_SOLVER = '';
CBT_MIQP_SOLVER = '';
CBT_NLP_SOLVER = '';
CBT_EP_SOLVER = '';
CBT_CLP_SOLVER = '';

% Plots: gnuplot works without a display, and inline in Jupyter. Hide Octave's
% notice that gnuplot is discouraged; students can't act on it.
previousWarnings = warning('off', 'all');
graphics_toolkit('gnuplot');
warning(previousWarnings);
clear previousWarnings
