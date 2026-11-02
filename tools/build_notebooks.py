"""Build the practical's notebooks from this one source file.

Each notebook is written four times:
    practical/en/<name>.ipynb          student version, English
    practical/de/<name>.ipynb          student version, German
    teacher/solutions/en/<name>.ipynb  with solutions, English
    teacher/solutions/de/<name>.ipynb  with solutions, German

Change the text here and run `python3 tools/build_notebooks.py` from the project
folder, then `python3 tools/check_parity.py`. Writing both languages side by side
keeps the code in the English and German versions identical.

Cell types:
    md(en, de)                   explanation
    code(en, de)                 code cell; the two versions may differ only in comments and text
    exercise(student, solution)  code cell with blanks (___) for students, filled in for teachers;
                                 each argument is an (en, de) pair
    answer(en, de)               answer box: empty for students, model answer for teachers
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def md(en, de):
    return {"kind": "md", "en": en, "de": de}


def code(en, de=None):
    return {"kind": "code", "en": en, "de": en if de is None else de}


def exercise(student, solution):
    return {"kind": "exercise", "student": student, "solution": solution}


def answer(en, de):
    return {"kind": "answer", "en": en, "de": de}


ANSWER_PROMPT = {
    "en": "✏️ **Your answer:** *(double-click here to type)*\n\n",
    "de": "✏️ **Deine Antwort:** *(Doppelklick hier, um zu schreiben)*\n\n",
}
ANSWER_LABEL = {"en": "✅ **Answer:** ", "de": "✅ **Antwort:** "}

LANGUAGE_CELL = code(
    "setLanguage('en')   % language of the messages below",
    "setLanguage('de')   % Sprache der Ausgaben",
)

SOURCES = md(
    """## Sources

* **Model:** the *E. coli* core model (`e_coli_core`) from BiGG Models. Orth JD, Fleming RMT, Palsson BØ (2010). Reconstruction and use of microbial metabolic networks: the core *Escherichia coli* metabolic model as an educational guide. *EcoSal Plus* 4(1). [doi:10.1128/ecosalplus.10.2.1](https://doi.org/10.1128/ecosalplus.10.2.1)
* **Database:** King ZA et al. (2016). BiGG Models: A platform for integrating, standardizing and sharing genome-scale models. *Nucleic Acids Research* 44(D1):D515–D522. [doi:10.1093/nar/gkv1049](https://doi.org/10.1093/nar/gkv1049). BiGG Models © 2019 The Regents of the University of California; free for educational, research and non-profit use.
* **Software:** COBRA Toolbox v3.7.1. Heirendt L et al. (2019). Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0. *Nature Protocols* 14:639–702. [doi:10.1038/s41596-018-0098-2](https://doi.org/10.1038/s41596-018-0098-2). It runs in [GNU Octave](https://octave.org) with the [GLPK](https://www.gnu.org/software/glpk/) solver.
* **Method:** Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28:245–248. [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614)""",
    """## Quellen

* **Modell:** das *E.-coli*-Kernmodell (`e_coli_core`) aus BiGG Models. Orth JD, Fleming RMT, Palsson BØ (2010). Reconstruction and use of microbial metabolic networks: the core *Escherichia coli* metabolic model as an educational guide. *EcoSal Plus* 4(1). [doi:10.1128/ecosalplus.10.2.1](https://doi.org/10.1128/ecosalplus.10.2.1)
* **Datenbank:** King ZA et al. (2016). BiGG Models: A platform for integrating, standardizing and sharing genome-scale models. *Nucleic Acids Research* 44(D1):D515–D522. [doi:10.1093/nar/gkv1049](https://doi.org/10.1093/nar/gkv1049). BiGG Models © 2019 The Regents of the University of California; frei für Bildung, Forschung und gemeinnützige Zwecke.
* **Software:** COBRA Toolbox v3.7.1. Heirendt L et al. (2019). Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0. *Nature Protocols* 14:639–702. [doi:10.1038/s41596-018-0098-2](https://doi.org/10.1038/s41596-018-0098-2). Sie läuft in [GNU Octave](https://octave.org) mit dem Solver [GLPK](https://www.gnu.org/software/glpk/).
* **Methode:** Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28:245–248. [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614)""",
)

SOURCES_SHORT = md(
    """<small>Model: *E. coli* core model from BiGG Models (Orth et al. 2010; King et al. 2016). Software: COBRA Toolbox (Heirendt et al. 2019) in GNU Octave. Full sources at the end of `01_tutorial_fba.ipynb`.</small>""",
    """<small>Modell: *E.-coli*-Kernmodell aus BiGG Models (Orth et al. 2010; King et al. 2016). Software: COBRA Toolbox (Heirendt et al. 2019) in GNU Octave. Vollständige Quellen am Ende von `01_tutorial_fba.ipynb`.</small>""",
)

# ---------------------------------------------------------------------------
# 00 Welcome
# ---------------------------------------------------------------------------
WELCOME = [
    md(
        """# Welcome to bioinformatics! 🧬💻

**Bioinformatics** is where biology meets computers. Bioinformaticians write programs to answer biological questions, for example:

* reading and comparing **DNA** (where did the coronavirus come from?),
* predicting the 3D shape of **proteins** (and designing medicines that fit them),
* simulating the **metabolism** of a cell (how does a bacterium turn sugar into new bacteria?).

Today you'll try the third one. You'll use a computer model of the gut bacterium ***Escherichia coli*** (*E. coli*) and predict how fast it grows, what it eats, and which of its genes it can't live without.

But first: how does this page work?""",
        """# Willkommen in der Bioinformatik! 🧬💻

In der **Bioinformatik** treffen sich Biologie und Informatik. Bioinformatikerinnen und Bioinformatiker schreiben Programme, die biologische Fragen beantworten, zum Beispiel:

* **DNA** lesen und vergleichen (woher kommt das Coronavirus?),
* die 3D-Form von **Proteinen** vorhersagen (und Medikamente entwerfen, die genau hineinpassen),
* den **Stoffwechsel** einer Zelle simulieren (wie macht ein Bakterium aus Zucker neue Bakterien?).

Heute probierst du das Dritte aus. Du arbeitest mit einem Computermodell des Darmbakteriums ***Escherichia coli*** (*E. coli*) und sagst vorher, wie schnell es wächst, was es frisst und auf welche seiner Gene es nicht verzichten kann.

Aber zuerst: Wie funktioniert diese Seite?""",
    ),
    md(
        """## How to use a notebook

This page is a **notebook**. It mixes text (like this) with **code cells** (the grey boxes).

To run a code cell: click on it and press **Shift + Enter**. The result appears below the cell.

Try it with the cell below:""",
        """## So benutzt du ein Notebook

Diese Seite ist ein **Notebook**. Es mischt Text (so wie diesen) mit **Code-Zellen** (den grauen Kästen).

So führst du eine Code-Zelle aus: Klicke hinein und drücke **Umschalt + Enter**. Das Ergebnis erscheint unter der Zelle.

Probiere es mit der Zelle hier unten aus:""",
    ),
    code("1 + 1"),
    md(
        """The computer can remember values under a name. That's called a **variable**. Run the cell, then change the number 7 to something else and run it again.""",
        """Der Computer kann sich Werte unter einem Namen merken. Das nennt man eine **Variable**. Führe die Zelle aus, ändere dann die Zahl 7 und führe sie noch einmal aus.""",
    ),
    code(
        "x = 7\ndouble_x = 2 * x",
    ),
    md(
        """## Your first exercise: bacteria multiply fast

A bacterium divides into two every **20 minutes**. After 20 minutes you have 2, after 40 minutes 4, after 60 minutes 8, ...

How many bacteria are there after **3 hours**, if you start with one?

Replace the `___` with the right numbers and run the cell. *Tip: `2^3` means 2 × 2 × 2.*""",
        """## Deine erste Aufgabe: Bakterien vermehren sich schnell

Ein Bakterium teilt sich alle **20 Minuten** in zwei. Nach 20 Minuten hast du 2, nach 40 Minuten 4, nach 60 Minuten 8, ...

Wie viele Bakterien sind es nach **3 Stunden**, wenn du mit einem anfängst?

Ersetze die `___` durch die richtigen Zahlen und führe die Zelle aus. *Tipp: `2^3` bedeutet 2 × 2 × 2.*""",
    ),
    exercise(
        (
            "minutes = ___                 % 3 hours in minutes\ndivisions = minutes / ___      % how often does it divide?\nbacteria = 2 ^ divisions",
            "minutes = ___                 % 3 Stunden in Minuten\ndivisions = minutes / ___      % wie oft teilt es sich?\nbacteria = 2 ^ divisions",
        ),
        (
            "minutes = 180                 % 3 hours in minutes\ndivisions = minutes / 20       % how often does it divide?\nbacteria = 2 ^ divisions",
            "minutes = 180                 % 3 Stunden in Minuten\ndivisions = minutes / 20       % wie oft teilt es sich?\nbacteria = 2 ^ divisions",
        ),
    ),
    md(
        """How long would it take to reach as many bacteria as there are people on Earth (about 8 billion = `8e9`)? Try a few numbers of hours in the cell above.""",
        """Wie lange würde es dauern, bis es so viele Bakterien wie Menschen auf der Erde gibt (etwa 8 Milliarden = `8e9`)? Probiere in der Zelle oben ein paar Stundenzahlen aus.""",
    ),
    answer(
        "After 3 hours (9 divisions) there are 2⁹ = **512** bacteria. 8 billion is reached after about 33 divisions, so **11 hours**. In reality, bacteria run out of food long before that, and how fast they grow depends on the food. That's what the next notebook is about.",
        "Nach 3 Stunden (9 Teilungen) sind es 2⁹ = **512** Bakterien. 8 Milliarden sind nach etwa 33 Teilungen erreicht, also nach **11 Stunden**. In Wirklichkeit geht den Bakterien lange vorher das Futter aus, und wie schnell sie wachsen, hängt vom Futter ab. Darum geht es im nächsten Notebook.",
    ),
    md(
        """**Well done!** Now open `01_tutorial_fba.ipynb` in the file list on the left.""",
        """**Gut gemacht!** Öffne jetzt `01_tutorial_fba.ipynb` in der Dateiliste links.""",
    ),
]

# ---------------------------------------------------------------------------
# 01 Tutorial
# ---------------------------------------------------------------------------
TUTORIAL = [
    md(
        """# A bacterium in the computer

## What is metabolism?

Every cell is a tiny chemical factory. It takes in food (for example sugar) and, step by step, turns it into energy and into the building blocks of a new cell. Each step is a **chemical reaction**, and each reaction is carried out by an **enzyme**. The instructions for building each enzyme are in a **gene**.

```mermaid
flowchart LR
    A[Food<br>glucose, oxygen, ...] --> B[Reactions<br>made possible by enzymes]
    B --> C[Building blocks<br>amino acids, DNA, fats, ...]
    C --> D[New cell]
    B --> E[Waste<br>CO2, water, ...]
```

Scientists have collected all known reactions of *E. coli* into a **metabolic model**. Today we use a small version of it, the *E. coli* **core model** from the [BiGG database](http://bigg.ucsd.edu/models/e_coli_core).

First run the cell below; it sets the language of the messages. Then load the model.""",
        """# Ein Bakterium im Computer

## Was ist Stoffwechsel?

Jede Zelle ist eine winzige chemische Fabrik. Sie nimmt Nahrung auf (zum Beispiel Zucker) und verwandelt sie Schritt für Schritt in Energie und in die Bausteine einer neuen Zelle. Jeder Schritt ist eine **chemische Reaktion**, und jede Reaktion wird von einem **Enzym** durchgeführt. Die Bauanleitung für jedes Enzym steht in einem **Gen**.

```mermaid
flowchart LR
    A[Nahrung<br>Glukose, Sauerstoff, ...] --> B[Reaktionen<br>durch Enzyme ermöglicht]
    B --> C[Bausteine<br>Aminosäuren, DNA, Fette, ...]
    C --> D[Neue Zelle]
    B --> E[Abfall<br>CO2, Wasser, ...]
```

Forschende haben alle bekannten Reaktionen von *E. coli* in einem **Stoffwechselmodell** gesammelt. Heute benutzen wir eine kleine Version davon, das ***E.-coli*-Kernmodell** (*core model*) aus der [BiGG-Datenbank](http://bigg.ucsd.edu/models/e_coli_core).

Führe zuerst die Zelle unten aus; sie stellt die Sprache der Ausgaben ein. Dann lade das Modell.""",
    ),
    LANGUAGE_CELL,
    code("model = loadEcoli();"),
    md(
        """## A look inside the model

Each reaction has a short ID and a full name. Here are the first ten:""",
        """## Ein Blick ins Modell

Jede Reaktion hat eine kurze ID und einen vollen Namen (auf Englisch). Hier sind die ersten zehn:""",
    ),
    code("[model.rxns(1:10), model.rxnNames(1:10)]"),
    md(
        """Let's look at one reaction more closely: **PGK** (phosphoglycerate kinase). It is one of the steps that break down sugar and produce energy in the form of **ATP**, the cell's "battery".

The output shows the reaction formula and, at the end, the **gene** that codes for its enzyme.""",
        """Schauen wir uns eine Reaktion genauer an: **PGK** (Phosphoglyceratkinase). Sie ist einer der Schritte, die Zucker abbauen und dabei Energie in Form von **ATP** herstellen, der „Batterie“ der Zelle.

Die Ausgabe zeigt die Reaktionsgleichung und ganz am Ende das **Gen**, das für ihr Enzym codiert.""",
    ),
    code("printRxnFormula(model, 'rxnAbbrList', 'PGK', 'gprFlag', true);"),
    md(
        """`3pg_c + atp_c <=> 13dpg_c + adp_c` means: 3-phosphoglycerate and ATP react to 1,3-bisphosphoglycerate and ADP. The `_c` means "in the cytoplasm", the inside of the cell. `_e` would mean "outside the cell". `<=>` means the reaction can run in both directions.

`b2926` is the gene's ID. Its name is *pgk*.""",
        """`3pg_c + atp_c <=> 13dpg_c + adp_c` bedeutet: 3-Phosphoglycerat und ATP reagieren zu 1,3-Bisphosphoglycerat und ADP. Das `_c` bedeutet „im Cytoplasma“, also im Inneren der Zelle. `_e` würde „außerhalb der Zelle“ bedeuten. `<=>` heißt, dass die Reaktion in beide Richtungen laufen kann.

`b2926` ist die ID des Gens. Sein Name ist *pgk*.""",
    ),
    md(
        """## How the computer predicts growth: flux balance analysis

Imagine the model as a road network: the reactions are roads, and the molecules are the traffic. The amount of traffic on each road is called a **flux**. The computer has to find out how much traffic flows on each road. It uses three rules:

1. **Nothing piles up.** Everything that is made inside the cell is used up again, like a bathtub with the tap and drain open where the water level stays the same.
2. **Limits.** The cell can only take up a limited amount of food per hour. In our model: at most 10 units of glucose (sugar).
3. **A goal.** We assume the bacterium wants to **grow as fast as possible**. Evolution has made bacteria very good at that.

There is a special reaction that stands for "build a new cell": the **biomass reaction**, `BIOMASS_Ecoli_core_w_GAM`. It's a recipe listing all the building blocks a new cell needs. The computer searches for the fluxes that make this reaction as fast as possible.

This method is called **flux balance analysis (FBA)**. The search uses a mathematical technique called *linear programming*. Let's run it:""",
        """## Wie der Computer Wachstum vorhersagt: Flussbilanzanalyse

Stell dir das Modell wie ein Straßennetz vor: Die Reaktionen sind Straßen, und die Moleküle sind der Verkehr. Wie viel Verkehr über eine Straße fließt, nennt man **Fluss**. Der Computer muss herausfinden, wie viel Verkehr über jede Straße fließt. Dafür hat er drei Regeln:

1. **Nichts staut sich.** Alles, was in der Zelle hergestellt wird, wird auch wieder verbraucht, wie bei einer Badewanne mit offenem Hahn und offenem Abfluss, in der der Wasserstand gleich bleibt.
2. **Grenzen.** Die Zelle kann pro Stunde nur eine begrenzte Menge Nahrung aufnehmen. In unserem Modell: höchstens 10 Einheiten Glukose (Zucker).
3. **Ein Ziel.** Wir nehmen an, dass das Bakterium **so schnell wie möglich wachsen** will. Die Evolution hat Bakterien darin sehr gut gemacht.

Es gibt eine besondere Reaktion, die für „baue eine neue Zelle“ steht: die **Biomasse-Reaktion** `BIOMASS_Ecoli_core_w_GAM`. Sie ist ein Rezept mit allen Bausteinen, die eine neue Zelle braucht. Der Computer sucht die Flüsse, mit denen diese Reaktion so schnell wie möglich läuft.

Diese Methode heißt **Flussbilanzanalyse** (*flux balance analysis*, **FBA**). Für die Suche wird ein mathematisches Verfahren namens *lineare Optimierung* benutzt. Probieren wir es aus:""",
    ),
    code("[growth, solution] = showGrowth(model);"),
    md(
        """The model predicts that *E. coli* doubles about every **48 minutes** on glucose with plenty of oxygen. In the lab, *E. coli* doubles every 20 to 60 minutes depending on the conditions, so the prediction is in the right range. The computer worked that out from nothing but the list of reactions!

## What goes in, what comes out?""",
        """Das Modell sagt vorher, dass sich *E. coli* mit Glukose und genug Sauerstoff etwa alle **48 Minuten** verdoppelt. Im Labor verdoppelt sich *E. coli* je nach Bedingungen alle 20 bis 60 Minuten, die Vorhersage liegt also im richtigen Bereich. Der Computer hat das nur aus der Liste der Reaktionen berechnet!

## Was geht hinein, was kommt heraus?""",
    ),
    code("showExchange(model, solution)"),
    md(
        """The numbers are in mmol per gram of bacteria per hour.

**Question 1:** What does *E. coli* take up, and what does it release? Compare that with what *you* breathe in and out.""",
        """Die Zahlen sind in mmol pro Gramm Bakterien pro Stunde.

**Frage 1:** Was nimmt *E. coli* auf, und was gibt es ab? Vergleiche das mit dem, was *du* ein- und ausatmest.""",
    ),
    answer(
        "It takes up glucose (sugar), oxygen, ammonium (a source of nitrogen) and phosphate. It releases carbon dioxide, water and H⁺. Just like us, it \"burns\" sugar with oxygen and breathes out CO₂ and water. Nitrogen and phosphate are needed to build proteins and DNA.",
        "Es nimmt Glukose (Zucker), Sauerstoff, Ammonium (eine Stickstoffquelle) und Phosphat auf. Es gibt Kohlendioxid, Wasser und H⁺ ab. Genau wie wir „verbrennt“ es Zucker mit Sauerstoff und atmet CO₂ und Wasser aus. Stickstoff und Phosphat braucht es, um Proteine und DNA zu bauen.",
    ),
    md(
        """## The busiest reactions

Which reactions carry the most traffic? Positive numbers mean the reaction runs forwards, negative numbers mean it runs backwards.""",
        """## Die aktivsten Reaktionen

Über welche Reaktionen fließt am meisten Verkehr? Positive Zahlen heißen, die Reaktion läuft vorwärts, negative Zahlen, sie läuft rückwärts.""",
    ),
    code("showFluxes(model, solution, 15)"),
    md(
        """**Question 2:** Look at the names in the list under the chart. Several of the busiest reactions have to do with ATP (`ATPS4r` = ATP synthase) and with breathing (`CYTBD` = cytochrome oxidase, `NADH16` = NADH dehydrogenase). Why do you think the cell spends so much effort on these?""",
        """**Frage 2:** Schau dir die Namen in der Liste unter dem Diagramm an. Mehrere der aktivsten Reaktionen haben mit ATP (`ATPS4r` = ATP-Synthase) und mit der Atmung zu tun (`CYTBD` = Cytochrom-Oxidase, `NADH16` = NADH-Dehydrogenase). Warum steckt die Zelle wohl so viel Aufwand in diese Reaktionen?""",
    ),
    answer(
        "Building a new cell costs a lot of energy. These reactions form the **respiratory chain**, which uses oxygen to make most of the cell's ATP. ATP is the energy currency that powers almost every other reaction.",
        "Eine neue Zelle zu bauen kostet sehr viel Energie. Diese Reaktionen bilden die **Atmungskette**, die mit Sauerstoff den größten Teil des ATP der Zelle herstellt. ATP ist die Energiewährung, mit der fast alle anderen Reaktionen angetrieben werden.",
    ),
    md(
        """## Summary

* A **metabolic model** lists all reactions of a cell, with the genes behind them.
* **Flux balance analysis** finds the fluxes that let the cell grow fastest, without anything piling up and without eating more than allowed.
* From that, the computer predicts the **growth rate** and what the cell **takes up and releases**.

In the exercises you'll change the conditions and see how the bacterium reacts. Start with `02_exercise_oxygen.ipynb`.""",
        """## Zusammenfassung

* Ein **Stoffwechselmodell** listet alle Reaktionen einer Zelle auf, zusammen mit den Genen dahinter.
* Die **Flussbilanzanalyse** findet die Flüsse, mit denen die Zelle am schnellsten wächst, ohne dass sich etwas staut und ohne dass sie mehr frisst als erlaubt.
* Daraus sagt der Computer die **Wachstumsrate** vorher und was die Zelle **aufnimmt und abgibt**.

In den Aufgaben änderst du die Bedingungen und schaust, wie das Bakterium reagiert. Fang mit `02_exercise_oxygen.ipynb` an.""",
    ),
]

# ---------------------------------------------------------------------------
# 02 Oxygen
# ---------------------------------------------------------------------------
OXYGEN = [
    md(
        """# Exercise: life without oxygen

*E. coli* lives in our gut, where there is hardly any oxygen. Can it grow there? And what changes?

Run the first two cells to set up.""",
        """# Aufgabe: Leben ohne Sauerstoff

*E. coli* lebt in unserem Darm, wo es kaum Sauerstoff gibt. Kann es dort wachsen? Und was ändert sich?

Führe die ersten beiden Zellen aus, um alles vorzubereiten.""",
    ),
    LANGUAGE_CELL,
    code("model = loadEcoli();"),
    md(
        """## With oxygen

`setMedium(model, glucose, oxygen)` sets how much glucose and oxygen the cells may take up at most. 1000 means "as much as they want".""",
        """## Mit Sauerstoff

`setMedium(model, glucose, oxygen)` legt fest, wie viel Glukose und Sauerstoff die Zellen höchstens aufnehmen dürfen. 1000 bedeutet „so viel sie wollen“.""",
    ),
    code(
        "model_air = setMedium(model, 10, 1000);\n[growth_air, solution_air] = showGrowth(model_air);",
    ),
    md(
        """## Without oxygen

Now take the oxygen away. Replace `___` with the right number.""",
        """## Ohne Sauerstoff

Jetzt nimm den Sauerstoff weg. Ersetze `___` durch die richtige Zahl.""",
    ),
    exercise(
        (
            "model_no_air = setMedium(model, 10, ___);\n[growth_no_air, solution_no_air] = showGrowth(model_no_air);",
            "model_no_air = setMedium(model, 10, ___);\n[growth_no_air, solution_no_air] = showGrowth(model_no_air);",
        ),
        (
            "model_no_air = setMedium(model, 10, 0);\n[growth_no_air, solution_no_air] = showGrowth(model_no_air);",
            "model_no_air = setMedium(model, 10, 0);\n[growth_no_air, solution_no_air] = showGrowth(model_no_air);",
        ),
    ),
    md(
        """**Question 1:** Can *E. coli* grow without oxygen? How many times slower is it? *(Tip: you can calculate in a code cell, e.g. `growth_air / growth_no_air`.)*""",
        """**Frage 1:** Kann *E. coli* ohne Sauerstoff wachsen? Wie viel Mal langsamer ist es? *(Tipp: Du kannst in einer Code-Zelle rechnen, z. B. `growth_air / growth_no_air`.)*""",
    ),
    code(
        "growth_air / growth_no_air",
    ),
    answer(
        "Yes, it still grows, but about **4 times slower**: 0.212 instead of 0.874 per hour. It doubles every 196 minutes instead of every 48 minutes.",
        "Ja, es wächst noch, aber etwa **4-mal langsamer**: 0,212 statt 0,874 pro Stunde. Es verdoppelt sich alle 196 Minuten statt alle 48 Minuten.",
    ),
    md(
        """## What comes out without oxygen?""",
        """## Was kommt ohne Sauerstoff heraus?""",
    ),
    code("showExchange(model_no_air, solution_no_air)"),
    md(
        """**Question 2:** Which substances does *E. coli* release now that it didn't release with oxygen? Do you know any of them from everyday life?""",
        """**Frage 2:** Welche Stoffe gibt *E. coli* jetzt ab, die es mit Sauerstoff nicht abgegeben hat? Kennst du einige davon aus dem Alltag?""",
    ),
    answer(
        "**Formate** (formic acid, known from ant stings), **acetate** (the acid in vinegar) and **ethanol** (the alcohol in beer and wine). This is called **fermentation**. Yeast does the same to make bread rise and to brew beer, and your muscles make lactic acid when they run out of oxygen.",
        "**Formiat** (Ameisensäure, bekannt von Ameisenbissen), **Acetat** (die Säure im Essig) und **Ethanol** (der Alkohol in Bier und Wein). Das nennt man **Gärung** (Fermentation). Hefe macht das Gleiche, wenn Brotteig aufgeht und wenn Bier gebraut wird, und deine Muskeln bilden Milchsäure, wenn ihnen der Sauerstoff ausgeht.",
    ),
    md(
        """**Why?** With oxygen, the cell can "burn" glucose completely to CO₂ and get a lot of energy (ATP) from it. Without oxygen it can only break glucose down halfway. It gets much less energy, and the half-used molecules are released as waste. Less energy means slower growth.

## How much oxygen is enough?

The cell below calculates the growth rate for many different amounts of oxygen and draws a graph. Just run it.""",
        """**Warum?** Mit Sauerstoff kann die Zelle Glukose vollständig zu CO₂ „verbrennen“ und bekommt dabei viel Energie (ATP). Ohne Sauerstoff kann sie Glukose nur zur Hälfte abbauen. Sie bekommt viel weniger Energie, und die halb genutzten Moleküle werden als Abfall abgegeben. Weniger Energie heißt langsameres Wachstum.

## Wie viel Sauerstoff ist genug?

Die Zelle unten berechnet die Wachstumsrate für viele verschiedene Sauerstoffmengen und zeichnet ein Diagramm. Führe sie einfach aus.""",
    ),
    code(
        """oxygen = 0:2:30;                      % 0, 2, 4, ... 30
growth = zeros(size(oxygen));
for i = 1:numel(oxygen)
  m = changeRxnBounds(model, 'EX_o2_e', -oxygen(i), 'l');   % allow this much oxygen
  s = optimizeCbModel(m);                                     % run FBA
  growth(i) = s.f;                                            % remember the growth rate
end
plot(oxygen, growth, 'o-', 'linewidth', 2)
xlabel('Oxygen uptake (mmol per gram per hour)')
ylabel('Growth rate (per hour)')
grid on""",
        """oxygen = 0:2:30;                      % 0, 2, 4, ... 30
growth = zeros(size(oxygen));
for i = 1:numel(oxygen)
  m = changeRxnBounds(model, 'EX_o2_e', -oxygen(i), 'l');   % so viel Sauerstoff erlauben
  s = optimizeCbModel(m);                                     % FBA ausführen
  growth(i) = s.f;                                            % Wachstumsrate merken
end
plot(oxygen, growth, 'o-', 'linewidth', 2)
xlabel('Sauerstoff-Aufnahme (mmol pro Gramm pro Stunde)')
ylabel('Wachstumsrate (pro Stunde)')
grid on""",
    ),
    md(
        """**Question 3:** Describe the graph. From what amount of oxygen does extra oxygen stop helping? Why does the line become flat?""",
        """**Frage 3:** Beschreibe das Diagramm. Ab welcher Sauerstoffmenge hilft mehr Sauerstoff nicht mehr? Warum wird die Linie flach?""",
    ),
    answer(
        "Growth rises steadily with oxygen and becomes flat at about **22** units. From there on, glucose is the limit: the cell already burns all 10 units of sugar it can take up, and extra oxygen has nothing left to burn.",
        "Das Wachstum steigt mit dem Sauerstoff gleichmäßig an und wird bei etwa **22** Einheiten flach. Ab dann ist die Glukose die Grenze: Die Zelle verbrennt schon alle 10 Einheiten Zucker, die sie aufnehmen kann, und für mehr Sauerstoff gibt es nichts mehr zu verbrennen.",
    ),
    md(
        """**Done!** Continue with `03_exercise_food.ipynb`.""",
        """**Fertig!** Weiter geht es mit `03_exercise_food.ipynb`.""",
    ),
]

# ---------------------------------------------------------------------------
# 03 Food
# ---------------------------------------------------------------------------
FOOD = [
    md(
        """# Exercise: what's on the menu?

In this exercise you'll find out how the amount and the type of food change how fast *E. coli* grows.""",
        """# Aufgabe: Was steht auf dem Speiseplan?

In dieser Aufgabe findest du heraus, wie Menge und Art der Nahrung beeinflussen, wie schnell *E. coli* wächst.""",
    ),
    LANGUAGE_CELL,
    code("model = loadEcoli();"),
    md(
        """## More sugar, faster growth?

Each food has an **exchange reaction** whose ID starts with `EX_`. Glucose is `EX_glc__D_e`. With `changeRxnBounds` you set how much of it the cell may take up. The amount is negative, because taking up means the substance *leaves* the surroundings.

The cell below tries glucose amounts from 0 to 20. Run it.""",
        """## Mehr Zucker, schnelleres Wachstum?

Jede Nahrung hat eine **Austauschreaktion** (*exchange reaction*), deren ID mit `EX_` beginnt. Glukose ist `EX_glc__D_e`. Mit `changeRxnBounds` legst du fest, wie viel davon die Zelle aufnehmen darf. Die Menge ist negativ, denn Aufnehmen heißt, dass der Stoff die Umgebung *verlässt*.

Die Zelle unten probiert Glukosemengen von 0 bis 20 aus. Führe sie aus.""",
    ),
    code(
        """glucose = 0:1:20;
growth = zeros(size(glucose));
for i = 1:numel(glucose)
  m = changeRxnBounds(model, 'EX_glc__D_e', -glucose(i), 'l');   % allow this much glucose
  s = optimizeCbModel(m);
  growth(i) = s.f;
end
plot(glucose, growth, 'o-', 'linewidth', 2)
xlabel('Glucose uptake (mmol per gram per hour)')
ylabel('Growth rate (per hour)')
grid on""",
        """glucose = 0:1:20;
growth = zeros(size(glucose));
for i = 1:numel(glucose)
  m = changeRxnBounds(model, 'EX_glc__D_e', -glucose(i), 'l');   % so viel Glukose erlauben
  s = optimizeCbModel(m);
  growth(i) = s.f;
end
plot(glucose, growth, 'o-', 'linewidth', 2)
xlabel('Glukose-Aufnahme (mmol pro Gramm pro Stunde)')
ylabel('Wachstumsrate (pro Stunde)')
grid on""",
    ),
    md(
        """**Question 1:** What shape does the line have? What happens to the growth rate if you double the glucose?""",
        """**Frage 1:** Welche Form hat die Linie? Was passiert mit der Wachstumsrate, wenn du die Glukose verdoppelst?""",
    ),
    answer(
        "A **straight line**: double the glucose gives double the growth (5 → 0.42, 10 → 0.87, 20 → 1.79 per hour). With very little glucose (below about half a unit) there is no growth, because the cell first needs energy just to stay alive (*maintenance*). With no glucose at all the model finds no solution, so the point at 0 is missing. In a real cell the line would level off, because the transporters that bring sugar into the cell can only work so fast.",
        "Eine **gerade Linie**: doppelt so viel Glukose ergibt doppelt so viel Wachstum (5 → 0,42, 10 → 0,87, 20 → 1,79 pro Stunde). Mit sehr wenig Glukose (unter etwa einer halben Einheit) gibt es kein Wachstum, weil die Zelle zuerst Energie braucht, nur um am Leben zu bleiben (*Erhaltungsstoffwechsel*). Ganz ohne Glukose findet das Modell keine Lösung, darum fehlt der Punkt bei 0. In einer echten Zelle würde die Linie irgendwann flach werden, weil die Transporter, die Zucker in die Zelle bringen, nur begrenzt schnell arbeiten.",
    ),
    md(
        """## Other foods

*E. coli* can also live on other foods. In the cell below, glucose is switched off (0) and the cell gets 10 units of **acetate** (`EX_ac_e`) instead.""",
        """## Andere Nahrung

*E. coli* kann auch von anderer Nahrung leben. In der Zelle unten wird die Glukose abgeschaltet (0), und die Zelle bekommt stattdessen 10 Einheiten **Acetat** (`EX_ac_e`).""",
    ),
    code(
        """m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');   % no glucose
m = changeRxnBounds(m, 'EX_ac_e', -10, 'l');          % 10 units of acetate
showGrowth(m);""",
        """m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');   % keine Glukose
m = changeRxnBounds(m, 'EX_ac_e', -10, 'l');          % 10 Einheiten Acetat
showGrowth(m);""",
    ),
    md(
        """Now it's your turn. Try **fructose** (fruit sugar, `EX_fru_e`) and **succinate** (`EX_succ_e`). Replace `___` with the ID of the food.

| Food | ID | Growth rate (per hour) |
|---|---|---|
| glucose | `EX_glc__D_e` | 0.874 |
| acetate | `EX_ac_e` | |
| fructose | `EX_fru_e` | |
| succinate | `EX_succ_e` | |

*Double-click the table to fill in your results.*""",
        """Jetzt bist du dran. Probiere **Fruktose** (Fruchtzucker, `EX_fru_e`) und **Succinat** (`EX_succ_e`) aus. Ersetze `___` durch die ID der Nahrung.

| Nahrung | ID | Wachstumsrate (pro Stunde) |
|---|---|---|
| Glukose | `EX_glc__D_e` | 0,874 |
| Acetat | `EX_ac_e` | |
| Fruktose | `EX_fru_e` | |
| Succinat | `EX_succ_e` | |

*Doppelklicke auf die Tabelle, um deine Ergebnisse einzutragen.*""",
    ),
    exercise(
        (
            """m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');   % no glucose
m = changeRxnBounds(m, '___', -10, 'l');              % 10 units of another food
showGrowth(m);""",
            """m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');   % keine Glukose
m = changeRxnBounds(m, '___', -10, 'l');              % 10 Einheiten einer anderen Nahrung
showGrowth(m);""",
        ),
        (
            """m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');   % no glucose
m = changeRxnBounds(m, 'EX_fru_e', -10, 'l');         % 10 units of another food
showGrowth(m);
m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');
m = changeRxnBounds(m, 'EX_succ_e', -10, 'l');
showGrowth(m);""",
            """m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');   % keine Glukose
m = changeRxnBounds(m, 'EX_fru_e', -10, 'l');         % 10 Einheiten einer anderen Nahrung
showGrowth(m);
m = changeRxnBounds(model, 'EX_glc__D_e', 0, 'l');
m = changeRxnBounds(m, 'EX_succ_e', -10, 'l');
showGrowth(m);""",
        ),
    ),
    md(
        """**Question 2:** Which food is best for *E. coli*, and which is worst? Glucose and fructose have **6** carbon atoms per molecule, succinate has **4** and acetate only **2**. Can you explain the results with that?""",
        """**Frage 2:** Welche Nahrung ist für *E. coli* am besten, welche am schlechtesten? Glukose und Fruktose haben **6** Kohlenstoffatome pro Molekül, Succinat hat **4** und Acetat nur **2**. Kannst du die Ergebnisse damit erklären?""",
    ),
    answer(
        "Glucose and fructose: 0.874, succinate: 0.398, acetate: 0.173 per hour. Glucose and fructose are equally good. The cell gets the same amount of material and energy from them, because fructose is converted into the same intermediate products. The fewer carbon atoms a molecule has, the less building material and energy the cell gets from each molecule, so it grows more slowly.",
        "Glukose und Fruktose: 0,874, Succinat: 0,398, Acetat: 0,173 pro Stunde. Glukose und Fruktose sind gleich gut. Die Zelle bekommt aus beiden gleich viel Material und Energie, weil Fruktose in dieselben Zwischenprodukte umgewandelt wird. Je weniger Kohlenstoffatome ein Molekül hat, desto weniger Baumaterial und Energie bekommt die Zelle aus jedem Molekül, also wächst sie langsamer.",
    ),
    md(
        """**Extra:** Can *E. coli* live on acetate **without oxygen**? Try it with `setMedium(m, 0, 0)` after giving it acetate.""",
        """**Extra:** Kann *E. coli* **ohne Sauerstoff** von Acetat leben? Probiere es mit `setMedium(m, 0, 0)` aus, nachdem du ihm Acetat gegeben hast.""",
    ),
    exercise(
        (
            """m = changeRxnBounds(model, 'EX_ac_e', -10, 'l');
m = setMedium(m, 0, 0);   % no glucose, no oxygen
showGrowth(m);""",
            """m = changeRxnBounds(model, 'EX_ac_e', -10, 'l');
m = setMedium(m, 0, 0);   % keine Glukose, kein Sauerstoff
showGrowth(m);""",
        ),
        (
            """m = changeRxnBounds(model, 'EX_ac_e', -10, 'l');
m = setMedium(m, 0, 0);   % no glucose, no oxygen
showGrowth(m);""",
            """m = changeRxnBounds(model, 'EX_ac_e', -10, 'l');
m = setMedium(m, 0, 0);   % keine Glukose, kein Sauerstoff
showGrowth(m);""",
        ),
    ),
    answer(
        "No. Acetate is itself a waste product of fermentation, so there's no energy left to get from it without oxygen. The model finds no solution at all, because the cell can't even make the energy it needs to stay alive.",
        "Nein. Acetat ist selbst schon ein Abfallprodukt der Gärung, ohne Sauerstoff ist daraus keine Energie mehr zu holen. Das Modell findet überhaupt keine Lösung, weil die Zelle nicht einmal die Energie herstellen kann, die sie zum Überleben braucht.",
    ),
    md(
        """**Done!** Continue with `04_exercise_knockouts.ipynb`.""",
        """**Fertig!** Weiter geht es mit `04_exercise_knockouts.ipynb`.""",
    ),
]

# ---------------------------------------------------------------------------
# 04 Knockouts
# ---------------------------------------------------------------------------
KNOCKOUTS = [
    md(
        """# Exercise: switching off genes

Each enzyme is built from the instructions in a gene. If a gene is broken or removed (a **knockout**), its enzyme is missing, and the reaction it carries out can't happen anymore.

That's how many **antibiotics** work: they block an enzyme that the bacterium can't live without. In this exercise you'll use the model to look for such weak spots.""",
        """# Aufgabe: Gene ausschalten

Jedes Enzym wird nach der Bauanleitung in einem Gen gebaut. Ist ein Gen kaputt oder entfernt (ein **Knockout**), fehlt sein Enzym, und die Reaktion, die es durchführt, kann nicht mehr stattfinden.

So wirken viele **Antibiotika**: Sie blockieren ein Enzym, ohne das das Bakterium nicht leben kann. In dieser Aufgabe suchst du mit dem Modell nach solchen Schwachstellen.""",
    ),
    LANGUAGE_CELL,
    code("model = loadEcoli();\nshowGrowth(model);"),
    md(
        """## A first knockout

The gene *pfkB* codes for an enzyme in the breakdown of sugar. What happens if you switch it off?""",
        """## Ein erster Knockout

Das Gen *pfkB* codiert ein Enzym für den Abbau von Zucker. Was passiert, wenn du es ausschaltest?""",
    ),
    code("m = knockOut(model, 'pfkB');\nshowGrowth(m);"),
    md(
        """Nothing happens! *E. coli* has a second gene, *pfkA*, that codes for an enzyme doing the same job. Cells often have such **backups**.

Now switch off the gene ***eno*** (enolase), which codes for another step in the breakdown of sugar. Replace `___`.""",
        """Nichts passiert! *E. coli* hat ein zweites Gen, *pfkA*, das ein Enzym für dieselbe Aufgabe codiert. Zellen haben oft solche **Reservekopien**.

Schalte jetzt das Gen ***eno*** (Enolase) aus, das einen anderen Schritt im Zuckerabbau codiert. Ersetze `___`.""",
    ),
    exercise(
        (
            "m = knockOut(model, '___');\nshowGrowth(m);",
            "m = knockOut(model, '___');\nshowGrowth(m);",
        ),
        (
            "m = knockOut(model, 'eno');\nshowGrowth(m);",
            "m = knockOut(model, 'eno');\nshowGrowth(m);",
        ),
    ),
    md(
        """**Question 1:** What happens without *eno*? What does that mean for the bacterium?""",
        """**Frage 1:** Was passiert ohne *eno*? Was bedeutet das für das Bakterium?""",
    ),
    answer(
        "The bacterium **cannot grow** at all. There is no backup for enolase, and no detour around this step. A gene like this is called **essential**.",
        "Das Bakterium **kann gar nicht mehr wachsen**. Für die Enolase gibt es keine Reservekopie und keinen Umweg um diesen Schritt herum. So ein Gen nennt man **essenziell**.",
    ),
    md(
        """## Testing all genes

Testing 137 genes by hand would take a while. `findEssentialGenes` switches off every gene, one at a time, and lists the ones the bacterium can't grow without.""",
        """## Alle Gene testen

137 Gene von Hand zu testen würde dauern. `findEssentialGenes` schaltet jedes Gen einzeln aus und listet die auf, ohne die das Bakterium nicht wachsen kann.""",
    ),
    code("essential_glucose = findEssentialGenes(model);"),
    md(
        """**Question 2:** How many of the 137 genes are essential? Why do you think so few genes are essential?""",
        """**Frage 2:** Wie viele der 137 Gene sind essenziell? Warum sind wohl so wenige Gene essenziell?""",
    ),
    answer(
        "Only **7** (gltA, eno, ptsI, ptsH, gapA, icd, pgk). The metabolic network has many backup genes and detours. If one road is closed, the traffic can usually take another route. That makes bacteria robust, and it's why good antibiotic targets are rare.",
        "Nur **7** (gltA, eno, ptsI, ptsH, gapA, icd, pgk). Das Stoffwechselnetz hat viele Reservegene und Umwege. Wenn eine Straße gesperrt ist, kann der Verkehr meist eine andere Route nehmen. Das macht Bakterien robust, und darum sind gute Angriffspunkte für Antibiotika selten.",
    ),
    md(
        """## Does it depend on the conditions?

In the gut there is hardly any oxygen. Find the essential genes **without oxygen**. Replace `___` so that the cells get 10 units of glucose but no oxygen.""",
        """## Hängt das von den Bedingungen ab?

Im Darm gibt es kaum Sauerstoff. Finde die essenziellen Gene **ohne Sauerstoff**. Ersetze `___` so, dass die Zellen 10 Einheiten Glukose, aber keinen Sauerstoff bekommen.""",
    ),
    exercise(
        (
            "model_gut = setMedium(model, ___, ___);\nessential_gut = findEssentialGenes(model_gut);",
            "model_gut = setMedium(model, ___, ___);\nessential_gut = findEssentialGenes(model_gut);",
        ),
        (
            "model_gut = setMedium(model, 10, 0);\nessential_gut = findEssentialGenes(model_gut);",
            "model_gut = setMedium(model, 10, 0);\nessential_gut = findEssentialGenes(model_gut);",
        ),
    ),
    md(
        """**Question 3:** Which genes are essential only without oxygen?

*Tip: `setdiff(essential_gut, essential_glucose)` lists the genes that are in the first list but not in the second. Try it in the cell below.*""",
        """**Frage 3:** Welche Gene sind nur ohne Sauerstoff essenziell?

*Tipp: `setdiff(essential_gut, essential_glucose)` listet die Gene, die in der ersten Liste stehen, aber nicht in der zweiten. Probiere es in der Zelle unten aus.*""",
    ),
    code("setdiff(essential_gut, essential_glucose)"),
    answer(
        "**pgi, ppc and tpiA**. Without oxygen the cell has fewer ways to make energy, so some of its detours disappear and more genes become essential. Which genes a bacterium needs depends on where it lives!",
        "**pgi, ppc und tpiA**. Ohne Sauerstoff hat die Zelle weniger Möglichkeiten, Energie zu gewinnen, also fallen einige Umwege weg, und mehr Gene werden essenziell. Welche Gene ein Bakterium braucht, hängt davon ab, wo es lebt!",
    ),
    md(
        """## Think like a drug designer

**Question 4:** Enolase (*eno*) is essential for *E. coli*. But human cells use enolase too, to break down sugar. Would a medicine that blocks enolase be a good antibiotic? What makes a good antibiotic target?""",
        """## Denk wie eine Medikamenten-Entwicklerin

**Frage 4:** Enolase (*eno*) ist für *E. coli* essenziell. Aber auch menschliche Zellen benutzen Enolase, um Zucker abzubauen. Wäre ein Medikament, das Enolase blockiert, ein gutes Antibiotikum? Was macht einen guten Angriffspunkt für ein Antibiotikum aus?""",
    ),
    answer(
        "Probably not: it could harm our own cells too. A good target is (1) **essential** for the bacterium under the conditions where it causes disease, and (2) **absent or very different in humans**. Examples are the enzymes that build the bacterial cell wall, which our cells don't have (penicillin blocks them). Bioinformaticians compare bacterial and human genes to find such targets.",
        "Wahrscheinlich nicht: Es könnte auch unseren eigenen Zellen schaden. Ein guter Angriffspunkt ist (1) für das Bakterium **essenziell**, und zwar unter den Bedingungen, unter denen es krank macht, und (2) **beim Menschen nicht vorhanden oder ganz anders gebaut**. Beispiele sind die Enzyme, die die Zellwand der Bakterien bauen, die unsere Zellen nicht haben (Penicillin blockiert sie). Bioinformatikerinnen und Bioinformatiker vergleichen bakterielle und menschliche Gene, um solche Angriffspunkte zu finden.",
    ),
    md(
        """**Done!** If you have time left, try the bonus: `05_bonus_production.ipynb`.""",
        """**Fertig!** Wenn du noch Zeit hast, probiere den Bonus aus: `05_bonus_production.ipynb`.""",
    ),
]

# ---------------------------------------------------------------------------
# 05 Bonus: production
# ---------------------------------------------------------------------------
PRODUCTION = [
    md(
        """# Bonus: bacteria as factories

Bacteria can be used to make useful substances: medicines like insulin, plastics, or fuels like **bioethanol**. Bioinformaticians use models like ours to plan which genes to change so that the bacterium makes as much product as possible.

Until now the goal was "grow as fast as possible". You can give the model a different goal: "make as much ethanol as possible".""",
        """# Bonus: Bakterien als Fabriken

Mit Bakterien kann man nützliche Stoffe herstellen: Medikamente wie Insulin, Kunststoffe oder Treibstoffe wie **Bioethanol**. Bioinformatikerinnen und Bioinformatiker planen mit Modellen wie unserem, welche Gene man verändern muss, damit das Bakterium so viel Produkt wie möglich herstellt.

Bisher war das Ziel „so schnell wie möglich wachsen“. Du kannst dem Modell aber auch ein anderes Ziel geben: „so viel Ethanol wie möglich herstellen“.""",
    ),
    LANGUAGE_CELL,
    code("model = loadEcoli();\nmodel = setMedium(model, 10, 0);   % 10 glucose, no oxygen", "model = loadEcoli();\nmodel = setMedium(model, 10, 0);   % 10 Glukose, kein Sauerstoff"),
    md(
        """`changeObjective` changes the goal. `EX_etoh_e` is the reaction that releases ethanol.""",
        """`changeObjective` ändert das Ziel. `EX_etoh_e` ist die Reaktion, die Ethanol abgibt.""",
    ),
    code(
        """m = changeObjective(model, 'EX_etoh_e');      % new goal: release as much ethanol as possible
s = optimizeCbModel(m, 'max');
biomass = s.x(strcmp(m.rxns, 'BIOMASS_Ecoli_core_w_GAM'));
fprintf('Ethanol: %.1f, growth: %.3f per hour\\n', s.f, biomass)""",
        """m = changeObjective(model, 'EX_etoh_e');      % neues Ziel: so viel Ethanol wie möglich abgeben
s = optimizeCbModel(m, 'max');
biomass = s.x(strcmp(m.rxns, 'BIOMASS_Ecoli_core_w_GAM'));
fprintf('Ethanol: %.1f, Wachstum: %.3f pro Stunde\\n', s.f, biomass)""",
    ),
    md(
        """**Question 1:** From 10 glucose the cell makes 20 ethanol: 2 ethanol per glucose, the chemical maximum. But how fast does the bacterium grow now? Is that a problem for a factory?""",
        """**Frage 1:** Aus 10 Glukose macht die Zelle 20 Ethanol: 2 Ethanol pro Glukose, das chemische Maximum. Aber wie schnell wächst das Bakterium jetzt? Ist das ein Problem für eine Fabrik?""",
    ),
    answer(
        "It doesn't grow at all (0 per hour). All the sugar goes into ethanol, and nothing is left for new cells. A factory needs bacteria that also grow, otherwise there are soon no workers left.",
        "Es wächst gar nicht (0 pro Stunde). Der ganze Zucker geht in Ethanol, für neue Zellen bleibt nichts übrig. Eine Fabrik braucht Bakterien, die auch wachsen, sonst gibt es bald keine Arbeiter mehr.",
    ),
    md(
        """## Growth or product? A trade-off

The cell below forces the bacterium to grow at a certain minimum rate, and then asks how much ethanol it can still make. Run it.""",
        """## Wachstum oder Produkt? Ein Kompromiss

Die Zelle unten zwingt das Bakterium, mindestens mit einer bestimmten Rate zu wachsen, und fragt dann, wie viel Ethanol es noch herstellen kann. Führe sie aus.""",
    ),
    code(
        """growth = linspace(0, 0.21, 15);                 % from no growth up to the maximum without oxygen
ethanol = zeros(size(growth));
for i = 1:numel(growth)
  m = changeRxnBounds(model, 'BIOMASS_Ecoli_core_w_GAM', growth(i), 'l');   % grow at least this fast
  m = changeObjective(m, 'EX_etoh_e');
  s = optimizeCbModel(m, 'max');
  ethanol(i) = s.f;
end
plot(growth, ethanol, 'o-', 'linewidth', 2)
xlabel('Growth rate (per hour)')
ylabel('Maximum ethanol (mmol per gram per hour)')
ylim([0 22])   % fixed axis, so every computer shows the same picture
grid on""",
        """growth = linspace(0, 0.21, 15);                 % von keinem Wachstum bis zum Maximum ohne Sauerstoff
ethanol = zeros(size(growth));
for i = 1:numel(growth)
  m = changeRxnBounds(model, 'BIOMASS_Ecoli_core_w_GAM', growth(i), 'l');   % mindestens so schnell wachsen
  m = changeObjective(m, 'EX_etoh_e');
  s = optimizeCbModel(m, 'max');
  ethanol(i) = s.f;
end
plot(growth, ethanol, 'o-', 'linewidth', 2)
xlabel('Wachstumsrate (pro Stunde)')
ylabel('Maximales Ethanol (mmol pro Gramm pro Stunde)')
ylim([0 22])   % feste Achse, damit jeder Computer dasselbe Bild zeigt
grid on""",
    ),
    md(
        """**Question 2:** Describe the trade-off. If you ran a bioethanol company, which point on the line would you choose, and why?""",
        """**Frage 2:** Beschreibe den Kompromiss. Wenn du eine Bioethanol-Firma hättest, welchen Punkt auf der Linie würdest du wählen, und warum?""",
    ),
    answer(
        "The faster the bacteria grow, the less ethanol they make. Up to a growth rate of about 0.18 per hour this costs only a little ethanol (20 → 17); after that, ethanol drops steeply to about 9 at maximum growth. Many would choose the \"corner\" at about 0.18: the bacteria still grow well and make almost as much ethanol as possible. There is no single right answer, though. A common strategy is to first let the bacteria grow fast (to get many workers), then switch them to production. Researchers also look for gene knockouts that force the cell to make ethanol *while* it grows.",
        "Je schneller die Bakterien wachsen, desto weniger Ethanol stellen sie her. Bis zu einer Wachstumsrate von etwa 0,18 pro Stunde kostet das nur wenig Ethanol (20 → 17); danach fällt das Ethanol steil auf etwa 9 bei maximalem Wachstum. Viele würden die „Ecke“ bei etwa 0,18 wählen: Die Bakterien wachsen noch gut und stellen fast so viel Ethanol wie möglich her. Eine einzige richtige Antwort gibt es aber nicht. Eine übliche Strategie ist, die Bakterien zuerst schnell wachsen zu lassen (um viele Arbeiter zu bekommen) und sie dann auf Produktion umzuschalten. Forschende suchen auch nach Gen-Knockouts, die die Zelle zwingen, *während* des Wachstums Ethanol herzustellen.",
    ),
    md(
        """## Your own product

**Succinate** (`EX_succ_e`) is used to make plastics and medicines. How much succinate can *E. coli* make at most from 10 glucose, without oxygen and with oxygen? Replace the `___`.""",
        """## Dein eigenes Produkt

**Succinat** (`EX_succ_e`) wird zur Herstellung von Kunststoffen und Medikamenten verwendet. Wie viel Succinat kann *E. coli* aus 10 Glukose höchstens herstellen, ohne Sauerstoff und mit Sauerstoff? Ersetze die `___`.""",
    ),
    exercise(
        (
            """m = changeObjective(setMedium(model, 10, ___), '___');
s = optimizeCbModel(m, 'max');
fprintf('%.1f\\n', s.f)""",
            """m = changeObjective(setMedium(model, 10, ___), '___');
s = optimizeCbModel(m, 'max');
fprintf('%.1f\\n', s.f)""",
        ),
        (
            """m = changeObjective(setMedium(model, 10, 0), 'EX_succ_e');
s = optimizeCbModel(m, 'max');
fprintf('%.1f\\n', s.f)
m = changeObjective(setMedium(model, 10, 1000), 'EX_succ_e');
s = optimizeCbModel(m, 'max');
fprintf('%.1f\\n', s.f)""",
            """m = changeObjective(setMedium(model, 10, 0), 'EX_succ_e');
s = optimizeCbModel(m, 'max');
fprintf('%.1f\\n', s.f)
m = changeObjective(setMedium(model, 10, 1000), 'EX_succ_e');
s = optimizeCbModel(m, 'max');
fprintf('%.1f\\n', s.f)""",
        ),
    ),
    answer(
        "About **13.9** without oxygen and **16.4** with oxygen. Unlike ethanol, here oxygen helps: making succinate needs extra energy and carbon dioxide, which the cell gets more easily by breathing.",
        "Etwa **13,9** ohne Sauerstoff und **16,4** mit Sauerstoff. Anders als beim Ethanol hilft hier der Sauerstoff: Für Succinat braucht die Zelle zusätzliche Energie und Kohlendioxid, die sie durch Atmung leichter bekommt.",
    ),
    md(
        """**Congratulations!** 🎉 You've used the same methods that researchers use to study bacteria, find targets for new antibiotics and design bacterial factories. That's bioinformatics!""",
        """**Herzlichen Glückwunsch!** 🎉 Du hast dieselben Methoden benutzt, mit denen Forschende Bakterien untersuchen, Angriffspunkte für neue Antibiotika finden und Bakterien-Fabriken planen. Das ist Bioinformatik!""",
    ),
]

NOTEBOOKS = {
    "00_welcome": WELCOME,
    "01_tutorial_fba": TUTORIAL + [SOURCES],
    "02_exercise_oxygen": OXYGEN + [SOURCES_SHORT],
    "03_exercise_food": FOOD + [SOURCES_SHORT],
    "04_exercise_knockouts": KNOCKOUTS + [SOURCES_SHORT],
    "05_bonus_production": PRODUCTION + [SOURCES_SHORT],
}


def to_cells(spec, lang, solutions):
    cells = []
    for item in spec:
        kind = item["kind"]
        if kind == "md":
            cells.append(("markdown", item[lang]))
        elif kind == "code":
            cells.append(("code", item[lang]))
        elif kind == "exercise":
            pair = item["solution"] if solutions else item["student"]
            cells.append(("code", pair[0] if lang == "en" else pair[1]))
        elif kind == "answer":
            if solutions:
                cells.append(("markdown", ANSWER_LABEL[lang] + item[lang]))
            else:
                cells.append(("markdown", ANSWER_PROMPT[lang]))
    return cells


def notebook(cells):
    nb_cells = []
    for i, (cell_type, source) in enumerate(cells):
        cell = {"cell_type": cell_type, "id": f"cell-{i:02d}", "metadata": {}, "source": source}
        if cell_type == "code":
            cell["execution_count"] = None
            cell["outputs"] = []
        nb_cells.append(cell)
    return {
        "cells": nb_cells,
        "metadata": {
            "kernelspec": {"display_name": "Octave", "language": "octave", "name": "octave"},
            "language_info": {"name": "octave", "file_extension": ".m", "mimetype": "text/x-octave"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main():
    targets = {
        False: ROOT / "practical",
        True: ROOT / "teacher" / "solutions",
    }
    for solutions, base in targets.items():
        for lang in ("en", "de"):
            out_dir = base / lang
            out_dir.mkdir(parents=True, exist_ok=True)
            for name, spec in NOTEBOOKS.items():
                path = out_dir / f"{name}.ipynb"
                nb = notebook(to_cells(spec, lang, solutions))
                path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
                print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
