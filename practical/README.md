**English** | [Deutsch](README.de.md)

# Practical: a bacterium in the computer

In this practical you'll use a computer model of the bacterium *E. coli* to predict how fast it grows, what it eats and which genes it can't live without.

## Starting

You need **Docker Desktop**, and it must be running (look for the whale icon).

| Computer | Double-click |
|---|---|
| Windows | `start.bat` |
| Mac | `start.command` |
| Linux | run `./start.sh` in a terminal |

After a few seconds your browser opens **JupyterLab** with the `en` folder. If it doesn't, open <http://localhost:8888> yourself.

## Working

Open the notebooks in order:

1. `00_welcome.ipynb`: how notebooks work
2. `01_tutorial_fba.ipynb`: the bacterium in the computer
3. `02_exercise_oxygen.ipynb`: life without oxygen
4. `03_exercise_food.ipynb`: what's on the menu?
5. `04_exercise_knockouts.ipynb`: switching off genes
6. `05_bonus_production.ipynb`: bacteria as factories (bonus)

Run a cell with **Shift + Enter**. Where you see `___`, fill in the gap. Your work is saved in this `practical` folder on your own computer.

## Stopping

Double-click `stop.bat` (Windows) or run `./stop.sh` (Mac/Linux). Your notebooks stay where they are.

## Something went wrong?

* **"Docker is not running"**: start Docker Desktop, wait until it says it's running, try again.
* **A cell shows an error**: check that you ran the cells above it, from the top.
* **Start a notebook again from scratch**: menu *Kernel → Restart Kernel and Clear…*, then run the cells again.
* Still stuck? Ask your teacher.

## Credits

The *E. coli* core model comes from the [BiGG Models](http://bigg.ucsd.edu) database (Orth, Fleming & Palsson 2010; King et al. 2016). The calculations use the [COBRA Toolbox](https://github.com/opencobra/cobratoolbox) (Heirendt et al. 2019) in [GNU Octave](https://octave.org). The full sources are at the end of `01_tutorial_fba.ipynb`.

These materials are licensed under [CC BY 4.0](../LICENSE-CC-BY-4.0.txt) (notebooks) and [MIT](../LICENSE) (code).
