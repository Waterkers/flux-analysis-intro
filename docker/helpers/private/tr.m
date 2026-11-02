function s = tr(key, varargin)
% Look up a helper message in the current language and fill in its values.
  m = messages(currentLanguage());
  s = sprintf(m.(key), varargin{:});
end
