# coding: utf-8
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import csv
import os
import subprocess
import datetime

# Output file - this should be fixed
output_file = 'result_data_sp_capital_explore.csv'

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

#SJC
#leitos = 280
#SP Capital
leitos = 4861
# Manaus
#leitos = 463

# São Paulo Capital
day_init = 0
day_next_1 = 25
day_next_2 = 74
day_next_3 = 151
day_mid = 125
year = 2020
month = 2
day = 26

# São José dos Campos
#day_init = 0
#day_next_1 = 21
#day_next_2 = 53
#day_next_3 = 135
#day_mid = 104

# Manaus
#day_init = 0
#day_next_1 = 9
#day_next_2 = 58
#day_next_3 = 143
#day_mid = 112


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


# Fixed post break parameters
# SJC
#g_s = 23
#r_0 = 4.71
#g_e = 0.53
# SP Capital
g_s = 54
r_0 = 7.54
g_e = 0.73
# Manaus
#g_s = 160
#r_0 = 10.0
#g_e = 0.6

# Fixed outbreak parameters
# SJC
#g_s0 = 23
#r_00 = 4.71
#g_e0 = 1.00
# SP Capital
g_s0 = 54
r_00 = 7.54
g_e0 = 1.0
#Manaus
#g_s0 = 160
#r_00 = 10.0
#g_e0 = 1.0


# First scenario
# Lock, never relax until the 31 of july
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '10', '0', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s1, e1, y1, r1, n1, a1, c1, h1, l1, ri1 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Lock, then relax to level 1 on 10 of may, then open on the 31 of july
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '9', '0', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s2, e2, y2, r2, n2, a2, c2, h2, l2, ri2 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Lock, then relax to level 2 on 10 of may, then open on the 31 of july
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '8', '0', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s3, e3, y3, r3, n3, a3, c3, h3, l3, ri3 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Lock, then relax to level 1 on 10 of may, relax to level 2 on 30 of june, then open on 31 of july
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_mid), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '9', '8', '-s', '-ex', '0', str(day_next_3)])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s4, e4, y4, r4, n4, a4, c4, h4, l4, ri4 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Lock, then simply open on 10 of may
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '0', '0', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s5, e5, y5, r5, n5, a5, c5, h5, l5, ri5 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Lock until the 31 of june, then relax to level 2 until end of the year
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s), '-R0', str(r_0), '-Rp', str(r_0), '-epi', str(g_e),
                 '-itv', '0', '10', '10', '7', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s6, e6, y6, r6, n6, a6, c6, h6, l6, ri6 = read_output(output_file)
os.chdir("..")
os.chdir("scripts")

# Do nothing, wild behaviour scenario
subprocess.call(['python', 'cenario_generator.py', '-i', cenario_folder, '-d', str(day_init), str(day_next_1),
                 str(day_next_2), str(day_next_3), '-m', '3',
                 '-I0', str(g_s0), '-R0', str(r_00), '-Rp', str(r_00), '-epi', str(g_e0),
                 '-itv', '0', '1', '1', '1', '-s'])
os.chdir("..")
subprocess.call(['bin/csv_to_input', cenario_folder], stdout=open(os.devnull, 'wb'))
subprocess.call(['bin/spatial_covid0d_estrat.exe', 'input/generated-input.txt', '/'.join(['output', output_file]),
                 '3'], stdout=open(os.devnull, 'wb'))
os.chdir("output")
s0, e0, y0, r0, n0, a0, c0, h0, l0, ri0 = read_output(output_file)
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

S2 = np.sum(s2, axis=1)
E2 = np.sum(e2, axis=1)
I2 = np.sum(y2, axis=1)
R2 = np.sum(r2, axis=1)
N2 = np.sum(n2, axis=1)
A2 = np.sum(a2, axis=1)
C2 = np.sum(c2, axis=1)
H2 = np.sum(h2, axis=1)
L2 = np.sum(l2, axis=1)
RI2 = np.sum(ri2, axis=1)
Ac2 = C2 + RI2 + I2

S3 = np.sum(s3, axis=1)
E3 = np.sum(e3, axis=1)
I3 = np.sum(y3, axis=1)
R3 = np.sum(r3, axis=1)
N3 = np.sum(n3, axis=1)
A3 = np.sum(a3, axis=1)
C3 = np.sum(c3, axis=1)
H3 = np.sum(h3, axis=1)
L3 = np.sum(l3, axis=1)
RI3 = np.sum(ri3, axis=1)
Ac3 = C3 + RI3 + I3

S4 = np.sum(s4, axis=1)
E4 = np.sum(e4, axis=1)
I4 = np.sum(y4, axis=1)
R4 = np.sum(r4, axis=1)
N4 = np.sum(n4, axis=1)
A4 = np.sum(a4, axis=1)
C4 = np.sum(c4, axis=1)
H4 = np.sum(h4, axis=1)
L4 = np.sum(l4, axis=1)
RI4 = np.sum(ri4, axis=1)
Ac4 = C4 + RI4 + I4

S5 = np.sum(s5, axis=1)
E5 = np.sum(e5, axis=1)
I5 = np.sum(y5, axis=1)
R5 = np.sum(r5, axis=1)
N5 = np.sum(n5, axis=1)
A5 = np.sum(a5, axis=1)
C5 = np.sum(c5, axis=1)
H5 = np.sum(h5, axis=1)
L5 = np.sum(l5, axis=1)
RI5 = np.sum(ri5, axis=1)
Ac5 = C5 + RI5 + I5

S6 = np.sum(s6, axis=1)
E6 = np.sum(e6, axis=1)
I6 = np.sum(y6, axis=1)
R6 = np.sum(r6, axis=1)
N6 = np.sum(n6, axis=1)
A6 = np.sum(a6, axis=1)
C6 = np.sum(c6, axis=1)
H6 = np.sum(h6, axis=1)
L6 = np.sum(l6, axis=1)
RI6 = np.sum(ri6, axis=1)
Ac6 = C6 + RI6 + I6

S0 = np.sum(s0, axis=1)
E0 = np.sum(e0, axis=1)
I0 = np.sum(y0, axis=1)
R0 = np.sum(r0, axis=1)
N0 = np.sum(n0, axis=1)
A0 = np.sum(a0, axis=1)
C0 = np.sum(c0, axis=1)
H0 = np.sum(h0, axis=1)
L0 = np.sum(l0, axis=1)
RI0 = np.sum(ri0, axis=1)
Ac0 = C0 + RI0 + I0

# Plot dos gráficos
t_array = np.linspace(0, t_days - 1, t_days, dtype=int)
tempDate = datetime.datetime(year, month, day)
t_dates = (tempDate + t_array*datetime.timedelta(days=1))
day_1 = (tempDate + day_next_1*datetime.timedelta(days=1))
day_2 = (tempDate + day_next_2*datetime.timedelta(days=1))
day_3 = (tempDate + day_next_3*datetime.timedelta(days=1))

fig, ax = plt.subplots()
plt.axvline(day_1, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_2, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_3, linestyle='--', linewidth=1.0, color='black')
plt.plot(t_dates, I1, '-', color='blue', label=u'Lock down until the 31 of july')
plt.plot(t_dates, I6, '-', color='orange', label=u'Lock down until the 31 of july, \n then relax to level 3 until the '
                                                 u'end of the year')
plt.plot(t_dates, I2, '-', color='m', label=u'Lock down until the 10 of may, level 1 until the 31 of july')
plt.plot(t_dates, I4, '-', color='y', label=u'Lock down until the 10 of may, relax to level 1 \n until the 30 of june, '
                                            u'relax to level 2 until the 31 of july')
plt.plot(t_dates, I3, '-', color='green', label=u'Lock down until the 10 of may, level 2 until the 31 of july')
plt.plot(t_dates, I5, '-', color='red', label=u'Simply open on the 10 of may')
plt.plot(t_dates, I0, '-', color='black', label=u'Do-nothing scenario')
plt.xlim([datetime.date(year, month, day), datetime.date(2020, 12, 31)])
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(weeks)
ax.xaxis.set_major_formatter(month_fmt)
plt.ylabel(u'individuals')
plt.legend(loc='upper right', fontsize='small', framealpha=0.1, fancybox=True)

fig, ax = plt.subplots()
plt.axvline(day_1, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_2, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_3, linestyle='--', linewidth=1.0, color='black')
plt.plot(t_dates, C1, '-', color='blue', label=u'Lock down until the 31 of july')
plt.plot(t_dates, C6, '-', color='orange', label=u'Lock down until the 31 of july, \n then relax to level 3 until the '
                                                 u'end of the year')
plt.plot(t_dates, C2, '-', color='m', label=u'Lock down until the 10 of may, level 1 until the 31 of july')
plt.plot(t_dates, C4, '-', color='y', label=u'Lock down until the 10 of may, relax to level 1 \n until the 30 of june, '
                                            u'relax to level 2 until the 31 of july')
plt.plot(t_dates, C3, '-', color='green', label=u'Lock down until the 10 of may, level 2 until the 31 of july')
plt.plot(t_dates, C5, '-', color='red', label=u'Simply open on the 10 of may')
plt.plot(t_dates, C0, '-', color='black', label=u'Do-nothing scenario')
plt.xlim([datetime.date(year, month, day), datetime.date(2020, 12, 31)])
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(weeks)
ax.xaxis.set_major_formatter(month_fmt)
plt.ylabel(u'individuals')
plt.legend(loc='upper left', fontsize='small', framealpha=0.1, fancybox=True)

fig, ax = plt.subplots()
plt.axvline(day_1, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_2, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_3, linestyle='--', linewidth=1.0, color='black')
plt.axhline(leitos, linestyle='--', linewidth=1.0, color='red', label=u'Leitos disponíveis')
plt.plot(t_dates, H1, '-', color='blue', label=u'Lock down until the 31 of july')
plt.plot(t_dates, H6, '-', color='orange', label=u'Lock down until the 31 of july, \n then relax to level 3 until the '
                                                 u'end of the year')
plt.plot(t_dates, H2, '-', color='m', label=u'Lock down until the 10 of may, level 1 until the 31 of july')
plt.plot(t_dates, H4, '-', color='y', label=u'Lock down until the 10 of may, relax to level 1 \n until the 30 of june, '
                                            u'relax to level 2 until the 31 of july')
plt.plot(t_dates, H3, '-', color='green', label=u'Lock down until the 10 of may, level 2 until the 31 of july')
plt.plot(t_dates, H5, '-', color='red', label=u'Simply open on the 10 of may')
plt.plot(t_dates, H0, '-', color='black', label=u'Do-nothing scenario')
plt.plot(t_dates, L1, '--', color='blue')
plt.plot(t_dates, L6, '--', color='orange')
plt.plot(t_dates, L2, '--', color='m')
plt.plot(t_dates, L4, '--', color='y')
plt.plot(t_dates, L3, '--', color='green')
plt.plot(t_dates, L5, '--', color='red')
plt.plot(t_dates, L0, '--', color='black')
plt.xlim([datetime.date(year, month, day), datetime.date(2020, 12, 31)])
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(weeks)
ax.xaxis.set_major_formatter(month_fmt)
plt.ylabel(u'individuals')
plt.legend(loc='upper right', fontsize='small', framealpha=0.1, fancybox=True)

fig, ax = plt.subplots()
plt.axvline(day_1, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_2, linestyle='--', linewidth=1.0, color='black')
plt.axvline(day_3, linestyle='--', linewidth=1.0, color='black')
plt.plot(t_dates, R1, '-', color='blue', label=u'Lock down until the 31 of july')
plt.plot(t_dates, R6, '-', color='orange', label=u'Lock down until the 31 of july, \n then relax to level 3 until the '
                                                 u'end of the year')
plt.plot(t_dates, R2, '-', color='m', label=u'Lock down until the 10 of may, level 1 until the 31 of july')
plt.plot(t_dates, R4, '-', color='y', label=u'Lock down until the 10 of may, relax to level 1 \n until the 30 of june, '
                                            u'relax to level 2 until the 31 of july')
plt.plot(t_dates, R3, '-', color='green', label=u'Lock down until the 10 of may, level 2 until the 31 of july')
plt.plot(t_dates, R5, '-', color='red', label=u'Simply open on the 10 of may')
plt.plot(t_dates, R0, '-', color='black', label=u'Do-nothing scenario')
plt.xlim([datetime.date(year, month, day), datetime.date(2020, 12, 31)])
ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(weeks)
ax.xaxis.set_major_formatter(month_fmt)
plt.ylabel(u'individuals')
plt.legend(loc='upper left', fontsize='small', framealpha=0.1, fancybox=True)

plt.show()