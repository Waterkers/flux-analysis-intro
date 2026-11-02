function showFluxes(model, solution, n)
% showFluxes(model, solution, n)  Bar chart of the n reactions with the largest flux.
%   Balkendiagramm der n Reaktionen mit dem größten Fluss (Standard: n = 15).
  if nargin < 3
    n = 15;
  end
  % Round before sorting: reactions with the same flux (e.g. GAPD and PGK) differ only
  % in the last digits, which vary between processors. Rounded, they tie, and the sort
  % keeps ties in model order, so every computer shows the same chart.
  [~, order] = sort(round(abs(solution.x) * 1e6), 'descend');
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
