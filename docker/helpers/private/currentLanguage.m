function lang = currentLanguage()
% Language chosen with setLanguage(), else $PRACTICAL_LANG, else English.
  global PRACTICAL_LANGUAGE
  lang = PRACTICAL_LANGUAGE;
  if isempty(lang)
    lang = getenv('PRACTICAL_LANG');
  end
  if ~strcmp(lang, 'de')
    lang = 'en';
  end
end
