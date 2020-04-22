# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

# Leitura do arquivo de saída

t_days = 400
age_strata = 16
compartments = 11
leitos = 60000
output_file = 'result_data.csv'

# Dados de infectados atuais no Brasil
YData  = np.array([1, 1, 1, 2, 2, 2, 2, 4, 4, 13, 13, 20, 25, 31, 38, 52, 151, 151, 162, 199, 318, 367, 613, 780, 1004,
                   1519, 1888, 2199, 2493, 2902, 3319, 3787, 4114, 4300, 5389, 6469, 7593, 8570, 9788, 10439, 11470,
                   13221, 15224, 16969, 18453, 19430, 20796])
CData = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 6, 11, 15, 25, 34, 46, 59, 77, 92,
                  111, 136, 159, 201, 240, 324, 359, 445, 486, 564, 686, 819, 950, 1057, 1124, 1223, 1328, 1532, 1736])
tData = np.linspace(0, YData.size - 1, YData.size)
cData = np.linspace(0, CData.size - 1, CData.size)
YData = 10*YData

s = np.zeros([t_days, age_strata], dtype=np.float64)
e = np.zeros([t_days, age_strata], dtype=np.float64)
y = np.zeros([t_days, age_strata], dtype=np.float64)
r = np.zeros([t_days, age_strata], dtype=np.float64)
n = np.zeros([t_days, age_strata], dtype=np.float64)
a = np.zeros([t_days, age_strata], dtype=np.float64)
c = np.zeros([t_days, age_strata], dtype=np.float64)
h = np.zeros([t_days, age_strata], dtype=np.float64)
l = np.zeros([t_days, age_strata], dtype=np.float64)
t_array = np.array(t_days, dtype=np.float64)

t_array = np.linspace(0, t_days-1, t_days)

curr_dir = os.path.abspath(os.curdir)
print(u'Diretório atual ' + curr_dir)
print(u'Movendo para o diretório de saída (output) ')
os.chdir("..")
os.chdir("output")

curr_dir = os.path.abspath(os.curdir)
print(u'Diretório de saída (output) ' + curr_dir)

with open(output_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            s[j, i] = row[compartments * (i+1)]
            e[j, i] = row[compartments * (i+1) + 1]
            y[j, i] = row[compartments * (i+1) + 2]
            r[j, i] = row[compartments * (i+1) + 3]
            n[j, i] = row[compartments * (i+1) + 4]
            a[j, i] = row[compartments * (i+1) + 5]
            c[j, i] = row[compartments * (i+1) + 6]
            h[j, i] = row[compartments * (i+1) + 7]
            l[j, i] = row[compartments * (i+1) + 8]
        j = j + 1

print(u'Voltando para o diretório de script')
os.chdir("..")
os.chdir("scripts")

# Soma todas as faixas etárias

S = np.sum(s, axis=1)
E = np.sum(e, axis=1)
I = np.sum(y, axis=1)
R = np.sum(r, axis=1)
N = np.sum(n, axis=1)
A = np.sum(a, axis=1)
C = np.sum(c, axis=1)
H = np.sum(h, axis=1)
L = np.sum(l, axis=1)

# Criam-se grupos de faixa etária: 1: 0 - 20 / 2: 20 - 55 / 3: 55 ou mais

I1 = np.sum(y[:, 0:3], axis=1)
I2 = np.sum(y[:, 4:9], axis=1)
I3 = np.sum(y[:, 10:16], axis=1)

R1 = np.sum(r[:, 0:3], axis=1)
R2 = np.sum(r[:, 4:9], axis=1)
R3 = np.sum(r[:, 10:16], axis=1)

H1 = np.sum(h[:, 0:3], axis=1)
H2 = np.sum(h[:, 4:9], axis=1)
H3 = np.sum(h[:, 10:16], axis=1)

L1 = np.sum(l[:, 0:3], axis=1)
L2 = np.sum(l[:, 4:9], axis=1)
L3 = np.sum(l[:, 10:16], axis=1)

C1 = np.sum(c[:, 0:3], axis=1)
C2 = np.sum(c[:, 4:9], axis=1)
C3 = np.sum(c[:, 10:16], axis=1)

# Plota os gráficos

plt.figure(1)
plt.subplot(121)
plt.plot(t_array, S, '-', label='S')
plt.plot(t_array, I, '-', label='I')
plt.plot(t_array, R, '-', label='R')
plt.plot(t_array, C, '-', label='C')
plt.plot(t_array, H, '-', label='H')
plt.plot(t_array, L, '-', label='L')
plt.plot(t_array, N, '-', label='N')
plt.plot(t_array, E, '-', label='E')
plt.plot(t_array, A, '-', label='A')
plt.xlim([0, 0.5*t_days])
plt.xlabel(u'dias')
plt.ylabel(u'indivíduos')
plt.legend(loc='center left', shadow=True, fontsize='small')

plt.subplot(122)
plt.semilogy([0, t_days-1], [leitos, leitos], '--r', label=u'Leitos disponíveis')
plt.semilogy(t_array, S)
plt.semilogy(t_array, I)
plt.semilogy(t_array, R)
plt.semilogy(t_array, C)
plt.semilogy(t_array, H)
plt.semilogy(t_array, L)
plt.semilogy(tData, YData, 'ok')
plt.semilogy(cData, CData, 'or', label=u'Óbitos')
plt.xlim([0, 0.5*t_days])
plt.ylim([1E-01, 1.1*N.max()])
plt.xlabel('tempo (dias)')

plt.suptitle(u'Curva total das populações em compartimentos - modelo SEAIR')

plt.figure(2)
plt.subplot(121)
plt.plot(t_array, I1, '-b', label='I: 0 a 20')
plt.plot(t_array, I2, '-g', label='I: 20 a 55')
plt.plot(t_array, I3, '-r', label='I: 55 ou mais')
plt.xlim([0, 0.5*t_days])
plt.xlabel(u'dias')
plt.ylabel(u'indivíduos')
plt.legend(loc='center right', shadow=True, fontsize='small')

plt.subplot(122)
plt.semilogy(t_array, I1, '-b',  label='I: 0 a 20')
plt.semilogy(t_array, I2, '-g',  label='I: 20 a 55')
plt.semilogy(t_array, I3, '-r', label='I: 55 ou mais')
plt.semilogy(t_array, R1, '--b', label='R: 0 a 20')
plt.semilogy(t_array, R2, '--g', label='R: 20 a 55')
plt.semilogy(t_array, R3, '--r', label='R: 55 ou mais')
plt.xlabel('tempo (dias)')
plt.xlim([0, 0.5*t_days])
plt.ylim([1E-01, 1.1*N.max()])
plt.legend(loc='lower right', shadow=True, fontsize='small')

plt.suptitle(u'Infectados e recuperados por faixa etária - modelo SEAIR')

plt.figure(3)
plt.subplot(121)
plt.plot(t_array, H1, '-b', label='H: 0 a 20')
plt.plot(t_array, H2, '-g', label='H: 20 a 55')
plt.plot(t_array, H3, '-r', label='H: 55 ou mais')
plt.plot(t_array, L1, '--b', label='L: 0 a 20')
plt.plot(t_array, L2, '--g', label='L: 20 a 55')
plt.plot(t_array, L3, '--r', label='L: 55 ou mais')
plt.xlim([0, 0.5*t_days])
plt.xlabel(u'dias')
plt.ylabel(u'indivíduos')
plt.legend(loc='center right', shadow=True, fontsize='small')

plt.subplot(122)
plt.semilogy(t_array, H1, '-b', label='H: 0 a 20')
plt.semilogy(t_array, H2, '-g', label='H: 20 a 55')
plt.semilogy(t_array, H3, '-r', label='H: 55 ou mais')
plt.semilogy(t_array, L1, '--b', label='L: 0 a 20')
plt.semilogy(t_array, L2, '--g', label='L: 20 a 55')
plt.semilogy(t_array, L3, '--r', label='L: 55 ou mais')
plt.semilogy(t_array, C1, '-.b', label='C: 0 a 20')
plt.semilogy(t_array, C2, '-.g', label='C: 20 a 55')
plt.semilogy(t_array, C3, '-.r', label='C: 55 ou mais')
plt.xlabel('tempo (dias)')
plt.xlim([0, 0.5*t_days])
plt.ylim([1E-01, 1.1*I.max()])
plt.legend(loc='lower right', shadow=True, fontsize='small')

plt.suptitle(u'Estimativa de hospitalizados, leitos e óbitos por faixa etária - modelo SEAIR')

plt.show()