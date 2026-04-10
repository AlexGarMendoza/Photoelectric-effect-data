import numpy as np
from Dataprocessing import process_all_data

# uses the cleaned data from Dataprocessing.py
# picks the linear region for each wavelength
# does weighted least squares
# finds stopping voltage and its uncertainty

# choose the linear fit region for each wavelength (index range for plots)
#fill in the parenthesis with the values we want for the plots
fit_ranges = {
    "1700A": (),
    "1800A": (),
    "1900A": (),
    "2000A": (),
    "2100A": (),
    "2200A": (),
    "2300A": (),
    "2400A": (),
    "2500A": (),
    "2600A": (),
    "2700A": ()

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






# main part
# prints all fit values
def main():
    results = analyze_all_data()