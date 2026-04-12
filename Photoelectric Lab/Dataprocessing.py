import numpy as np
from pathlib import Path
import re

# takes raw txt file data and pulls out the numbers + metadata 
# computes background current and finds average
# loops through all the wavelength files and creates cleaned data sets

def load_photoelectric_file(filename):
    meta = {}
    rows = []
    reading_table = False

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            # skip empty lines
            if not line:
                continue

            #metadata
            if line.startswith("Photocathode:"):
                match = re.search(r"Material\s+#(\d+)", line)
                if match:
                    meta["material"] = int(match.group(1))

            elif line.startswith("Work Function:"):
                value = line.split(":", 1)[1].strip().split()[0]
                meta["work_function_eV"] = float(value)

            elif line.startswith("Wavelength:"):
                value = line.split(":", 1)[1].strip().split()[0]
                meta["wavelength_A"] = float(value)

            elif line.startswith("Frequency:"):
                value = line.split(":", 1)[1].strip().split()[0]
                meta["frequency_Hz"] = float(value)

            # start of data table 
            elif line.startswith("V_r"):
                reading_table = True
                continue

            #actual number data 
            elif reading_table:
                parts = line.split()

                if len(parts) == 3:
                    try:
                        vr = float(parts[0])
                        i_total = float(parts[1])
                        sigma_i = float(parts[2]) / np.sqrt(100)
                        rows.append([vr, i_total, sigma_i])
                    except ValueError:
                        pass

    if len(rows) == 0:
        raise ValueError(f"No usable number data found in {filename}")

    data = np.array(rows, dtype=float)

    return {
        "meta": meta,
        "Vr": data[:, 0],
        "I_total": data[:, 1],
        "sigma_I": data[:, 2]
    }


# background current stuff
# finds the average background current and its spread
def compute_background(filename):
    bg_data = load_photoelectric_file(filename)

    i_back_avg = np.mean(bg_data["I_total"])
    sigma_back = np.std(bg_data["I_total"], ddof=1)

    return i_back_avg, sigma_back


# loads all wavelength files
# then makes I_photo and sigma_photo for each one
def average_by_voltage(vr, i_total, sigma_i):
    vr_rounded = np.round(vr, 5)
    unique_vr = np.unique(vr_rounded)

    vr_avg = []
    i_total_avg = []
    sigma_total = []

    for value in unique_vr:
        mask = vr_rounded == value
        currents = i_total[mask]
        sigmas = sigma_i[mask]

        vr_avg.append(value)
        i_total_avg.append(np.mean(currents))

        if len(currents) > 1:
            sigma_total.append(np.std(currents, ddof=1))
        else:
            sigma_total.append(sigmas[0])

    return (
        np.array(vr_avg, dtype=float),
        np.array(i_total_avg, dtype=float),
        np.array(sigma_total, dtype=float)
    )

def process_all_data():
    background_file = "Background current secondary.txt"

    # get background numbers first
    i_back_avg, sigma_back = compute_background(background_file)

    datasets = {}

    # grabs all main wavelength files automatically
    for path in sorted(Path(".").glob("main *A.txt")):
        file_data = load_photoelectric_file(path)

        vr_avg, i_total_avg, sigma_total = average_by_voltage(
            file_data["Vr"],
            file_data["I_total"],
            file_data["sigma_I"]
        )

        file_data["Vr"] = vr_avg
        file_data["I_total"] = i_total_avg
        file_data["sigma_I"] = sigma_total

        # subtract background current
        file_data["I_photo"] = file_data["I_total"] - i_back_avg

        # combine uncertainty from total current and background current
        file_data["sigma_photo"] = np.sqrt(file_data["sigma_I"]**2 + sigma_back**2)

        # use wavelength like 1700A as the dictionary key
        key = f'{int(file_data["meta"]["wavelength_A"])}A'
        datasets[key] = file_data

    return i_back_avg, sigma_back, datasets
# main part
# just prints out what got loaded so we can check it
def main():
    i_back_avg, sigma_back, datasets = process_all_data()

    print("Background results")
    print(f"Average background current = {i_back_avg:.6e} A")
    print(f"Background sigma          = {sigma_back:.6e} A")
    print()

    print("Loaded wavelength datasets")

    for key in sorted(datasets.keys(), key=lambda x: int(x[:-1])):
        meta = datasets[key]["meta"]

        print(
            f"{key:>6} | "
            f"frequency = {meta['frequency_Hz']:.6e} Hz | "
            f"points = {len(datasets[key]['Vr'])}"
        )

    print()
    print(f"Total wavelength datasets loaded: {len(datasets)}")


if __name__ == "__main__":
    main()