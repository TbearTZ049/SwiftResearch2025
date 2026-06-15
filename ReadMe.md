## Burst Chaser v2

This will be a guide on how use and recreate the setup for burst chaser v2 that was previously created by Carter Murawski. It will explain how to download the initial CSV and what code to run to get each resulting data point. It will also contain the steps taken to create new additions to the project. For a more detailed look into the math and machine learning, please refer to the overleaf document within this folder which contains Carter's Research paper. 

## Baseline (reproduced [6.10.26])
Honest accuracy on the 46-burst expert golden sample:
- Citizen science (majority vote): ~[__]%
- Image-ML (RF on 32×32 plot images): [__]/46 = [__]%  — collapses to "Simple"
- (Internal 20% holdout: 93% — same-distribution, overfit, *not* the golden sample)


## 0. Install the tools

**Miniconda** — manages the isolated Python environment.
- Windows
  Download the Windows 64-bit installer from the official Miniconda page (search "Miniconda" → docs.conda.io) and run it with the default options.
    - **Windows note:** After installing, open **"Anaconda Prompt (miniconda3)"** from the Start Menu and run all `conda` commands *there*. That shortcut comes pre-configured, so `conda` and `conda activate` work immediately. Plain PowerShell or CMD often won't activate environments until extra setup (see Troubleshooting), so save yourself the headache and use the Anaconda Prompt.
    - **Git for Windows** — version control.
If you'd like you can download from <https://git-scm.com> and install with defaults which besides `git`, will give you two useful bonuses: **Git Bash** (Unix-style shell where most Mac/Linux commands work exactly as written) and **Git Credential Manager** (handles GitHub login through your browser — no SSH keys to set up).


- MacOS
  - Installation for mininconda can be sourced through homebrew or through the GUI downloader
      -  brew install --cask miniconda
      - conda init "$(basename "${SHELL}")"

**VS Code** — editor.
Install from <https://code.visualstudio.com> and add the **Python** and **Jupyter** extensions (both by Microsoft).

**Which shell to use, and when:**
- **Anaconda Prompt** → anything involving `conda` (creating the environment, installing packages).
- **Git Bash** → `git` commands, and any Unix-style file commands (`cat`, `touch`, etc.).
- Either one can run the `python <script>.py` commands once the environment is active.

---

## Environment
- conda env `burstchaser` (Python 3.11); rebuild with `conda env create -f environment.yml`. 


# Burst Chaser — Code Reproduction & Setup Guide

## Baseline (reproduced [6.10.26])
Honest accuracy on the 46-burst expert golden sample:
- Citizen science (majority vote): ~[__]%
- Image-ML (RF on 32×32 plot images): [__]/46 = [__]%  — collapses to "Simple"
- (Internal 20% holdout: 93% — same-distribution, overfit, *not* the golden sample)

## 0. Install the tools

**Miniconda** — manages the isolated Python environment.
Download the Windows 64-bit installer from the official Miniconda page (search "Miniconda" → docs.conda.io) and run it with the default options.
- **Windows note:** After installing, open **"Anaconda Prompt (miniconda3)"** from the Start Menu and run all `conda` commands *there*. That shortcut comes pre-configured, so `conda` and `conda activate` work immediately. Plain PowerShell or CMD often won't activate environments until extra setup (see Troubleshooting), so save yourself the headache and use the Anaconda Prompt.

**Git for Windows** — version control.
If you'd like you can download from <https://git-scm.com> and install with defaults which besides `git`, will give you two useful bonuses: **Git Bash** (Unix-style shell where most Mac/Linux commands work exactly as written) and **Git Credential Manager** (handles GitHub login through your browser — no SSH keys to set up).

**VS Code** — editor.
Install from <https://code.visualstudio.com> and add the **Python** and **Jupyter** extensions (both by Microsoft).

**Which shell to use, and when:**
- **Anaconda Prompt** → anything involving `conda` (creating the environment, installing packages).
- **Git Bash** → `git` commands, and any Unix-style file commands (`cat`, `touch`, etc.).
- Either one can run the `python <script>.py` commands once the environment is active.

---

---

## 1. Get the repo

Recommended: clone **my fork**, which already includes the model-training fix from Step 5 (so you can skip that edit).

```bash
git clone https://github.com/TbearTZ049/SwiftResearch2025.git
cd SwiftResearch2025
```

**Note:** the repo is ~79 MB because it stores ~2,800 light-curve images. 

The first time you `git push`, a browser window will pop up to log into GitHub (via Git Credential Manager).

---

## 2. Create the Python environment

- conda env `burstchaser` (Python 3.11); rebuild with `conda env create -f environment.yml`. 

or In **Anaconda Prompt**:

```bash
conda create -n burstchaser python=3.11
conda activate burstchaser
```

`conda create` builds an isolated Python 3.11 sandbox named `burstchaser`, so this project's libraries don't collide with anything else on your system. Once it's active, your prompt shows `(burstchaser)` at the start of the line — that's how you know you're in it.

### Blocker #1 — the Anaconda 429 error

When you try to install packages, you may hit this:

```
CondaHTTPError: HTTP 429 terms of service rate limit exceeded for url
https://repo.anaconda.com/pkgs/main/...
```

**Why it happens:** conda defaults to Anaconda's commercial package repo, which now rate-limits and requires accepting their terms of service.

**The fix:** switch to **conda-forge**, the free community-run channel (it has full Windows builds of everything). Run:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Then rebuild the environment cleanly so even Python itself comes from conda-forge (your first attempt left it empty anyway):

```bash
conda deactivate
conda env remove -n burstchaser -y
conda create --override-channels -c conda-forge -n burstchaser python=3.11 -y
conda activate burstchaser
```

The `--override-channels -c conda-forge` part forces conda to use *only* conda-forge and ignore Anaconda's repo entirely. That's what makes the 429 impossible to recur.

### Install the libraries

```bash
conda install --override-channels -c conda-forge numpy pandas scipy matplotlib scikit-learn scikit-image pillow astropy jupyter ipykernel -y
```

What they're for:
- **pandas / numpy** — tables and arrays.
- **scikit-learn** — the Random Forest classifier (and the K-means used in the pulse-location track).
- **scikit-image / pillow** — reading and shrinking the light-curve images.
- **matplotlib / astropy** — plotting and astronomy data handling (needed for the next phase of the project).
- **jupyter / ipykernel** — notebook support inside VS Code.

This pulls in a long list of dependency packages.

---

## 3. Register the environment with Jupyter / VS Code

```bash
python -m ipykernel install --user --name burstchaser --display-name "Python (burstchaser)"
```

This makes `burstchaser` selectable as a kernel inside VS Code notebooks. In VS Code: open the repo folder, then **Ctrl+Shift+P → "Python: Select Interpreter"** and pick `burstchaser`. For notebooks, choose the **"Python (burstchaser)"** kernel.

---

## 4. Blocker #2 — the pandas 3.0 training error

**If you cloned my fork, this is already fixed — skip to Step 6.** If you're working from a copy of the *original* repo, you'll hit this when you run `ImageRecognition.py`:

- *NOTE Error & Fix* from Burstchaser v1: pandas 3.0 + pyarrow makes string columns Arrow-backed; sklearn can't index
  them. Fixed with `.to_numpy()` (see Changes).

```
TypeError: only integer scalar arrays can be converted to a scalar index
```

(the traceback ends in a `pyarrow ... ChunkedArray.__getitem__` line).

**Why it happens:** pandas 3.0 (which conda-forge installs) stores text columns as "Arrow-backed" strings when the `pyarrow` library is present — and pyarrow gets pulled in automatically. The original code reads the label column with `.values`, which on an Arrow-backed column hands back a type that scikit-learn's `train_test_split` can't index.

**The fix:** open `ImageRecognition.py` in VS Code and find this line near the top (around line 21):

```python
labels = df[label_column].values
```

Change `.values` to `.to_numpy()`:

```python
labels = df[label_column].to_numpy()
```

`.to_numpy()` always returns a plain NumPy array regardless of the column's storage backend, which scikit-learn handles without issue. This fix is platform-independent and will be identical on Windows and Mac.

---

## 5. Reproduce the pipeline

Make sure you're in the repo folder with `(burstchaser)` active, then run these **in order**. (The forward-slash file paths inside the scripts work fine on Windows — Python normalizes them automatically.)


```bash
python GoldenSampleCheck.py
python Process_Images.py
python ImageRecognition.py
python generate_ml_csv.py
python GoldenSampleCheck.py
```

What each one does:

1. **GoldenSampleCheck.py** (first run) — scores the existing model's predictions against the 46 expert-labeled "golden sample" bursts and prints how many it got right.
2. **Process_Images.py** — reads each burst's light-curve PNG, shrinks it to 32×32 pixels, flattens it into a row of pixel values, and writes `ClassifiedBursts/Image_Labels.csv`. (It prints progress through ~1,486 bursts.)
3. **ImageRecognition.py** — trains a Random Forest on those pixel rows, prints its accuracy, and saves the model to `MachineLearning/rf_model.pkl`.
4. **generate_ml_csv.py** — applies the trained model to every burst and writes its predictions into `MachineLearning/pulse_shape_freq_with_ml.csv`.
5. **GoldenSampleCheck.py** (second run) — re-scores using the model you just trained.

**Ignore `train_model.py`** — it's a leftover that reads a file nothing produces. The real trainer is `ImageRecognition.py`.

**About `ReadDataExport.py`:** it's listed as step 1 in the original README, but it needs the raw Zooniverse classification export, which isn't in the repo. You don't need it to reproduce anything — every script above runs from CSVs that are already committed. 

---

## 6. Confirm 

You've reproduced it correctly if you see:

From **ImageRecognition.py**:

```
Train Accuracy: 1.000
Test Accuracy: 0.932
```

From the final **GoldenSampleCheck.py**:

```
✅ Total Compared: 46
✅ Matches: 14
❌ Mismatches: 32
```

…with every mismatch showing `ML_Verify = Simple`.

**What these numbers mean** (so they make sense): the model scores 93% on a random split of the *training* bursts but only **14/46 ≈ 30%** on the expert golden sample. It learns to label almost everything "Simple," and the golden sample is dominated by the "Other" / multi-pulse class it can't recognize. That **30% is the baseline**, not the 93%. Reproducing these exact numbers means your environment matches and is working from the same starting point.

---

## Windows troubleshooting

**`conda` not recognized, or `conda activate` seems to do nothing.**
Use the **Anaconda Prompt (miniconda3)** Start Menu shortcut instead of plain CMD/PowerShell. If you must use PowerShell, run `conda init powershell`, then fully close and reopen the terminal. If activation is *still* blocked, run this once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` — PowerShell blocks conda's activation script by default, and this allows it.

**`python` not recognized.**
The environment isn't active. Re-run `conda activate burstchaser` and confirm you see the `(burstchaser)` prefix on your prompt.

**`cat`, `touch`, `mkdir -p`, or `<< EOF` don't work.**
Those are Unix commands. Either run them in **Git Bash**, or just create and edit files directly in VS Code (e.g., make a new file in the editor instead of using `touch`).

**Git warns about line endings (LF vs CRLF).**
Harmless, but to quiet it run `git config --global core.autocrlf true`. This is the Windows-standard setting and converts line endings automatically.

**The 429 error comes back on a later install.**
That command isn't using conda-forge. Add `--override-channels -c conda-forge` to the `conda install`, or check that `conda config --show channels` lists `conda-forge` at the top.

**The `TypeError ... ChunkedArray` error appears in a different script.**
Same pandas-3.0 Arrow cause as Blocker #2. Find the offending `.values` and replace it with `.to_numpy()`.

---







Downloading Classifications CSV from Zooniverse 

    1. Go to Zooniverse Burst Chaser and log into your account
    2. Navigate to the Lab section 
    3. Find Data Exports
    4. Request a new classification export 
        a. This may take a while due to Zooniverse system, but you will get 
            an email notifying you when things are ready. 
    5. Download your Data Export 

    This export will consist of classifications from all of the citizen science surveys

Reading the Classifications CSV

    1. Have Classifications CSV in your computer or folder. 
    2. Navigate to the ReadDataExport file
    3. Ajust the CSV it is running
    4. When Ran All CSVS will be updated 

Label Bursts with Classifications

    1. Locate Prop_Freq_Verify
    2. When ran it will use your previosly created Pulse_Shapes CSV
        and Label bursts based of proportional data and frequency statistics.
    3. Output Can be found in classified bursts.

Create Image Processing and Machine Learning Labels

    1.Processing Images and Create ML by running Proccess_Images.py file
    2.ImageRecognition will create a machine learning algorithm to classify
    3.Generate_ml_to_csv creates a csv that labels bursts based off machine learning


Pulse Locations and Painting Boxes 
    1. KmeanLocation.py because all of your location results are in a csv you will use this file
        to eliminate some of the boxes. 
    2. Then run PaintBoxes.py to create images with the narrowd down boxes
        results will be in the. 


