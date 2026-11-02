"""Patch the COBRA Toolbox so the functions used in the practical run under Octave.

Each patch replaces one exact line; the build fails if a line is not found, so a
new COBRA release can't silently skip a fix.
"""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])

PATCHES = [
    # Octave pads char matrices with NUL instead of spaces; cellstr() keeps the NULs
    # and the later eval() of the field table fails.
    ("descFileRead.m",
     "raw = struct(data{:});",
     "for k = 2:2:numel(data), data{k}(data{k} == 0) = ' '; end\n"
     "raw = struct(data{:});"),
    # Octave's glpk() returns an error code as 3rd output and the LP status in extra.status.
    ("solveCobraLP.m",
     "[x,f,origStat,extra] = glpk(c,A,b,lb,ub,csense,[],osense,params);",
     "[x,f,origStat,extra] = glpk(c,A,b,lb,ub,csense,[],osense,params);\n"
     "if exist('OCTAVE_VERSION', 'builtin') && origStat == 0 && isfield(extra, 'status')\n"
     "    origStat = extra.status;\n"
     "end"),
    # Octave's regexprep() has no ${expression} replacements.
    ("parseGPR.m",
     "ruleString = regexprep(grRuleString, '([^\\(\\)\\|\\&\\s]+)', '${convertGenes($0)}');",
     "ruleString = regexprepfun(grRuleString, '([^\\(\\)\\|\\&\\s]+)', @(t) convertGenes(t{1}));"),
    ("creategrRulesField.m",
     "currentrules = regexprep(currentrules,'x\\(([0-9]+)\\)','${model.genes{str2num($1)}}');",
     "currentrules = regexprepfun(currentrules,'x\\(([0-9]+)\\)',@(t) model.genes{str2num(t{2})});"),
    ("printRxnFormula.m",
     "rule = regexprep(rule,'x\\((?<id>[0-9]+)\\)','${model.genes{num2str($1)}}');",
     "rule = regexprepfun(rule,'x\\(([0-9]+)\\)',@(t) model.genes{str2num(t{2})});"),
    ("printGPRForRxns.m",
     "gprs = regexprep(gprs,'x\\(([0-9]+)\\)','${model.genes{str2num($1)}}');",
     "gprs = regexprepfun(gprs,'x\\(([0-9]+)\\)',@(t) model.genes{str2num(t{2})});"),
]

failed = False
for rel, old, new in PATCHES:  # rel is a file name, searched for under src/
    found = list((ROOT / "src").rglob(rel))
    if len(found) != 1:
        print(f"PATCH FAILED: expected one {rel} under src/, found {len(found)}")
        failed = True
        continue
    path = found[0]
    text = path.read_text(encoding="utf-8", errors="surrogateescape")
    lines = text.split("\n")
    hits = [i for i, line in enumerate(lines) if line.strip() == old]
    if len(hits) != 1:
        print(f"PATCH FAILED: {rel}: expected 1 match, found {len(hits)}: {old}")
        failed = True
        continue
    i = hits[0]
    indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
    lines[i] = "\n".join(indent + part for part in new.split("\n"))
    path.write_text("\n".join(lines), encoding="utf-8", errors="surrogateescape")
    print(f"patched {rel}")

sys.exit(1 if failed else 0)
