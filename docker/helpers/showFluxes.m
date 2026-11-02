function showFluxes(model, solution, n)
% showFluxes(model, solution, n)  Bar chart of the n reactions with the largest flux.
%   Balkendiagramm der n Reaktionen mit dem größten Fluss (Standard: n = 15).
  if nargin < 3
    n = 15;
  end
  [~, order] = sort(abs(solution.x), 'descend');
  top = order(min(n, numel(order)):-1:1);
  barh(solution.x(top));
  set(gca, 'ytick', 1:numel(top), 'yticklabel', strrep(model.rxns(top), '_', '\_'));
  xlabel(tr('fluxLabel'));
  title(tr('fluxTitle', numel(top)));
  grid on

  % The chart only has room for IDs, so list the full names as well.
  for k = fliplr(top(:)')
    fprintf('  %-12s %8.2f   %s\n', model.rxns{k}, solution.x(k), model.rxnNames{k});
  end
end
