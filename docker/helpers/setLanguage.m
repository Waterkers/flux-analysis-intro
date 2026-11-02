function setLanguage(lang)
% setLanguage('en') or setLanguage('de'): language of everything the helpers print.
%   setLanguage('de') oder setLanguage('en'): Sprache aller Ausgaben der Hilfsfunktionen.
  global PRACTICAL_LANGUAGE
  if ~any(strcmp(lang, {'en', 'de'}))
    error(tr('unknownLang', lang));
  end
  PRACTICAL_LANGUAGE = lang;
  fprintf(tr('langSet'));
end
