# Photoelectric Effect Data Analysis

Data processing and plot generation for the photoelectric effect lab at Portland State University.

---

## Setup

Requires Python 3. All dependencies are installed into a local virtual environment.

```bash
cd "Photoelectric Lab"
python3 -m venv .venv
.venv/bin/pip install numpy matplotlib watchdog
```

---

## Generating Plots

Run this once to generate all figures:

```bash
cd "Photoelectric Lab"
.venv/bin/python report_plots.py
```

This produces:
- `figure_photocurrent_<wavelength>.png` — photocurrent vs. retarding voltage for each wavelength (1700A–2700A), with the weighted linear fit overlaid
- `figure_stopping_voltage.png` — stopping voltage vs. frequency with the final fit, used to extract Planck's constant

---

## Adjusting the Linear Fit Region

The fit region for each wavelength is set by index ranges in `analysis.py`:

```python
fit_ranges = {
    "1700A": (start_index, stop_index),
    ...
}
```

The indices refer to row positions in the data arrays (0 = first voltage point). To find which indices correspond to which voltages, open `plotted_points.txt` — it lists every data point with its index, voltage, and background-subtracted photocurrent side by side for all wavelengths.

To auto-regenerate all figures whenever you update `fit_ranges`, run the watcher:

```bash
cd "Photoelectric Lab"
.venv/bin/python watch_fit.py
```

Save `analysis.py` and all figures will regenerate automatically. Stop the watcher with `Ctrl+C`.

---

## File Overview

| File | Purpose |
|------|---------|
| `Dataprocessing.py` | Loads raw data files, subtracts background current, propagates uncertainties |
| `analysis.py` | Defines fit ranges, runs weighted least squares, computes stopping voltages |
| `final_fit.py` | Fits stopping voltage vs. frequency to extract Planck's constant and work function |
| `report_plots.py` | Generates all figures |
| `watch_fit.py` | Watches `analysis.py` for changes and reruns all figures automatically |
| `plotted_points.txt` | Full data table (indexed) for identifying linear fit regions |

---

## Data Files

- `main data <wavelength>A.txt` — raw photocurrent measurements (1000 voltage points, each averaged over 100 trials)
- `Background current secondary.txt` — background current measurement, subtracted from all datasets
