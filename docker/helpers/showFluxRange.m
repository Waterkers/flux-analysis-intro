function [minFlux, maxFlux] = showFluxRange(model, percent, reactions)
% showFluxRange(model, percent, reactions)  Flux variability analysis: the smallest and
%   largest flux each reaction can have while the cells still grow at least `percent` %
%   of their maximum. Prints a table and draws each range as a bar.
%   Flussvariabilitätsanalyse: kleinster und größter Fluss jeder Reaktion, solange die
%   Zellen noch mindestens `percent` % ihres maximalen Wachstums erreichen.
  if ischar(reactions)
    reactions = {reactions};
  end
  solution = optimizeCbModel(model);
  [minFlux, maxFlux] = fluxVariability(model, percent, 'max', reactions);
  % Round to 2 decimals: the solver leaves differences around 0.001 at the edges that
  % vary between processors. Rounded, every computer shows the same table.
  minFlux = round(minFlux * 100) / 100;
  maxFlux = round(maxFlux * 100) / 100;
  minFlux(minFlux == 0) = 0;   % no "-0.00"
  maxFlux(maxFlux == 0) = 0;

  fprintf('%s', tr('rangeHead', percent, percent / 100 * solution.f));   % '%s': the text contains a %
  fprintf(tr('rangeColumns'));
  for k = 1:numel(reactions)
    i = find(strcmp(model.rxns, reactions{k}));
    if strncmp(reactions{k}, 'EX_', 3)
      name = exchangeNames(reactions{k}, currentLanguage());
    else
      name = model.rxnNames{i};
    end
    if minFlux(k) == maxFlux(k)
      note = tr('rangeFixed');
    else
      note = '';
    end
    fprintf('  %-10s %8.2f %8.2f   %s%s\n', reactions{k}, minFlux(k), maxFlux(k), name, note);
  end

  n = numel(reactions);
  clf
  hold on
  for k = 1:n
    y = n + 1 - k;   % first reaction at the top
    plot([minFlux(k) maxFlux(k)], [y y], '-', 'linewidth', 8, 'color', [0.2 0.45 0.75]);
    % dots at both ends, so a fixed flux (no range) still shows up
    plot([minFlux(k) maxFlux(k)], [y y], 'o', 'markersize', 7, 'color', [0.1 0.2 0.4], 'markerfacecolor', [0.1 0.2 0.4]);
  end
  plot([0 0], [0.5 n + 0.5], 'k--');
  hold off
  ylim([0.5 n + 0.5]);
  % room around the dots, so none sits on the edge of the chart
  lo = min([minFlux(:); 0]);
  hi = max([maxFlux(:); 0]);
  pad = max(0.1 * (hi - lo), 1);
  xlim([lo - pad, hi + pad]);
  % gnuplot reads _ as subscript; tick labels need it escaped twice
  set(gca, 'ytick', 1:n, 'yticklabel', strrep(fliplr(reactions(:)'), '_', '\\_'));
  xlabel(tr('fluxLabel'));
  title(tr('rangeTitle', percent));
  grid on
end
