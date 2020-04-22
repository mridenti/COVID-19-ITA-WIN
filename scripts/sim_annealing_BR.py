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

# Dados de infectados atuais no Brasil
YData = np.array([1, 1, 1, 2, 2, 2, 2, 4, 4, 13, 13, 20, 25, 31, 38, 52, 151, 151, 162, 200, 321, 372, 621, 793, 1021,
                  1546, 1924, 2247,  2554, 2985, 3417, 3904, 4256, 4579, 5717, 6836, 8044, 9056, 10360, 11130, 12161,
                  14034, 16170, 18092, 19638, 20727, 22192,	23430,	25262,	28320,	30425, 33682, 36658, 38654, 40743,
                  43079])
CData = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 6, 11, 15, 25, 34, 46, 59, 77, 92,
                  111, 136, 159, 201, 240, 324, 359, 445, 486, 564, 686, 819, 950, 1057, 1124, 1223, 1328, 1532, 1736,
                  1924, 2141, 2354, 2462, 2587, 2741])

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
    subprocess.call(['python', 'cenario_generator.py', '-i', 'cenarioBR', '-d', '0', '27', '75', '200', '-m', '3',
                     '-I0', str(g_s), '-R0', str(r_0)], stdout=open(os.devnull, 'wb'))
    os.chdir("..")
    subprocess.call(['bin/csv_to_input', 'cenarioBR'], stdout=open(os.devnull, 'wb'))
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
g_bound = [35.0, 60.0]
x0 = [8.0, 50.0]
print(f(x0))
ret = optimize.dual_annealing(f, [r_bound, g_bound], callback=print_fun, maxiter=10, seed=1234)
print("global minimum: x = [%.4f, %.4f], f(x0) = %.4f" % (ret.x[0], ret.x[1], ret.fun))

subprocess.call(['python', 'cenario_generator.py', '-i', 'cenarioBR', '-d', '0', '27', '75', '200', '-m', '3',
                 '-I0', str(ret.x[1]), '-R0', str(ret.x[0])])
os.chdir("..")
subprocess.call(['bin/csv_to_input', 'cenarioBR'])
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', 'output/result_data.csv', '3'])
os.chdir("scripts")
subprocess.call(['python', 'plot_output_SEAHIR_BR.py', '-d', '0', '27', '75', '200', '-s', str(ret.x[1])])