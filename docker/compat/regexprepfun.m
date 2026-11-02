function out = regexprepfun(str, pattern, fun)
% Octave-compatible replacement for MATLAB's regexprep(str, pattern, '${expr}').
% fun is called as fun(tok) for every match, where tok = {wholeMatch, token1, token2, ...},
% and must return the replacement text. str may be a char array or a cell array of them.
  if iscell(str)
    out = cellfun(@(s) regexprepfun(s, pattern, fun), str, 'UniformOutput', false);
    return
  end
  [matches, tokens, pieces] = regexp(str, pattern, 'match', 'tokens', 'split');
  out = pieces{1};
  for k = 1:numel(matches)
    out = [out, fun([matches(k), tokens{k}]), pieces{k + 1}];
  end
end
