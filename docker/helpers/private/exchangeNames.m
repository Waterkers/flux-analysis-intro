function name = exchangeNames(rxnId, lang)
% Everyday name of the substance moved by an exchange reaction (EX_...), in English or German.
  table = {
    'EX_ac_e',     'acetate (vinegar acid)',  'Acetat (Essigsäure)'
    'EX_acald_e',  'acetaldehyde',            'Acetaldehyd'
    'EX_akg_e',    '2-oxoglutarate',          '2-Oxoglutarat'
    'EX_co2_e',    'carbon dioxide (CO2)',    'Kohlendioxid (CO2)'
    'EX_etoh_e',   'ethanol (alcohol)',       'Ethanol (Alkohol)'
    'EX_for_e',    'formate',                 'Formiat (Ameisensäure)'
    'EX_fru_e',    'fructose (sugar)',        'Fruktose (Zucker)'
    'EX_fum_e',    'fumarate',                'Fumarat'
    'EX_glc__D_e', 'glucose (sugar)',         'Glukose (Zucker)'
    'EX_gln__L_e', 'glutamine',               'Glutamin'
    'EX_glu__L_e', 'glutamate',               'Glutamat'
    'EX_h_e',      'H+ (acidity)',            'H+ (Säure)'
    'EX_h2o_e',    'water',                   'Wasser'
    'EX_lac__D_e', 'lactate (lactic acid)',   'Laktat (Milchsäure)'
    'EX_mal__L_e', 'malate',                  'Malat'
    'EX_nh4_e',    'ammonium (nitrogen)',     'Ammonium (Stickstoff)'
    'EX_o2_e',     'oxygen (O2)',             'Sauerstoff (O2)'
    'EX_pi_e',     'phosphate',               'Phosphat'
    'EX_pyr_e',    'pyruvate',                'Pyruvat'
    'EX_succ_e',   'succinate',               'Succinat (Bernsteinsäure)'
  };
  row = find(strcmp(table(:, 1), rxnId), 1);
  if isempty(row)
    name = rxnId;
  elseif strcmp(lang, 'de')
    name = table{row, 3};
  else
    name = table{row, 2};
  end
end
