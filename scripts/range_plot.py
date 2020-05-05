# coding: utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import os
import subprocess
import datetime

# Output file - this should be fixed
output_file = 'result_data_SP_CAPITAL_range.csv'

# Cenario folder
cenario_folder = 'cenarioSP_CAPITAL'

# Number of age groups
age_strata = 16

# Number of days
t_days = 400

# Number of compartments in the output file
compartments = 11

# Time specifications for plot
months = mdates.MonthLocator()  # every month
weeks = mdates.WeekdayLocator()  # every week
month_fmt = mdates.DateFormatter('%b')

# São Paulo Capital
day_init = 0
day_next_1 = 25
day_next_2 = 74
day_next_3 = 151
leitos = 4861
year = 2020
month = 2
day = 26
# day_mid = 125

# São José dos Campos
# day_init = 0
# day_next_1 = 21
# day_next_2 = 53
# day_next_3 = 135
# day_mid = 104

# Manaus
# day_init = 0
# day_next_1 = 9
# day_next_2 = 58
# day_next_3 = 143
# day_mid = 112

# Fixed post break parameters
# SJC
# g_s = 20
# r_0 = 4.5
# g_e = 0.53

# SP Capital
g_s = 54
r_0 = 7.54
g_e = 0.73

g_sp = 106
r_0p = 7.61
g_ep = 0.78

g_sm = 32
r_0m = 7.46
g_em = 0.70


# Manaus
# g_s = 160
# r_0 = 10.0
# g_e = 0.6


def read_output(out_file):
    s = np.zeros([t_days, age_strata], dtype=np.float64)
    e = np.zeros([t_days, age_strata], dtype=np.float64)
    y = np.zeros([t_days, age_strata], dtype=np.float64)
    r = np.zeros([t_days, age_strata], dtype=np.float64)
    n = np.zeros([t_days, age_strata], dtype=np.float64)
    a = np.zeros([t_days, age_strata], dtype=np.float64)
    c = np.zeros([t_days, age_strata], dtype=np.float64)
    h = np.zeros([t_days, age_strata], dtype=np.float64)
    l = np.zeros([t_days, age_strata], dtype=np.float64)
    ri = np.zeros([t_days, age_strata], dtype=np.float64)
    with open(out_file, "r") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader, None)
        j = 0
        for row in spamreader:
            for i in range(age_strata):
                s[j, i] = row[compartments * (i + 1)]
                e[j, i] = row[compartments * (i + 1) + 1]
                y[j, i] = row[compartments * (i + 1) + 2]
                r[j, i] = row[compartments * (i + 1) + 3]
                n[j, i] = row[compartments * (i + 1) + 4]
                a[j, i] = row[compartments * (i + 1) + 5]
                c[j, i] = row[compartments * (i + 1) + 6]
                h[j, i] = row[compartments * (i + 1) + 7]
                l[j, i] = row[compartments * (i + 1) + 8]
            for ii in range(age_strata):
                ri[j, ii] = row[compartments * (age_strata + 1) + ii + 1]
            j = j + 1
        return s, e, y, r, n, a, c, h, l, ri


def make_plots_up(tt, var_out, nn, opt):
    arr_r = np.linspace(r_0, r_0p, nn)
    arr_gs = np.linspace(g_s, g_sp, nn)
    arr_ge = np.linspace(g_e, g_ep, nn)
    var_old = var_out
    for ii in range(0, len(arr_r)):
        subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                         str(day_next_2), str(day_next_3), '-m', '3',
                         '-I0', str(arr_gs[ii]), '-R0', str(arr_r[ii]), '-Rp', str(arr_r[ii]), '-epi', str(arr_ge[ii]),
                         '-itv', '0', '10', '10', '7'], stdout=open(os.devnull, 'wb'))
        os.chdir("..")
        subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
        subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt',
                         '/'.join(['output', output_file]), '3'], stdout=open(os.devnull, 'wb'))
        os.chdir("output")
        si, ei, yi, ri, ni, ai, ci, hi, li, rii = read_output(output_file)
        os.chdir("..")
        os.chdir("scripts")
        if opt is True:
            var = np.sum(hi, axis=1)
            plt.plot(tt, var, '-', color='lightsteelblue')
            if ii is 0:
                plt.fill_between(tt, var_old, var, facecolor='lightsteelblue', label=u'95% CI')
            else:
                plt.fill_between(tt, var_old, var, facecolor='lightsteelblue')
            var_old = var
        else:
            var = np.sum(li, axis=1)
            plt.plot(tt, var, '-', color='lightcoral')
            if ii is 0:
                plt.fill_between(tt, var_old, var, facecolor='lightcoral', label=u'95% CI')
            else:
                plt.fill_between(tt, var_old, var, facecolor='lightcoral')
            var_old = var


def make_plots_down(tt, var_out, nn, opt):
    arr_r = np.linspace(r_0m, r_0, nn)
    arr_gs = np.linspace(g_sm, g_s, nn)
    arr_ge = np.linspace(g_em, g_e, nn)
    var_old = var_out
    for ii in range(0, len(arr_r)):
        subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                         str(day_next_2), str(day_next_3), '-m', '3',
                         '-I0', str(arr_gs[-ii-1]), '-R0', str(arr_r[-ii-1]), '-Rp', str(arr_r[-ii-1]), '-epi',
                         str(arr_ge[-ii-1]), '-itv', '0', '10', '10', '7'], stdout=open(os.devnull, 'wb'))
        os.chdir("..")
        subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
        subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt',
                         '/'.join(['output', output_file]), '3'], stdout=open(os.devnull, 'wb'))
        os.chdir("output")
        si, ei, yi, ri, ni, ai, ci, hi, li, rii = read_output(output_file)
        os.chdir("..")
        os.chdir("scripts")
        if opt is True:
            var = np.sum(hi, axis=1)
            plt.plot(tt, var, '-', color='lightsteelblue')
            plt.fill_between(tt, var_old, var, facecolor='lightsteelblue')
            var_old = var
        else:
            var = np.sum(li, axis=1)
            plt.plot(tt, var, '-', color='lightcoral')
            plt.fill_between(tt, var_old, var, facecolor='lightcoral')
            var_old = var


# Fitted curve
# Supposed to open to level 3 after 31 of july
# Mean Curve
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '10', '7', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s1, e1, y1, r1, n1, a1, c1, h1, l1, ri1 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Upper limit
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_sp), '-R0', str(r_0p), '-Rp', str(r_0p), '-epi', str(g_ep),
                 '-itv', '0', '10', '10', '7', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s1p, e1p, y1p, r1p, n1p, a1p, c1p, h1p, l1p, ri1p = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Lower limit
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_sm), '-R0', str(r_0m), '-Rp', str(r_0m), '-epi', str(g_em),
                 '-itv', '0', '10', '10', '7', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s1m, e1m, y1m, r1m, n1m, a1m, c1m, h1m, l1m, ri1m = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Somam-se todas as faixas etárias

S1 = np.sum(s1, axis=1)
E1 = np.sum(e1, axis=1)
I1 = np.sum(y1, axis=1)
R1 = np.sum(r1, axis=1)
N1 = np.sum(n1, axis=1)
A1 = np.sum(a1, axis=1)
C1 = np.sum(c1, axis=1)
H1 = np.sum(h1, axis=1)
L1 = np.sum(l1, axis=1)
RI1 = np.sum(ri1, axis=1)
Ac1 = C1 + RI1 + I1

S1p = np.sum(s1p, axis=1)
E1p = np.sum(e1p, axis=1)
I1p = np.sum(y1p, axis=1)
R1p = np.sum(r1p, axis=1)
N1p = np.sum(n1p, axis=1)
A1p = np.sum(a1p, axis=1)
C1p = np.sum(c1p, axis=1)
H1p = np.sum(h1p, axis=1)
L1p = np.sum(l1p, axis=1)
RI1p = np.sum(ri1p, axis=1)
Ac1p = C1p + RI1p + I1p

S1m = np.sum(s1m, axis=1)
E1m = np.sum(e1m, axis=1)
I1m = np.sum(y1m, axis=1)
R1m = np.sum(r1m, axis=1)
N1m = np.sum(n1m, axis=1)
A1m = np.sum(a1m, axis=1)
C1m = np.sum(c1m, axis=1)
H1m = np.sum(h1m, axis=1)
L1m = np.sum(l1m, axis=1)
RI1m = np.sum(ri1m, axis=1)
Ac1m = C1m + RI1m + I1m

# Plot dos gráficos
t_array = np.linspace(0, t_days - 1, t_days, dtype=int)
tempDate = datetime.datetime(year, month, day)
t_dates = (tempDate + t_array*datetime.timedelta(days=1))

fig, ax = plt.subplots()
plt.title('Lock down until the 31 of july, then relax to level 3')
n_plots = 15
make_plots_up(t_dates, H1, n_plots, True)
make_plots_down(t_dates, H1, n_plots, True)
plt.plot(t_dates, H1, '-', color='blue', label=u'Hospitalizations')
make_plots_up(t_dates, L1, n_plots, False)
make_plots_down(t_dates, L1, n_plots, False)
plt.plot(t_dates, L1, '--', color='red', label=u'ICU demand')
plt.axhline(leitos, linestyle = '--', linewidth=1.0, color='black', label=u'Available ICUs')
plt.xlim([datetime.date(year, month, day), datetime.date(2020, 12, 31)])
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(weeks)
ax.xaxis.set_major_formatter(month_fmt)
#plt.xlabel(u'days')
plt.ylabel(u'individuals')
plt.legend(loc='upper left', fontsize='small', framealpha=0.1, fancybox=True)

fig, ax = plt.subplots()
plt.title('Lock down until the 31 of july, then relax to level 3')
plt.plot(t_dates, C1, '-', color='red', label=u'Casualties')
plt.fill_between(t_dates, C1m, C1p, facecolor='red', alpha=0.4, label=u'95% CI')
plt.xlim([datetime.date(year, month, day), datetime.date(2020, 12, 31)])
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(weeks)
ax.xaxis.set_major_formatter(month_fmt)
#plt.xlabel(u'days')
plt.ylabel(u'individuals')
plt.legend(loc='upper left', fontsize='small', framealpha=0.1, fancybox=True)

plt.show()
