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

# Dados de infectados atuais no Estado de São Paulo
YData = np.array([1, 1, 1, 2, 2, 2, 2, 2, 3, 6, 10, 13, 16, 16, 19, 30, 46, 65, 152, 164, 240, 286, 396, 396, 631, 745,
                  810, 862, 1052, 1223, 1406, 1451, 1517, 2339, 2981, 3506, 4048, 4466, 4620, 4866, 5682, 6708, 7480,
                  8216, 8419, 8755, 8895, 9371, 11043, 11568, 13894, 14267, 14580, 15385])

CData = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 5, 9, 15, 22, 30, 40, 48, 58, 68, 84,
                  98, 113, 136, 164, 188, 219, 260, 275, 304, 371, 428, 496, 540, 560, 588, 608, 695, 778, 853, 991,
                  1015, 1037, 1093])

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
    print(r_0, g_s)
    subprocess.call(['python', 'cenario_generator.py', '-i', 'cenarioSP', '-d', '0', '25', '75', '200', '-m', '3',
                     '-I0', str(g_s), '-R0', str(r_0)], stdout=open(os.devnull, 'wb'))
    os.chdir("..")
    subprocess.call(['bin/csv_to_input', 'cenarioSP'], stdout=open(os.devnull, 'wb'))
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


r_bound = [1.5, 11.0]
g_bound = [35.0, 55.0]
x0 = [8.0, 50.0]
print(f(x0))
ret = optimize.dual_annealing(f, [r_bound, g_bound], callback=print_fun, maxiter=10, seed=1234)
print("global minimum: x = [%.4f, %.4f], f(x0) = %.4f" % (ret.x[0], ret.x[1], ret.fun))

subprocess.call(['python', 'cenario_generator.py', '-i', 'cenarioSP', '-d', '0', '25', '75', '200', '-m', '3',
                 '-I0', str(ret.x[1]), '-R0', str(ret.x[0])])
os.chdir("..")
subprocess.call(['bin/csv_to_input', 'cenarioSP'])
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', 'output/result_data.csv', '3'])
os.chdir("scripts")
subprocess.call(['python', 'plot_output_SEAHIR_SP.py', '-d', '0', '25', '75', '200', '-s', str(ret.x[1])])