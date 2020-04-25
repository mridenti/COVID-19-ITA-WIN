# coding: utf-8
import numpy as np
import csv
import os
import subprocess
from scipy import optimize

# Optimization script based on simulated annealing
# Objective function is the chi2 of death and corrected infection notification

# Output file - this should be fixed
output_file = 'result_data.csv'

# Number of age groups
age_strata = 16

# Number of days
t_days = 400

# Number of compartments in the output file
compartments = 11

# Dados de infectados atuais em Manaus
YData = np.array([2, 2, 3, 7, 11, 25, 31, 45, 52, 63, 75, 105, 131, 140, 159, 179, 205, 232, 283, 379, 473, 560, 712,
                  800, 863, 932, 1053, 1106, 1295, 1350, 1459, 1531, 1593, 1664, 1772, 1809, 1958, 2286, 2481])

CData = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 5, 9, 11, 15, 19, 25, 33, 42, 45, 51, 60, 81, 92,
                  107, 127, 134, 155, 156, 163, 172, 193, 207])

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
    subprocess.call(['python', 'cenario_generator.py', '-i', 'cenarioManaus', '-d', '0', '8', '22', '200', '-m', '3',
                     '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                     '-itv', '0', '9', '10', '1'], stdout=open(os.devnull, 'wb'))
    os.chdir("..")
    subprocess.call(['bin/csv_to_input', 'cenarioManaus'], stdout=open(os.devnull, 'wb'))
    subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', 'output/result_data.csv', '3'],
                    stdout=open(os.devnull, 'wb'))
    os.chdir("output")
    f_ac, f_c = read_output(output_file)
    os.chdir("..")
    os.chdir("scripts")
    i_ac = len(tData)
    i_c = (CData > 0).astype(bool)
    i_cf = np.zeros(len(f_c), dtype=bool)
    i_cf[0:len(CData)] = i_c
    f_chi2 = np.sum(np.divide(np.multiply(f_ac[0:i_ac]/g_s - YData, f_ac[0:i_ac]/g_s - YData), YData)) + \
             np.sum(np.divide(np.multiply(f_c[i_cf] - CData[i_c], f_c[i_cf] - CData[i_c]), CData[i_c]))

    return f_chi2


r_bound = [7.0, 20.0]
g_bound = [60.0, 200.0]
g_e_bound = [0.2, 1.0]
ret = optimize.dual_annealing(f, [r_bound, g_bound, g_e_bound], callback=print_fun, maxiter=10, seed=1234)
print("global minimum: x = [%.4f, %.4f, %.4f], f(x0) = %.4f" % (ret.x[0], ret.x[1], ret.x[2], ret.fun))

subprocess.call(['python', 'cenario_generator.py', '-i', 'cenarioManaus', '-d', '0', '8', '22', '200', '-m', '3',
                 '-I0', str(ret.x[1]), '-R0', str(ret.x[0]), '-Rp',  str(ret.x[0]), '-epi', str(ret.x[2]),
                 '-itv', '0', '9', '10', '1'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', 'cenarioManaus'])
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', 'output/result_data.csv', '3'])
os.chdir("scripts")
subprocess.call(['python', 'plot_output_SEAHIR_Manaus.py', '-d', '0', '8', '22', '200', '-s', str(ret.x[1])])