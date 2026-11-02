function model = setMedium(model, glucose, oxygen)
% model = setMedium(model, glucose, oxygen)
%   Let the cells take up at most `glucose` and `oxygen` (mmol per gram per hour).
%   Die Zellen dürfen höchstens `glucose` und `oxygen` aufnehmen (mmol pro Gramm pro Stunde).
%   Example / Beispiel: model = setMedium(model, 10, 0)   % no oxygen / ohne Sauerstoff
  model = changeRxnBounds(model, 'EX_glc__D_e', -abs(glucose), 'l');
  model = changeRxnBounds(model, 'EX_o2_e', -abs(oxygen), 'l');
  fprintf(tr('medium', abs(glucose), abs(oxygen)));
end
