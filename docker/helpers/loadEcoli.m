function model = loadEcoli()
% model = loadEcoli()  Load the E. coli core model (BiGG: e_coli_core).
%   Lädt das E.-coli-Kernmodell (BiGG: e_coli_core).
  data = load('/opt/models/e_coli_core.mat');
  model = data.e_coli_core;
  model = rmfield(model, 'rev');      % old-style field, replaced by lb/ub
  model = generateRules(model);       % gene rules in the form COBRA's knockout functions need

  % Gene names (b2779 -> eno) from the BiGG JSON file, see model_extras.py.
  names = textscan(fileread('/opt/models/e_coli_core_names.tsv'), '%s %s %s', ...
                   'Delimiter', '\t', 'HeaderLines', 1);
  [found, idx] = ismember(model.genes, names{2});
  model.geneNames = model.genes;
  model.geneNames(found) = names{3}(idx(found));

  fprintf(tr('loaded', numel(model.rxns), numel(model.mets), numel(model.genes)));
end
