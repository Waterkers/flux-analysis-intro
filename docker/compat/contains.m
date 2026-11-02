function tf = contains(str, pattern, varargin)
% Minimal stand-in for MATLAB's contains(), which Octave does not provide.
% Supports char or cellstr inputs and the 'IgnoreCase' option.
  ignoreCase = false;
  for k = 1:2:numel(varargin)
    if strcmpi(varargin{k}, 'IgnoreCase')
      ignoreCase = logical(varargin{k + 1});
    end
  end
  if ischar(pattern)
    pattern = {pattern};
  end
  wasChar = ischar(str);
  if wasChar
    str = {str};
  end
  if ignoreCase
    str = lower(str);
    pattern = lower(pattern);
  end
  tf = false(size(str));
  for p = 1:numel(pattern)
    tf = tf | ~cellfun(@isempty, strfind(str, pattern{p}));
  end
end
