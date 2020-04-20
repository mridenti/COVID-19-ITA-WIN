# coding: utf-8
import numpy as np
import csv
import os
from scipy.sparse.linalg import eigs


#### Some function definition
def symmetrize(matrix_C, PP, age_n):
    c_m = np.zeros([age_n, age_n])
    for ii in range(0, age_n):
        for jj in range(0, age_n):
            c_m[ii, jj] = 0.5*(matrix_C[ii, jj] * PP[ii] / PP[jj] + matrix_C[jj, ii] * PP[jj] / PP[ii])
    return c_m


##### Variable parameters, for error estimation within reasonable bounds
I_0 = 50.0  # Total initial infected individuals
R0 = 8.0  # Reproduction number
#####
##### Model Flag
# 0: SIR
# 1: SEIR
# 2: SEAIR
# 3: SEAHIR
model = 3

age_strata = 16
t_days = 400
input_folder = 'cenarioSP'
demographic_file = 'demographic_data.csv'
epidemiologic_file = 'epidemiology_data.csv'
contact_matrix_all_file = 'contact_matrix_all.csv'
contact_matrix_home_file = 'contact_matrix_home.csv'
contact_matrix_work_file = 'contact_matrix_work.csv'
contact_matrix_school_file = 'contact_matrix_school.csv'
contact_matrix_other_file = 'contact_matrix_other.csv'

matrix_all = np.zeros([age_strata, age_strata], dtype=np.float64)
matrix_home = np.zeros([age_strata, age_strata], dtype=np.float64)
matrix_work = np.zeros([age_strata, age_strata], dtype=np.float64)
matrix_school = np.zeros([age_strata, age_strata], dtype=np.float64)
matrix_other = np.zeros([age_strata, age_strata], dtype=np.float64)

demog_variables = 3
data_demog = np.zeros([demog_variables, age_strata], dtype=np.float64)
pop = np.zeros(age_strata, dtype=np.float64)
mortalidade = np.zeros(age_strata, dtype=np.float64)
natalidade = np.zeros(age_strata, dtype=np.float64)

epid_variables = 11
data_epid = np.zeros([epid_variables, age_strata], dtype=np.float64)
TC = np.zeros(age_strata, dtype=np.float64)
phi = np.zeros(age_strata, dtype=np.float64)
xI = np.zeros(age_strata, dtype=np.float64)
xA = np.zeros(age_strata, dtype=np.float64)
dI = np.zeros(age_strata, dtype=np.float64)
dL = np.zeros(age_strata, dtype=np.float64)
dH = np.zeros(age_strata, dtype=np.float64)
dA = np.zeros(age_strata, dtype=np.float64)
eta = np.zeros(age_strata, dtype=np.float64)
pho = np.zeros(age_strata, dtype=np.float64)
alpha = np.zeros(age_strata, dtype=np.float64)
tlc = np.zeros(age_strata, dtype=np.float64)

curr_dir = os.path.abspath(os.curdir)
print(u'Diretório atual ' + curr_dir)
print(u'Movendo para o diretório de entrada (input) ')
os.chdir("..")
os.chdir(os.path.join('input', 'cenarios', input_folder))

curr_dir = os.path.abspath(os.curdir)
print(u'Diretório de entrada (input) ' + curr_dir)

# Read demographic data
with open(demographic_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            data_demog[j, i] = row[i + 1]
        j = j + 1

pop = data_demog[0, :]
mortalidade = data_demog[1, :] / (365 * 1000)
natalidade = data_demog[2, :]

# Read epidemiologic data
with open(epidemiologic_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            data_epid[j, i] = row[i + 1]
        j = j + 1

# Read contact matrices
# All
with open(contact_matrix_all_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            matrix_all[j, i] = row[i]
        j = j + 1

# Home
with open(contact_matrix_home_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            matrix_home[j, i] = row[i]
        j = j + 1

# Work
with open(contact_matrix_work_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            matrix_work[j, i] = row[i]
        j = j + 1

# School
with open(contact_matrix_school_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            matrix_school[j, i] = row[i]
        j = j + 1

# Other
with open(contact_matrix_other_file, "r") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    j = 0
    for row in spamreader:
        for i in range(age_strata):
            matrix_other[j, i] = row[i]
        j = j + 1

TC = data_epid[0, :]
phi = data_epid[1, :]
xI = data_epid[2, :]
xA = data_epid[3, :]
dI = data_epid[4, :]
dL = data_epid[5, :]
dH = data_epid[6, :]
dA = data_epid[7, :]
eta = data_epid[8, :]
rho = data_epid[9, :]
alpha = data_epid[10, :]

# calcula os valores de 'a' e gama's e mu_cov

a = 1 - np.exp(-np.divide(1, dL))
gamma = 1 - np.exp(-np.divide(1, dI))
gamma_RI = 1 - np.exp(-np.divide(1, dI))
gamma_RA = 1 - np.exp(-np.divide(1, dI))
gamma_RQI = 1 - np.exp(-np.divide(1, dI))
gamma_RQA = 1 - np.exp(-np.divide(1, dI))
gamma_HR = 1 - np.exp(-np.divide(1, dA))
gamma_H = np.divide(np.multiply(gamma_RI, phi), 1 - phi)
gamma_HQI = np.divide(np.multiply(gamma_RQI, phi), 1 - phi)
gamma_QI = np.divide(np.multiply(xI, gamma_H + gamma_RI), (1 - xI))
gamma_QA = np.divide(np.multiply(xA, gamma_RA), (1 - xA))
tlc = np.divide(TC, phi)
if model == 3:
    mu_cov = np.divide(np.multiply(gamma, tlc), 1 - tlc)
else:
    mu_cov = np.divide(np.multiply(gamma, TC), 1 - TC)

# cria arquivo initial.csv

rel_pop = np.divide(pop, np.sum(pop))  # partitioning of the cases, for I0 > age_strata
I_0_vec = np.zeros(pop.size)
I_0_vec[13] = I_0

with open('initial.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(np.concatenate((['POPULATION_S'], pop)))
    spamwriter.writerow(np.concatenate((['EXPOSED_E'], I_0 * R0 * rel_pop)))
    spamwriter.writerow(np.concatenate((['ASYMPTOMATIC_A'], I_0_vec)))
    spamwriter.writerow(np.concatenate((['INFECTED_I'], I_0_vec)))
    spamwriter.writerow(np.concatenate((['RECOVERED_R'], np.zeros(pop.size))))
    spamwriter.writerow(np.concatenate((['RECOVERED_SYMPTOMATIC_Ri'], np.zeros(pop.size))))
# cria arquivo parameters.csv

param_header = ['VARIAVEL', 'FAIXA_1', 'FAIXA_2', 'FAIXA_3', 'FAIXA_4', 'FAIXA_5', 'FAIXA_6', 'FAIXA_7', 'FAIXA_8',
                'FAIXA_9', 'FAIXA_10', 'FAIXA_11', 'FAIXA_12', 'FAIXA_13', 'FAIXA_14', 'FAIXA_15', 'FAIXA_16']

with open('parameters.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(param_header)
    spamwriter.writerow(np.concatenate((['LAMBDA'], natalidade)))
    spamwriter.writerow(np.concatenate((['MORT_EQ'], mortalidade)))
    spamwriter.writerow(np.concatenate((['MORT_COV'], mu_cov)))
    spamwriter.writerow(np.concatenate((['ALPHA'], alpha)))
    spamwriter.writerow(np.concatenate((['RHO'], rho)))
    spamwriter.writerow(np.concatenate((['PHI'], phi)))
    spamwriter.writerow(np.concatenate((['ETA'], eta)))
    spamwriter.writerow(np.concatenate((['A'], a)))
    spamwriter.writerow(np.concatenate((['GAMA_H'], gamma_H)))
    spamwriter.writerow(np.concatenate((['GAMA_HR'], gamma_HR)))
    spamwriter.writerow(np.concatenate((['GAMA_RI'], gamma_RI)))
    spamwriter.writerow(np.concatenate((['GAMA_RA'], gamma_RA)))
    spamwriter.writerow(np.concatenate((['GAMA_RQI'], gamma_RQI)))
    spamwriter.writerow(np.concatenate((['GAMA_RQA'], gamma_RQA)))
    spamwriter.writerow(np.concatenate((['GAMA_HQI'], gamma_HQI)))
    spamwriter.writerow(np.concatenate((['GAMA_QI'], gamma_QI)))
    spamwriter.writerow(np.concatenate((['GAMA_QA'], gamma_QA)))
    spamwriter.writerow(np.concatenate((['TLC'], tlc)))

# cria arquivos beta_gama.csv

# Escala a matriz de contato pelo perfil demográfico e escalona a mesma pelo auto-valor dominante

P = np.outer(pop, np.divide(1, pop))
# C_sym_all = 0.5*(np.dot(np.transpose(P), matrix_all) + np.dot(np.transpose(matrix_all), P))
C_sym_home = 0.5 * (matrix_home + symmetrize(matrix_home, pop, age_strata))
C_sym_school = 0.5 * (matrix_school + symmetrize(matrix_school, pop, age_strata))
C_sym_work = 0.5 * (matrix_work + symmetrize(matrix_work, pop, age_strata))
C_sym_other = 0.5 * (matrix_other + symmetrize(matrix_other, pop, age_strata))
C_sym = C_sym_home + C_sym_work + C_sym_school + C_sym_other
for i in range(0, age_strata):
    for j in range(0, age_strata):
        C_sym[i, j] = C_sym[i, j] * pop[i] / pop[j]
        C_sym_home[i, j] = C_sym_home[i, j] * pop[i] / pop[j]
        C_sym_school[i, j] = C_sym_school[i, j] * pop[i] / pop[j]
        C_sym_work[i, j] = C_sym_work[i, j] * pop[i] / pop[j]
        C_sym_other[i, j] = C_sym_other[i, j] * pop[i] / pop[j]
w, v = eigs(C_sym)
# Main eigenvector is normalized, norm_vec = 1. Mean square_vec=1/age_strata
#print(w.max())
#eig_vec = v[:, 0]
#print(v[:, 0])
#norm_vec = np.dot(eig_vec, eig_vec)
#square_vec = np.multiply(eig_vec, eig_vec)
#print(np.mean(norm_vec), 1./16.)
eig_value = np.real(w.max())
if model == 2 or 3:
    beta = R0 * gamma[0] / (rho.max() + np.mean(alpha) * (1 - rho.max())) / eig_value
    beta_val = R0 * gamma[0] / (rho.max() + np.mean(alpha) * (1 - rho.max()))
else:
    beta = R0 * gamma[0]
C_all_pre = beta * C_sym * age_strata
C_home_pre = beta * C_sym_home * age_strata
C_work_pre = beta * C_sym_work * age_strata
C_school_pre = beta * C_sym_school * age_strata
C_other_pre = beta * C_sym_other * age_strata

R0_post = R0
if model == 2 or model == 3:
    beta = R0_post * gamma[0] / (rho.max() + np.mean(alpha) * (1 - rho.max())) / eig_value
    beta_val = R0_post * gamma[0] / (rho.max() + np.mean(alpha) * (1 - rho.max()))
else:
    beta = R0 * gamma[0]
epi_f = 0.8 # protection decrease of transmission probability
C_home_post = epi_f * beta * C_sym_home * age_strata
C_work_post = epi_f * beta * C_sym_work * age_strata
C_school_post = epi_f * beta * C_sym_school * age_strata
C_other_post = epi_f * beta * C_sym_other * age_strata
C_all_post = C_home_post + C_work_post + C_school_post + C_other_post

# Build matrix for scenarios
I_old = np.diag(np.ones(age_strata))
A_home = np.diag(np.ones(age_strata))
B_other = np.diag(np.ones(age_strata))
B_school = np.diag(np.ones(age_strata))
B_lock = np.diag(np.ones(age_strata))
W_work = np.diag(np.ones(age_strata))
W_lock = np.diag(np.ones(age_strata))
for i in range(age_strata - 5, age_strata):
    I_old[i, i] = 0.1
for i in range(0, 4):
    A_home[i, i] = 1.5
for i in range(4, age_strata):
    A_home[i, i] = 1.1
for i in range(0, 4):
    B_school[i, i] = 0.4
for i in range(0, 4):
    B_other[i, i] = 0.4
for i in range(4, age_strata):
    B_other[i, i] = 0.6
for i in range(0, 4):
    B_lock[i, i] = 0.2
for i in range(4, age_strata):
    B_lock[i, i] = 0.3
for i in range(0, age_strata):
    W_work[i, i] = 0.5
for i in range(0, age_strata):
    W_lock[i, i] = 0.3

# Fechamento de escolas apenas
C_all_school = np.dot(A_home, C_home_post) + C_work_post + np.dot(B_school, C_other_post)

# Fechamento de escolas e distanciamento social
C_all_school_other = np.dot(A_home, C_home_post) + C_work_post + + np.dot(B_other, C_other_post)

# Fechamento de escolas, distanciamento social e trabalho
C_all_school_other_work = np.dot(A_home, C_home_post) + np.dot(W_work, C_work_post) + np.dot(B_other, C_other_post)

# Lockdown sem isolamento de idoso
C_all_lock = np.dot(A_home, C_home_post) + np.dot(W_lock, C_work_post) + np.dot(B_lock, C_other_post)

C_work_old = np.dot(np.dot(I_old, C_work_post), I_old)
C_school_old = np.dot(np.dot(I_old, C_school_post), I_old)
C_other_old = np.dot(np.dot(I_old, C_other_post), I_old)
# Isolamento dos idosos em, com redução de X% dos seus contatos
C_all_old = C_home_post + C_work_old + C_school_old + C_other_old

# Isolamento dos idosos, fechamento de escolas
C_all_old_school = np.dot(A_home, C_home_post) + C_work_old + np.dot(B_school, C_other_old)

# Isolamento dos idosos, fechamento de escolas e distanciamento social
C_all_old_school_other = np.dot(A_home, C_home_post) + C_work_old + np.dot(B_other, C_other_old)

# Isolamento dos idosos, fechamento de escolas, distanciamento social e distanciamento no trabalho
C_all_old_school_other_work = np.dot(A_home, C_home_post) + np.dot(W_work, C_work_old) + np.dot(B_other, C_other_old)

# Lockdown com isolamento de idoso
C_all_old_lock = np.dot(A_home, C_home_post) + np.dot(W_lock, C_work_old) + np.dot(B_lock, C_other_old)

# Matrix sem intervenção desde o instante zero

beta_gama_header = ['DAY', 'GAMA_F1', 'GAMA_F2', 'GAMA_F3', 'GAMA_F4', 'GAMA_F5', 'GAMA_F6', 'GAMA_F7', 'GAMA_F8',
                    'GAMA_F9',
                    'GAMA_F10', 'GAMA_F11', 'GAMA_F12', 'GAMA_F13', 'GAMA_F14', 'GAMA_F15', 'GAMA_F16',
                    'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX',
                    'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX',
                    'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX', 'BETA_MATRIX']
space_16 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

day_init = 0
day_next_1 = 24
day_next_2 = 75
day_next_3 = 200
with open('beta_gama.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(beta_gama_header)
    for i in range(0, age_strata):
        if i == 0:
            spamwriter.writerow(np.concatenate(([day_init], gamma, C_all_pre[i, :])))
        else:
            spamwriter.writerow(np.concatenate(([day_init], space_16, C_all_pre[i, :])))
    spamwriter.writerow(np.concatenate(([''], space_16, space_16)))
    for i in range(0, age_strata):
        if i == 0:
            spamwriter.writerow(np.concatenate(([day_next_1], gamma, C_all_old_lock[i, :])))
        else:
            spamwriter.writerow(np.concatenate(([day_next_1], space_16, C_all_old_lock[i, :])))
    spamwriter.writerow(np.concatenate(([''], space_16, space_16)))
    for i in range(0, age_strata):
        if i == 0:
            spamwriter.writerow(np.concatenate(([day_next_2], gamma, C_all_old_school_other[i, :])))
        else:
            spamwriter.writerow(np.concatenate(([day_next_2], space_16, C_all_old_school_other[i, :])))
    spamwriter.writerow(np.concatenate(([''], space_16, space_16)))
    for i in range(0, age_strata):
        if i == 0:
            spamwriter.writerow(np.concatenate(([day_next_3], gamma, C_all_post[i, :]/epi_f)))
        else:
            spamwriter.writerow(np.concatenate(([day_next_3], space_16, C_all_post[i, :]/epi_f)))

print(u'Voltando para o diretório de script')
os.chdir("..")
os.chdir("..")
os.chdir("..")
os.chdir("scripts")
