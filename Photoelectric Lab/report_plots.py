import numpy as np
import matplotlib.pyplot as plt

from Dataprocessing import process_all_data
from analysis import analyze_all_data, weighted_least_squares, fit_ranges
from final_fit import final_fit


# makes one photocurrent vs retarding voltage plot
# also draws the weighted fit line on the chosen linear region
def plot_photocurrent_curve(wavelength_key, filename):
    i_back_avg, sigma_back, datasets = process_all_data()

    if wavelength_key not in datasets:
        print(f"{wavelength_key} not found.")
        return

    data = datasets[wavelength_key]

    vr = data["Vr"]
    i_photo = data["I_photo"]
    sigma_photo = data["sigma_photo"]

    # get the fit range from analysis.py
    start, stop = fit_ranges[wavelength_key]

    x_fit = vr[start:stop]
    y_fit = i_photo[start:stop]
    sigma_fit = sigma_photo[start:stop]

    # weighted fit for the chosen linear region
    a, b, sigma_a, sigma_b = weighted_least_squares(x_fit, y_fit, sigma_fit)
    vs = -a / b

    # line for the fit
    x_line = np.linspace(x_fit.min(), x_fit.max(), 200)
    y_line = a + b * x_line

    plt.figure()
    plt.errorbar(
        vr,
        i_photo,
        yerr=sigma_photo,
        fmt='o',
        markersize=3,
        capsize=2,
        label="Data"
    )
    plt.plot(x_line, y_line, label="Weighted fit")

    plt.xlabel("Retarding Voltage (V)")
    plt.ylabel("Photocurrent (A)")
    plt.title(f"Photocurrent vs. Retarding Voltage ({wavelength_key})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()

    print(f"Saved {filename}")


# makes the final stopping voltage vs frequency plot
def plot_final_fit(filename):
    analysis_results = analyze_all_data()
    fit_results = final_fit()

    frequency = np.array([item["frequency_Hz"] for item in analysis_results])
    vs = np.array([item["Vs"] for item in analysis_results])
    sigma_vs = np.array([item["sigma_Vs"] for item in analysis_results])

    A = fit_results["A"]
    B = fit_results["B"]

    x_line = np.linspace(frequency.min(), frequency.max(), 300)
    y_line = A + B * x_line

    plt.figure()
    plt.errorbar(
        frequency,
        vs,
        yerr=sigma_vs,
        fmt='o',
        markersize=4,
        capsize=3,
        label="Data"
    )
    plt.plot(x_line, y_line, label="Weighted fit")

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Stopping Voltage (V)")
    plt.title("Stopping Voltage vs. Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(filename)
    plt.close()

    print(f"Saved {filename}")


# main
# makes the 3 plots for the report
def main():
    plot_photocurrent_curve("1700A", "figure1_photocurrent_1700A.png")
    plot_photocurrent_curve("2700A", "figure2_photocurrent_2700A.png")
    plot_final_fit("figure3_stopping_voltage.png")


if __name__ == "__main__":
    main()