# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
import os

##### Process command line options
##### Variable parameters, for error estimation within reasonable bounds
parser = argparse.ArgumentParser(description=u'This script plots the results for Manaus.')
parser.add_argument('-d', '--day', type=int, nargs=4, help='Days of measure beginning - four values required ',
                    required=True)
parser.add_argument('-s', '--scale_factor', type=float, help='Scale factor accounting for under notification ',
                    required=True)
args = parser.parse_args()

## show values ##
print ("Days: %s" % args.day)
print ("Scale factor accounting for under notification: %s" % args.scale_factor)

s_0 = float(args.scale_factor)

# Limite entre cenários
day_init = int(args.day[0])
day_next_1 = int(args.day[1])
day_next_2 = int(args.day[2])
day_next_3 = int(args.day[3])

t_days = 400
age_strata = 16
compartments = 11
leitos = 463
output_file = 'result_data.csv'

# Dados de infectados atuais em Manaus
YData = np.array([2, 2, 3, 7, 11, 25, 31, 45, 52, 63, 75, 105, 131, 140, 159, 179, 205, 232, 283, 379, 473, 560, 712,
                  800, 863, 932, 1053, 1106, 1295, 1350, 1459, 1531, 1593, 1664, 1772, 1809, 1958, 2286, 2481])

CData = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 5, 9, 11, 15, 19, 25, 33, 42, 45, 51, 60, 81, 92,
                  107, 127, 134, 155, 156, 163, 172, 193, 207])


tData = np.linspace(0, YData.size - 1, YData.size)
cData = np.linspace(0, CData.size - 1, CData.size)
YData = s_0*YData

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
t_array = np.array(t_days, dtype=np.float64)

t_array = np.linspace(0, t_days-1, t_days)

# Leitura dos arquivos de dados fundamentais
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
        for ii in range(age_strata):
            ri[j, ii] = row[compartments*(age_strata+1) + ii+1]
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
RI = np.sum(ri, axis=1)
Ac = C + RI + I

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
plt.plot(t_array, Ac, '-', label='Ac')
plt.plot(t_array, N, '-', label='N')
plt.plot(t_array, E, '-', label='E')
plt.plot(t_array, A, '-', label='A')
plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='red')
plt.axvspan(day_next_2, day_next_3, alpha=0.1, color='blue')
#plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='black')
plt.xlim([0, 0.7*t_days])
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
plt.semilogy(t_array, Ac)
plt.semilogy(tData, YData, 'ok')
plt.semilogy(cData, CData, 'or', label=u'Óbitos')
plt.xlim([0, 0.7*t_days])
plt.ylim([1, 1.1*N.max()])
plt.xlabel('tempo (dias)')
plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='red')
plt.axvspan(day_next_2, day_next_3, alpha=0.1, color='blue')
#plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='black')
max_H = np.max(H)
max_L = np.max(L)
max_I = np.max(I)
max_C = np.max(C)
t_max_I = t_array[np.where(I == max_I)]
t_max_L = t_array[np.where(L == max_L)]
if np.max(L) > leitos:
    t_colap = np.min(t_array[np.where(L > leitos)])
    textstr = '\n'.join([r'$Max(H)=%.2e$' % (max_H,), r'$Max(L)=%.2e$' % (max_L,), r'$Max(I)=%.2e$' % (max_I,),
                         r'$t(max(I))=%.f$ dias' % (t_max_I,),
                         r'$t(max(L))=%.f$ dias' % (t_max_L,),
                         r'$t(colapso)=%.f$ dias' % (t_colap,),
                         r'Obitos estimados $=%.2e$' % (max_C,),
                         'dia zero: 13/03'])
else:
    textstr = '\n'.join([r'$Max(H)=%.2e$' % (max_H,), r'$Max(L)=%.2e$' % (max_L,), r'$Max(I)=%.2e$' % (max_I,),
                         r'$t(max(I))=%.f$ dias' % (t_max_I,),
                         r'$t(max(L))=%.f$ dias' % (t_max_L,),
                         r'$t(colapso)=$inf ',
                         r'Obitos estimados $=%.2e$' % (max_C,),
                         'dia zero: 13/03'])

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
plt.text(0.5, 0.2, textstr, transform=plt.gca().transAxes, fontsize='small', verticalalignment='center', bbox=props)

plt.suptitle(u'Curva total das populações em compartimentos, Manaus - modelo SEAHIR')

plt.figure(2)
plt.subplot(121)
plt.plot(t_array, I1, '-b', label='I: 0 a 20')
plt.plot(t_array, I2, '-g', label='I: 20 a 55')
plt.plot(t_array, I3, '-r', label='I: 55 ou mais')
plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='red')
plt.axvspan(day_next_2, day_next_3, alpha=0.1, color='blue')
#plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='black')
plt.xlim([0, 0.7*t_days])
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
plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='red')
plt.axvspan(day_next_2, day_next_3, alpha=0.1, color='blue')
#plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='black')
plt.xlabel('tempo (dias)')
plt.xlim([0, 0.7*t_days])
plt.ylim([1, 1.1*N.max()])
plt.legend(loc='lower right', shadow=True, fontsize='small')

plt.suptitle(u'Infectados e recuperados por faixa etária, Manaus - modelo SEAHIR')

plt.figure(3)
plt.subplot(121)
plt.plot(t_array, H1, '-b', label='H: 0 a 20')
plt.plot(t_array, H2, '-g', label='H: 20 a 55')
plt.plot(t_array, H3, '-r', label='H: 55 ou mais')
plt.plot(t_array, L1, '--b', label='L: 0 a 20')
plt.plot(t_array, L2, '--g', label='L: 20 a 55')
plt.plot(t_array, L3, '--r', label='L: 55 ou mais')
plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='red')
plt.axvspan(day_next_2, day_next_3, alpha=0.1, color='blue')
#plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='black')
plt.xlim([0, 0.7*t_days])
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
plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='red')
plt.axvspan(day_next_2, day_next_3, alpha=0.1, color='blue')
#plt.axvspan(day_next_1, day_next_2, alpha=0.1, color='black')
plt.xlabel('tempo (dias)')
plt.xlim([0, 0.7*t_days])
plt.ylim([1, 1.1*I.max()])
plt.legend(loc='lower right', shadow=True, fontsize='small')

plt.suptitle(u'Estimativa de hospitalizados, leitos e óbitos por faixa etária, Manaus - modelo SEAHIR')

plt.show()