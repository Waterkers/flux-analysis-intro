function [growth, solution] = showGrowth(model)
% growth = showGrowth(model)  Run FBA (maximise growth) and print the growth rate.
%   Führt FBA aus (Wachstum maximieren) und zeigt die Wachstumsrate.
%   [growth, solution] = showGrowth(model) also returns all fluxes in solution.x.
  solution = optimizeCbModel(model);
  if solution.stat ~= 1
    growth = 0;
    fprintf(tr('infeasible'));
  elseif solution.f < 1e-6
    growth = 0;
    fprintf(tr('noGrowth'));
  else
    growth = solution.f;
    fprintf(tr('growth', growth, 60 * log(2) / growth));
  end
end
