1;  % script file, not a function file
% Build-time check: the image is only published if FBA gives the known answers.
% Reference values: E. coli core model, glucose 10, oxygen 1000 (BiGG defaults).

function check(ok, what)
  if ok
    printf('  ok    %s\n', what);
  else
    error('SMOKE TEST FAILED: %s', what);
  end
end

global CBT_LP_SOLVER
printf('Smoke test\n');
check(strcmp(CBT_LP_SOLVER, 'glpk'), 'LP solver is GLPK');
check(strncmp(which('glpk'), '/usr/share/octave', 17), 'glpk() is Octave''s built-in version');

model = loadEcoli();
check(numel(model.rxns) == 95 && numel(model.mets) == 72 && numel(model.genes) == 137, ...
      'model has 95 reactions, 72 metabolites, 137 genes');
check(strcmp(model.geneNames{strcmp(model.genes, 'b2779')}, 'eno'), 'gene names loaded (b2779 = eno)');

growth = showGrowth(model);
check(abs(growth - 0.8739) < 1e-3, sprintf('aerobic growth %.4f ~ 0.8739', growth));

growth = showGrowth(setMedium(model, 10, 0));
check(abs(growth - 0.2117) < 1e-3, sprintf('anaerobic growth %.4f ~ 0.2117', growth));

growth = showGrowth(knockOut(model, 'eno'));
check(growth < 1e-6, 'eno knockout cannot grow');

growth = showGrowth(knockOut(model, 'b1723'));
check(abs(growth - 0.8739) < 1e-3, 'pfkB knockout grows normally (pfkA takes over)');

[minFlux, maxFlux] = fluxVariability(model, 100, 'max', {'PFK', 'EX_ac_e', 'SUCDi'});
check(abs(minFlux(1) - 7.477) < 1e-2 && abs(maxFlux(1) - 7.477) < 1e-2, ...
      sprintf('flux variability: PFK fixed at %.3f ~ 7.477 at maximum growth', minFlux(1)));
check(maxFlux(2) < 1e-3 && maxFlux(3) > 999, ...
      'flux variability: no acetate at maximum growth, SUCDi unbounded (FRD7 loop)');
[minFlux, maxFlux] = fluxVariability(model, 90, 'max', {'EX_ac_e'});
check(abs(maxFlux - 3.814) < 1e-2, sprintf('flux variability at 90%%: acetate up to %.3f ~ 3.814', maxFlux));
out = evalc('showFluxRange(model, 90, {''EX_ac_e''});');
check(~isempty(strfind(out, '3.81')), 'showFluxRange prints acetate up to 3.81 at 90%');

essential = findEssentialGenes(model);
check(isequal(sort(essential(:))', sort({'gltA', 'eno', 'ptsI', 'ptsH', 'gapA', 'icd', 'pgk'})), ...
      sprintf('essential genes on glucose: %s', strjoin(essential(:)', ', ')));

setLanguage('de');
check(~isempty(strfind(evalc('showGrowth(model);'), 'Wachstumsrate')), 'German helper output');
setLanguage('en');

h = figure('visible', 'off');
[~, sol] = showGrowth(model);
showFluxes(model, sol, 10);
f = [tempname() '.png'];
print(h, f, '-dpng');
check(exist(f, 'file') == 2, 'plotting works without a display');
delete(f); close(h);

printf('Smoke test passed.\n');
