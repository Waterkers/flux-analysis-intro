function model = knockOut(model, gene)
% model = knockOut(model, gene)  Switch off a gene, by name ('eno') or ID ('b2779').
%   Schaltet ein Gen aus, über den Namen ('eno') oder die ID ('b2779').
  idx = find(strcmp(model.genes, gene) | strcmp(model.geneNames, gene), 1);
  if isempty(idx)
    error(tr('unknownGene', gene));
  end
  fprintf(tr('knockedOut', model.geneNames{idx}, model.genes{idx}));
  model = deleteModelGenes(model, model.genes{idx});   % also renames the gene to <id>_deleted
end
