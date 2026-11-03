[English](README.md) | **Deutsch**

# Praktikum: Ein Bakterium im Computer

In diesem Praktikum benutzt du ein Computermodell des Bakteriums *E. coli*, um vorherzusagen, wie schnell es wächst, was es frisst und auf welche Gene es nicht verzichten kann.

## Starten

Du brauchst **Docker Desktop**, und es muss laufen (achte auf das Wal-Symbol).

| Computer | Doppelklick auf |
|---|---|
| Windows | `start_de.bat` |
| Mac | `start_de.command` |
| Linux | im Terminal `./start.sh de` ausführen |

**Mac, nur beim ersten Mal:** macOS blockiert `start_de.command`, weil die Datei aus dem Internet heruntergeladen wurde. Rechtsklick → *Öffnen* hilft nicht. Stattdessen:

1. Doppelklicke auf `start_de.command`. macOS meldet, dass die Datei nicht geöffnet werden kann; klicke auf **Fertig**.
2. Öffne  → **Systemeinstellungen → Datenschutz & Sicherheit**, scrolle nach unten und klicke neben `start_de.command` auf **Dennoch öffnen**.
3. Gib dein Mac-Passwort ein (oder nutze Touch ID) und klicke noch einmal auf **Dennoch öffnen**.
4. Wenn Terminal nach Zugriff auf den Ordner *Downloads* fragt, klicke auf **Erlauben**.

Nach ein paar Sekunden öffnet sich dein Browser mit **JupyterLab** und dem Ordner `de`. Falls nicht, öffne <http://localhost:8888> selbst.

## Arbeiten

Öffne die Notebooks der Reihe nach:

1. `00_welcome.ipynb`: So funktionieren Notebooks
2. `01_tutorial_fba.ipynb`: Ein Bakterium im Computer
3. `02_exercise_oxygen.ipynb`: Leben ohne Sauerstoff
4. `03_exercise_food.ipynb`: Was steht auf dem Speiseplan?
5. `04_exercise_knockouts.ipynb`: Gene ausschalten
6. `05_bonus_production.ipynb`: Bakterien als Fabriken (Bonus)

Eine Zelle führst du mit **Umschalt + Enter** aus. Wo `___` steht, füllst du die Lücke aus. Deine Arbeit wird in diesem Ordner `practical` auf deinem eigenen Computer gespeichert.

## Beenden

Doppelklicke auf `stop.bat` (Windows) oder führe `./stop.sh` aus (Mac/Linux). Deine Notebooks bleiben erhalten.

## Etwas klappt nicht?

* **„Docker läuft nicht“**: Starte Docker Desktop, warte, bis es läuft, und versuche es noch einmal.
* **Eine Zelle zeigt einen Fehler**: Prüfe, ob du die Zellen darüber ausgeführt hast, von oben angefangen.
* **Ein Notebook ganz von vorn beginnen**: Menü *Kernel → Kernel neu starten und Ausgaben aller Zellen löschen…*, dann die Zellen noch einmal ausführen.
* Kommst du nicht weiter? Frag deine Lehrkraft.

## Quellen

Das *E.-coli*-Kernmodell stammt aus der Datenbank [BiGG Models](http://bigg.ucsd.edu) (Orth, Fleming & Palsson 2010; King et al. 2016). Die Berechnungen nutzen die [COBRA Toolbox](https://github.com/opencobra/cobratoolbox) (Heirendt et al. 2019) in [GNU Octave](https://octave.org). Die vollständigen Quellen stehen am Ende von `01_tutorial_fba.ipynb`.

Diese Materialien stehen unter [CC BY 4.0](../LICENSE-CC-BY-4.0.txt) (Notebooks) und [MIT](../LICENSE) (Code).
