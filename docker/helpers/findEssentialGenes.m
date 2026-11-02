function genes = findEssentialGenes(model)
% genes = findEssentialGenes(model)  Knock out every gene, one at a time, and list
%   the genes without which the cells cannot grow.
%   Schaltet jedes Gen einzeln aus und zeigt die Gene, ohne die die Zellen nicht wachsen.
  % evalc hides COBRA's progress bar, which floods a notebook cell.
  evalc('[grRatio, growthKO] = singleGeneDeletion(model, ''FBA'', model.genes, false);');
  growthKO(isnan(growthKO)) = 0;
  growthKO = max(growthKO, 0);   % solver noise can give -0.000
  essential = find(growthKO < 1e-6);
  fprintf(tr('essentialHead', numel(essential), numel(model.genes)));
  for k = essential'
    fprintf(tr('geneLine', model.geneNames{k}, model.genes{k}, growthKO(k)));
  end
  genes = model.geneNames(essential);
end
