"""Write gene and metabolite names from BiGG's JSON model to a tab-separated file.

The BiGG .mat file has no gene names, but names like 'eno' or 'pgk' are what
students can look up, so loadEcoli() adds them from this file.
"""
import csv
import json
import sys

model = json.load(open(sys.argv[1], encoding="utf-8"))
with open(sys.argv[2], "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out, delimiter="\t", lineterminator="\n")
    writer.writerow(["type", "id", "name"])
    for gene in model["genes"]:
        writer.writerow(["gene", gene["id"], gene.get("name") or gene["id"]])
