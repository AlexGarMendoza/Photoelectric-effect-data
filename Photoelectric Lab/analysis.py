import numpy as np
from Dataprocessing import process_all_data

# uses the cleaned data from Dataprocessing.py
# picks the linear region for each wavelength
# does weighted least squares
# finds stopping voltage and its uncertainty

# choose the linear fit region for each wavelength (index range for plots)
#fill in the parenthesis with the values we want for the plots
fit_ranges = {
    "1700A": (200, 700),
    "1800A": (200, 700),
    "1900A": (200, 700),
    "2000A": (200, 700),
    "2100A": (200, 700),
    "2200A": (200, 700),
    "2300A": (200, 700),
    "2400A": (200, 700),
    "2500A": (200, 700),
    "2600A": (200, 700),
    "2700A": (200, 700)

}

# weighted least squares fit by hand
# fits y = a + bx
# instead of treating all points equally, we weight them by 1 / sigma^2
# so points with smaller sigma (more reliable) have more influence
# and points with larger sigma (noisier) have less influence

def weighted_least_squares(x, y, sigma):
    w = 1.0 / (sigma ** 2) # function 

    sum_w = np.sum(w)
    sum_xw = np.sum(x * w)
    sum_yw = np.sum(y * w)
    sum_x2w = np.sum((x ** 2) * w)
    sum_xyw = np.sum(x * y * w)

    delta = sum_w * sum_x2w - (sum_xw ** 2)

    a = (sum_x2w * sum_yw - sum_xw * sum_xyw) / delta
    b = (sum_w * sum_xyw - sum_xw * sum_yw) / delta

    sigma_a = np.sqrt(sum_x2w / delta)
    sigma_b = np.sqrt(sum_w / delta)

    return a, b, sigma_a, sigma_b

#finds stopping voltage and its uncertainty 
# Vs = -a/b
def compute_stopping_voltage(a, b, sigma_a, sigma_b):
    vs = -a / b

    sigma_vs = abs(vs) * np.sqrt(
        (sigma_a / a) ** 2 + (sigma_b / b) ** 2
    )

    return vs, sigma_vs


# runs the analysis for every wavelength
def analyze_all_data():
    i_back_avg, sigma_back, datasets = process_all_data()

    results = []

    for key in sorted(datasets.keys(), key=lambda x: int(x[:-1])):
        data = datasets[key]

        if key not in fit_ranges:
            print(f"Skipping {key} because no fit range was given.")
            continue

        start, stop = fit_ranges[key]

        vr = data["Vr"][start:stop]
        i_photo = data["I_photo"][start:stop]
        sigma_photo = data["sigma_photo"][start:stop]

        a, b, sigma_a, sigma_b = weighted_least_squares(vr, i_photo, sigma_photo)
        vs, sigma_vs = compute_stopping_voltage(a, b, sigma_a, sigma_b)

        results.append({
            "wavelength_A": data["meta"]["wavelength_A"],
            "frequency_Hz": data["meta"]["frequency_Hz"],
            "a": a,
            "b": b,
            "sigma_a": sigma_a,
            "sigma_b": sigma_b,
            "Vs": vs,
            "sigma_Vs": sigma_vs
        })

    return results






# main part
# prints all fit values
def main():
    results = analyze_all_data()

    print("Analysis results")

    for item in results:
        print(
            f"{int(item['wavelength_A']):>4}A | "
            f"a = {item['a']:.6e} | "
            f"b = {item['b']:.6e} | "
            f"sigma_a = {item['sigma_a']:.6e} | "
            f"sigma_b = {item['sigma_b']:.6e} | "
            f"Vs = {item['Vs']:.6f} V | "
            f"sigma_Vs = {item['sigma_Vs']:.6f} V"
        )


if __name__ == "__main__":
    main()