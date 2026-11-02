function showExchange(model, solution)
% showExchange(model, solution)  What do the cells take up, and what do they release?
%   Was nehmen die Zellen auf, und was geben sie ab?
  ex = find(strncmp(model.rxns, 'EX_', 3));
  flux = solution.x(ex);
  names = cell(size(ex));
  for k = 1:numel(ex)
    names{k} = exchangeNames(model.rxns{ex(k)}, currentLanguage());
  end
  printList(tr('takesUp'), names, -flux, flux < -1e-6);
  printList(tr('releases'), names, flux, flux > 1e-6);
end

function printList(title, names, amount, keep)
  disp(title);
  idx = find(keep);
  [~, order] = sort(amount(idx), 'descend');
  idx = idx(order);
  if isempty(idx)
    disp(tr('none'));
  end
  for k = idx'
    % pad by characters, not bytes, so umlauts don't shift the columns
    % (UTF-8 continuation bytes are 10xxxxxx)
    bytes = double(names{k});
    width = sum(bytes < 128 | bytes >= 192);
    fprintf('  %s%s %8.2f\n', names{k}, blanks(max(28 - width, 1)), amount(k));
  end
end
