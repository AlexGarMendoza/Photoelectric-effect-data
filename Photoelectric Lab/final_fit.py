import numpy as np
from analysis import analyze_all_data

# takes stopping voltage results and computes final values
# finds Planck's constant, work function, R^2, and percent error


# constants
e = 1.602176634e-19
h_accepted = 6.62607015e-34


# weighted least squares fit
# same idea as before but now fitting Vs vs frequency
def weighted_least_squares(x, y, sigma):
    w = 1.0 / (sigma ** 2)

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


# computes R^2
def compute_r_squared(x, y, a, b):
    y_fit = a + b * x

    ss_err = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)

    return 1 - (ss_err / ss_tot)


# main final calculation
def final_fit():
    results = analyze_all_data()

    freq = np.array([item["frequency_Hz"] for item in results])
    vs = np.array([item["Vs"] for item in results])
    sigma_vs = np.array([item["sigma_Vs"] for item in results])

    # fit: Vs = A + B * frequency
    A, B, sigma_A, sigma_B = weighted_least_squares(freq, vs, sigma_vs)

    # physics results
    h = e * B
    sigma_h = e * sigma_B

    phi_J = -e * A
    sigma_phi_J = e * sigma_A

    phi_eV = -A
    sigma_phi_eV = sigma_A

    r_squared = compute_r_squared(freq, vs, A, B)

    percent_error_h = abs((h - h_accepted) / h_accepted) * 100

    return {
        "A": A,
        "B": B,
        "sigma_A": sigma_A,
        "sigma_B": sigma_B,
        "h": h,
        "sigma_h": sigma_h,
        "phi_J": phi_J,
        "sigma_phi_J": sigma_phi_J,
        "phi_eV": phi_eV,
        "sigma_phi_eV": sigma_phi_eV,
        "R_squared": r_squared,
        "percent_error_h": percent_error_h
    }


# main
# prints final values
def main():
    results = final_fit()

    print("Final fit results")
    print(f"A = {results['A']:.6e} V")
    print(f"B = {results['B']:.6e} V/Hz")
    print(f"sigma_A = {results['sigma_A']:.6e} V")
    print(f"sigma_B = {results['sigma_B']:.6e} V/Hz")
    print()

    print("Final results")
    print(f"h = {results['h']:.6e} J*s")
    print(f"sigma_h = {results['sigma_h']:.6e} J*s")
    print(f"phi = {results['phi_J']:.6e} J")
    print(f"sigma_phi_J = {results['sigma_phi_J']:.6e} J")
    print(f"phi = {results['phi_eV']:.6f} eV")
    print(f"sigma_phi_eV = {results['sigma_phi_eV']:.6f} eV")
    print(f"R^2 = {results['R_squared']:.6f}")
    print(f"Percent error in h = {results['percent_error_h']:.6f}%")


if __name__ == "__main__":
    main()