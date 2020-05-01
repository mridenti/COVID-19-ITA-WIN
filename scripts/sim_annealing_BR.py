# coding: utf-8
import numpy as np
import csv
import os
import subprocess
from scipy import optimize
from scipy import stats

# Optimization script based on simulated annealing
# Objective function is the chi2 of death and corrected infection notification

# Output file - this should be fixed
output_file = 'result_data_BR.csv'

# Output uncertainty file  - this should be fixed
output_unc_file = 'uncertainty_data.csv'

# Cenario folder
cenario_folder = 'cenarioBR'

# Number of age groups
age_strata = 16

# Number of days
t_days = 400

# Number of compartments in the output file
compartments = 11

# Dados de infectados atuais no Brasil
YData = np.array([1, 1, 1, 2, 2, 2, 2, 4, 4, 13, 13, 20, 25, 31, 38, 52, 151, 151, 162, 200, 321, 372, 621, 793, 1021,
                  1546, 1924, 2247, 2554, 2985, 3417, 3904, 4256, 4579, 5717, 6836, 8044, 9056, 10360, 11130, 12161,
                  14034, 16170, 18092, 19638, 20727, 22192, 23430, 25262, 28320, 30425, 33682, 36658, 38654, 40743,
                  43079, 45757, 50036, 54043, 59324, 63100, 67446, 73235, 79685, 87187])
CData = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 6, 11, 15, 25, 34, 46, 59, 77, 92,
                  111, 136, 159, 201, 240, 324, 359, 445, 486, 564, 686, 819, 950, 1057, 1124, 1223, 1328, 1532, 1736,
                  1924, 2141, 2354, 2462, 2587, 2741, 2906, 3331, 3704, 4057, 4286, 4603, 5083, 5513, 6006])

tData = np.linspace(0, YData.size - 1, YData.size)
tcData = np.linspace(0, CData.size - 1, CData.size)


class MyBounds(object):
    def __init__(self, xmax, xmin):
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)

    def __call__(self, **kwargs):
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmax and tmin


def print_fun(x, f, accepted):
    print("at minimum %.4f accepted %d" % (f, int(accepted)))


def read_output(out_file):
    y = np.zeros([t_days, age_strata], dtype=np.float64)
    c = np.zeros([t_days, age_strata], dtype=np.float64)
    ri = np.zeros([t_days, age_strata], dtype=np.float64)
    with open(out_file, "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader, None)
        j = 0
        for row in spamreader:
            for i in range(age_strata):
                y[j, i] = row[compartments * (i + 1) + 2]
                c[j, i] = row[compartments * (i + 1) + 6]
            for ii in range(age_strata):
                ri[j, ii] = row[compartments * (age_strata + 1) + ii + 1]
            j = j + 1
        c_s = np.sum(c, axis=1)
        ri_s = np.sum(ri, axis=1)
        y_s = np.sum(y, axis=1)
        return c_s + ri_s + y_s, c_s


def f(x):
    r_0 = x[0]
    g_s = x[1]
    g_e = x[2]
    print(r_0, g_s, g_e)
    subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', '0', '27', '75', '200', '-m', '3',
                     '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                     '-itv', '0', '10', '9', '1'], stdout=open(os.devnull, 'wb'))
    os.chdir("..")
    subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
    subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                     '3'],
                    stdout=open(os.devnull, 'wb'))
    os.chdir("output")
    f_ac, f_c = read_output(output_file)
    os.chdir("..")
    os.chdir("scripts")
    i_ac = len(tData)
    i_c = (CData > 0).astype(bool)
    i_cf = np.zeros(len(f_c), dtype=bool)
    i_cf[0:len(CData)] = i_c
    f_chi2 = np.sum(np.divide(np.multiply(f_ac[0:i_ac] / g_s - YData, f_ac[0:i_ac] / g_s - YData), YData)) + \
             np.sum(np.divide(np.multiply(f_c[i_cf] - CData[i_c], f_c[i_cf] - CData[i_c]), CData[i_c]))

    return f_chi2


def f_s(x, params):
    r_0 = params[0]
    g_s = x[0]
    g_e = params[1]
    fat_fac = params[2]
    subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', '0', '27', '75', '200', '-m', '3',
                     '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                     '-itv', '0', '10', '9', '1', '-f', str(fat_fac)], stdout=open(os.devnull, 'wb'))
    os.chdir("..")
    subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
    subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt',
                     '/'.join(['output', output_unc_file]), '3'], stdout=open(os.devnull, 'wb'))
    os.chdir("output")
    f_ac, f_c = read_output(output_unc_file)
    os.chdir("..")
    os.chdir("scripts")
    i_ac = len(tData)
    i_c = (CData > 0).astype(bool)
    i_cf = np.zeros(len(f_c), dtype=bool)
    i_cf[0:len(CData)] = i_c
    f_chi2 = np.sum(np.divide(np.multiply(f_ac[0:i_ac] / g_s - YData, f_ac[0:i_ac] / g_s - YData), YData)) + \
             np.sum(np.divide(np.multiply(f_c[i_cf] - CData[i_c], f_c[i_cf] - CData[i_c]), CData[i_c]))

    return f_chi2


def pchi2_limit(chi2_0, ngl, par):
    r_0 = par[0]
    g_s = par[1]
    g_e = par[2]
    # plus limit of R0
    delta_par = 0.001 * par[0]
    prob0 = stats.chi2.cdf(ngl, ngl)
    prob = prob0
    while prob < 0.95:
        r_0 = r_0 + delta_par
        chi2_upd = ngl * f_s([g_s], [r_0, g_e, 1.0]) / chi2_0
        prob = stats.chi2.cdf(chi2_upd, ngl)
        err_prob = (prob - 0.95) / 0.95
        if prob > 0.95 and err_prob > 0.01:
            delta_par = 0.5 * delta_par
            prob = 0.95
    r0_plus = r_0
    # minus limit of R0
    r_0 = par[0]
    delta_par = 0.001 * par[0]
    prob = prob0
    while prob < 0.95:
        r_0 = r_0 - delta_par
        chi2_upd = ngl * f_s([g_s], [r_0, g_e, 1.0]) / chi2_0
        prob = stats.chi2.cdf(chi2_upd, ngl)
        err_prob = (prob - 0.95) / 0.95
        if prob > 0.95 and err_prob > 0.01:
            delta_par = 0.5 * delta_par
            prob = 0.95
    r0_minus = r_0
    # plus limit of g_e
    r_0 = par[0]
    delta_par = 0.001 * par[2]
    prob = prob0
    while prob < 0.95:
        g_e = g_e + delta_par
        chi2_upd = ngl * f_s([g_s], [r_0, g_e, 1.0]) / chi2_0
        prob = stats.chi2.cdf(chi2_upd, ngl)
        err_prob = (prob - 0.95) / 0.95
        if prob > 0.95 and err_prob > 0.01:
            delta_par = 0.5 * delta_par
            prob = 0.95
    g_e_plus = g_e
    # minus limit of g_e
    g_e = par[2]
    delta_par = 0.001 * par[2]
    prob = prob0
    while prob < 0.95:
        g_e = g_e - delta_par
        chi2_upd = ngl * f_s([g_s], [r_0, g_e, 1.0]) / chi2_0
        prob = stats.chi2.cdf(chi2_upd, ngl)
        err_prob = (prob - 0.95) / 0.95
        if prob > 0.95 and err_prob > 0.01:
            delta_par = 0.5 * delta_par
            prob = 0.95
    g_e_minus = g_e

    return r0_plus, r0_minus, g_e_plus, g_e_minus


# Optimization to find the best fits and corresponding parameter values

r_bound = [7.0, 11.0]
g_bound = [5.0, 60.0]
g_s_bound = [0.4, 1.0]
ret = optimize.dual_annealing(f, [r_bound, g_bound, g_s_bound], callback=print_fun, maxiter=10, seed=1234)

# Uncertainty estimate:

# First: estimate of the R0 and attenuation factor uncertainties
print("Uncertainty estimate of R0 and attenuation factor:")

df = len(YData) + len(CData) - 3
chi2_init = ret.fun
r0_Plus, r0_Minus, g_e_Plus, g_e_Minus = pchi2_limit(chi2_init, df, [ret.x[0], ret.x[1], ret.x[2]])

# Second: estimate of the under notification factor uncertainty
print("Uncertainty estimate of the under notification index:")
minus_fac = 0.2
plus_fac = 1.8
g_unc_bound = [1.0, 3 * ret.x[1]]
ret_minus = optimize.dual_annealing(f_s, [g_unc_bound], [[ret.x[0], ret.x[2], minus_fac]],
                                    callback=print_fun, maxiter=10, seed=1234)
ret_plus = optimize.dual_annealing(f_s, [g_unc_bound], [[ret.x[0], ret.x[2], plus_fac]],
                                   callback=print_fun, maxiter=10, seed=1234)

subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', '0', '27', '75', '200', '-m', '3',
                 '-I0', str(ret.x[1]), '-R0', str(ret.x[0]), '-Rp', str(ret.x[0]), '-epi', str(ret.x[2]),
                 '-itv', '0', '10', '9', '1', '-s'])


print("global minimum: x = [%.4f, %.4f, %.4f], f(x0) = %.4f" % (ret.x[0], ret.x[1], ret.x[2], ret.fun))
print ("Under notification index uncertainty: [%.4f, %.4f]" % (ret_minus.x, ret_plus.x))
print ("R0 uncertainty: [%.4f, %.4f]" % (r0_Plus, r0_Minus))
print ("Attenuation factor uncertainty: [%.4f, %.4f]" % (g_e_Plus, g_e_Minus))
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt','/'.join(['output', output_file]),
                 '3'],
                stdout=open(os.devnull, 'wb'))
os.chdir("scripts")
subprocess.call(['python', 'plot_output_SEAHIR_BR.py', '-d', '0', '27', '75', '200', '-s', str(ret.x[1])])
