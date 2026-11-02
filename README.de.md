[English](README.md) | **Deutsch**

# FBA-Praktikum: Anleitung für Lehrkräfte

Eine fertige Umgebung für ein kurzes Schulpraktikum zur **Flussbilanzanalyse (FBA)**, als Einblick in die Bioinformatik. Die Schülerinnen und Schüler arbeiten in **JupyterLab im Browser**. Dahinter läuft ein Docker-Container mit **GNU Octave**, dem Solver **GLPK**, der **COBRA Toolbox** und dem ***E.-coli*-Kernmodell** aus [BiGG](http://bigg.ucsd.edu/models/e_coli_core). Alles gibt es auf **Englisch und Deutsch**.

Für die Notebooks 00–04 brauchen die Schülerinnen und Schüler etwa 45–60 Minuten; Notebook 05 ist ein Bonus.

## Was in diesem Ordner liegt

| Pfad | Was es ist | An Schüler weitergeben? |
|---|---|---|
| `practical/en/`, `practical/de/` | die Notebooks, in denen gearbeitet wird; werden in den Container eingebunden | ja |
| `practical/README*.md` | kurze Anleitung für Schüler | ja |
| `start.*`, `stop.*`, `docker-compose.yml`, `docker/` | Starten und Beenden, Definition des Images | ja |
| `teacher/solutions/{en,de}/` | dieselben Notebooks mit Lösungen und Ausgaben | **nein** |
| `tools/` | Notebook-Generator, Prüfungen, Paket-Skript | nein |

## Vor dem Praktikum

### 1. Image bauen

Du brauchst Docker (unter Windows/Mac Docker Desktop). In diesem Ordner:

```bash
docker compose build
```

Das dauert ein paar Minuten. Dabei werden Octave, die COBRA Toolbox und das Modell heruntergeladen, und anschließend läuft ein **Smoke-Test**. Der Build schlägt fehl, wenn die FBA nicht die bekannten Ergebnisse liefert (Wachstum 0,874 h⁻¹ mit Sauerstoff, 0,212 h⁻¹ ohne, 7 essenzielle Gene). Das Image heißt `fba-practical:1.0`.

### 2. Das Image auf die Schülerrechner bringen

Wähle eine Möglichkeit:

**a) USB-Stick / Netzlaufwerk** (funktioniert ohne gutes Internet):

```bash
tools/make_student_package.sh --with-image
```

Das erzeugt `dist/fba-practical-students.zip` und `dist/fba-practical-image.tar.gz` (etwa 1 GB). Auf jedem Schülerrechner das Zip entpacken und das Image einmal laden:

```bash
docker load -i fba-practical-image.tar.gz
```

**b) Eine Container-Registry** (z. B. GitHub Container Registry), damit die Schülerrechner das Image direkt herunterladen. Für Intel/AMD- und Apple-Silicon-Rechner bauen und hochladen:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/DEIN-KONTO/fba-practical:1.0 --push docker
```

Dann `.env.example` nach `.env` kopieren, dort `FBA_IMAGE=ghcr.io/DEIN-KONTO/fba-practical:1.0` eintragen und `tools/make_student_package.sh` ausführen (ohne `--with-image`). Das Skript legt deine `.env` mit ins Zip, damit die Schüler dieselbe Einstellung bekommen. (`.env` selbst wird nicht ins Repository übernommen.) Die Schülerrechner führen einmal `docker compose pull` aus, oder das Startskript lädt das Image beim ersten Start.

> Das in Schritt 1 gebaute Image läuft nur auf Rechnern mit demselben Prozessortyp wie deiner. Für eine Klasse mit Windows-PCs und Macs mit Apple Silicon nimm den `buildx`-Befehl oben. Auf einem Linux-Rechner braucht der Build für `arm64` QEMU-Emulation: `docker run --privileged --rm tonistiigi/binfmt --install arm64`.

### 3. Einmal ausprobieren

```bash
./start.sh de    # Deutsch
./start.sh       # English
```

Geh dann die Notebooks selbst durch. Die Lösungen in `teacher/solutions/` zeigen die erwartete Ausgabe jeder Zelle.

## Während des Praktikums

* **Windows:** Doppelklick auf `start_de.bat` (Deutsch) oder `start.bat` (English).
* **Mac:** Doppelklick auf `start_de.command` oder `start.command`. macOS blockiert jede dieser Dateien beim ersten Mal, weil sie aus dem Internet heruntergeladen wurden. Rechtsklick → *Öffnen* funktioniert in aktuellen macOS-Versionen **nicht**. Stattdessen:
  1. Doppelklick auf die Datei. macOS meldet, dass sie nicht geöffnet werden kann; auf **Fertig** klicken.
  2.  → **Systemeinstellungen → Datenschutz & Sicherheit** öffnen, nach unten zu *Sicherheit* scrollen und neben der Datei auf **Dennoch öffnen** klicken.
  3. Mit dem Passwort des Macs (oder Touch ID) bestätigen und noch einmal auf **Dennoch öffnen** klicken.
  4. Wenn gefragt wird, ob Terminal auf Dateien im Ordner *Downloads* zugreifen darf, auf **Erlauben** klicken.

  Das ist einmal pro Datei nötig, also einmal für `start_de.command` und einmal für `start.command`. Auf Macs, die von der Schule verwaltet werden, muss das eventuell die IT erlauben. Probiere es vor dem Praktikumstag an einem Schüler-Mac aus.
* **Linux:** `./start.sh de` oder `./start.sh`.

Der Browser öffnet `http://localhost:8888` im Ordner der gewählten Sprache. Auch die Menüs von JupyterLab sind dann in dieser Sprache. Zum Beenden: `stop.bat` / `./stop.sh`. Die Arbeit der Schülerinnen und Schüler bleibt in `practical/` auf ihrem Rechner.

JupyterLab ist nur vom Rechner selbst aus erreichbar (`127.0.0.1`), darum läuft es ohne Passwort.

## Notebooks ändern

Die Notebooks werden aus **`tools/build_notebooks.py`** erzeugt. Jede Zelle steht dort auf Englisch und Deutsch nebeneinander, und jede Aufgabe hat eine Schüler- und eine Lösungsfassung. Nach dem Bearbeiten:

```bash
python3 tools/build_notebooks.py     # schreibt practical/ und teacher/solutions/
python3 tools/check_parity.py        # en und de müssen denselben Code ausführen
tools/run_solutions.sh               # führt alle Lösungs-Notebooks aus, damit sie wieder Ausgaben enthalten
```

Wenn du die Notebooks stattdessen direkt in JupyterLab bearbeitest, führe danach `check_parity.py` aus. Es meldet jedes englisch-deutsche Paar, dessen Code auseinandergelaufen ist. Kommentare und Text in Anführungszeichen dürfen sich unterscheiden, alles andere muss übereinstimmen.

`build_notebooks.py` überschreibt `practical/`, also führe es nicht auf einem Rechner aus, auf dem Schüler schon gearbeitet haben.

## Funktionen für die Schüler

Der Container bringt ein paar kleine Funktionen mit, damit die Notebooks kurz bleiben. Sie sind dünne Hüllen um Funktionen der COBRA Toolbox und liegen in `docker/helpers/`:

| Funktion | Was sie tut |
|---|---|
| `setLanguage('en'/'de')` | Sprache aller folgenden Ausgaben |
| `model = loadEcoli()` | lädt das Modell (mit Gennamen wie *eno* für `b2779`) |
| `model = setMedium(model, glucose, oxygen)` | maximale Aufnahme von Glukose und Sauerstoff |
| `[growth, sol] = showGrowth(model)` | FBA; zeigt Wachstumsrate und Verdopplungszeit |
| `showExchange(model, sol)` | was die Zellen aufnehmen und abgeben, mit Alltagsnamen |
| `showFluxes(model, sol, n)` | Balkendiagramm der *n* größten Flüsse |
| `model = knockOut(model, 'eno')` | schaltet ein Gen aus, über Namen oder ID |
| `genes = findEssentialGenes(model)` | Einzel-Gen-Deletion: die Gene, ohne die die Zellen nicht wachsen |

Die Schüler benutzen außerdem direkt die COBRA-Funktionen `changeRxnBounds`, `changeObjective`, `optimizeCbModel` und `printRxnFormula`. Alle Texte der Hilfsfunktionen stehen in `docker/helpers/private/messages.m` und `exchangeNames.m`.

## So funktioniert der Container

* **Basis:** `quay.io/jupyter/minimal-notebook:2026-10-12` (Ubuntu 26.04, JupyterLab 4.6), dazu Octave 11 aus Ubuntu, `octave_kernel` und das deutsche JupyterLab-Sprachpaket. Das Paket lässt einige Menüpunkte auf Englisch (z. B. im Menü *Ausführen*); `docker/jupyterlab-de-additions.json` ergänzt beim Build deutsche Übersetzungen dafür und korrigiert zwei Tippfehler. Weitere Menüpunkte lassen sich dort ergänzen.
* **Solver:** GLPK, in Octave als `glpk()` eingebaut. Keine Lizenz nötig. Für das Modell mit 95 Reaktionen mehr als schnell genug.
* **COBRA Toolbox v3.7.1** in `/opt/cobratoolbox`, schreibgeschützt. `initCobraToolbox` wird **nicht** benutzt: Unter Octave verlangt es Git-Submodule und ruft Funktionen auf, die es nur in MATLAB gibt. Stattdessen setzt `docker/cobra_startup.m` `src/` auf den Pfad und setzt die Solver-Variablen, die `initCobraToolbox` setzen würde. Das läuft über die systemweite `octaverc` automatisch in jeder Octave-Sitzung.
* **Anpassungen für Octave:** `docker/patch_cobra.py` ändert beim Build sechs Zeilen der COBRA Toolbox. Sie betreffen:
  * mit NUL aufgefüllten Text in `descFileRead`
  * das Auslesen des GLPK-Status aus Octaves `glpk()`
  * `regexprep` mit `${…}`-Ausdrücken, die Octave nicht kennt (vier Stellen)

  `docker/compat/` ergänzt `contains()` und die Hilfsfunktion `regexprepfun()`, die diese Anpassungen benutzen. Der Build schlägt fehl, wenn eine angepasste Zeile in einer neueren COBRA-Version woanders steht.
* **Modell:** `e_coli_core.mat` und `e_coli_core.json` aus BiGG, geprüft gegen feste SHA-256-Prüfsummen. Die JSON-Datei liefert nur die Gennamen.
* **Unter Octave nicht getestet:** COBRA-Funktionen, die die Notebooks nicht benutzen. `fluxVariability` und `surfNet` funktionieren bekanntermaßen nicht.

## Wenn etwas nicht klappt

| Problem | Lösung |
|---|---|
| „Docker läuft nicht“ | Docker Desktop starten und warten, bis es läuft. |
| Windows: Docker Desktop verlangt WSL 2 | Den Anweisungen folgen und WSL 2 installieren (braucht einmal Administratorrechte). |
| Port 8888 ist schon belegt | Ein anderes Jupyter läuft. Beenden, oder `127.0.0.1:8888` in `docker-compose.yml` und in den Startskripten ändern. |
| `pull access denied for fba-practical` | Das Image ist nicht auf diesem Rechner: `docker load -i fba-practical-image.tar.gz`, oder `FBA_IMAGE` in `.env` eintragen (aus `.env.example` kopieren). |
| Image startet nicht auf einem Mac mit M-Chip: `exec format error` | Das Image wurde nur für Intel gebaut; mit `buildx` für beide Plattformen bauen (siehe Schritt 2b). |
| Linux: Dateien in `practical/` gehören einem anderen Benutzer | Mit `./start.sh` starten, das deine Benutzer-ID an den Container weitergibt. |
| Protokoll | `docker compose logs` |

## Quellen und Lizenzen

Dieses Praktikum baut auf der Arbeit anderer auf:

* **Modell:** das *E.-coli*-Kernmodell, Orth JD, Fleming RMT, Palsson BØ (2010), *EcoSal Plus* 4(1), [doi:10.1128/ecosalplus.10.2.1](https://doi.org/10.1128/ecosalplus.10.2.1).
* **Datenbank:** [BiGG Models](http://bigg.ucsd.edu), King ZA et al. (2016), *Nucleic Acids Research* 44(D1):D515–D522, [doi:10.1093/nar/gkv1049](https://doi.org/10.1093/nar/gkv1049).
* **Software:** [COBRA Toolbox](https://github.com/opencobra/cobratoolbox) v3.7.1, Heirendt L et al. (2019), *Nature Protocols* 14:639–702, [doi:10.1038/s41596-018-0098-2](https://doi.org/10.1038/s41596-018-0098-2); [GNU Octave](https://octave.org) mit dem Solver [GLPK](https://www.gnu.org/software/glpk/); [Jupyter](https://jupyter.org) und [`octave_kernel`](https://github.com/Calysto/octave_kernel).
* **Methode:** Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis? *Nature Biotechnology* 28:245–248, [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614).

Nichts davon liegt in diesem Repository; es wird beim Bauen des Images heruntergeladen. Die Lizenzen stehen in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) (auf Englisch).

**Hinweis zur Lizenz des Modells:** BiGG Models ist nur für Bildung, Forschung und gemeinnützige Zwecke frei. Ein gebautes Image enthält das Modell, also nutze oder verbreite das Image nicht kommerziell ohne Erlaubnis der UC San Diego. Der Lizenztext von BiGG liegt im Image unter `/opt/models/LICENSE-BiGG.txt`.

## Lizenz

Dieses Repository verwendet zwei Lizenzen:

| Was | Lizenz |
|---|---|
| Notebooks (`practical/`, `teacher/`), die Notebook-Texte in `tools/build_notebooks.py` und die Dokumentation (README-Dateien, `THIRD_PARTY_NOTICES.md`) | [CC BY 4.0](LICENSE-CC-BY-4.0.txt) |
| Alles andere: Code, Skripte, Docker- und Octave-Dateien | [MIT](LICENSE) |

Ausnahmen: `docker/LICENSE-BiGG.txt` ist der Lizenztext von BiGG, und `docker/patch_cobra.py` zitiert die sechs Zeilen der COBRA Toolbox, die es ändert (COBRA Toolbox: GPL-3.0). Software und Daten Dritter, die das Image nutzt, behalten ihre eigenen Lizenzen, siehe [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Du darfst die Notebooks gern für deinen eigenen Unterricht übersetzen, kürzen oder anpassen. Nach CC BY 4.0 nenne bitte die Quelle, zum Beispiel so: *„Nach dem FBA-Praktikum der fba-practical contributors, CC BY 4.0“*, mit einem Link zu diesem Repository.
