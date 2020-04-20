# COVID-19-ITA

## Compilação:
Para compilar o projeto, será necessário ter a ferramenta `premake` instalada em sua máquina. Em seguida entre na pasta build e realize a compilação do projeto.

```
cd build/
premake4 gmake
make
```

Os executáveis se encontraram no diretório `bin/`.

## Criando/Modificando um cenário:
Copie os arquivos da pasta `input/cenarios/default` para uma pasta no mesmo diretorio com o nome desejado para o cenário (e.g. `input/cenarios/lockdown` para um cenário chamado lockdown).
Altere os arquivos `.csv` do cenário utilizando um software de planilhas.

## Gerando um arquivo de input a partir de um cenário:
```
bin/csv_to_input [nome do cenário]
```

e.g.
```
bin/csv_to_input lockdown
```


## Executando a simulação:

```
bin/spatial_covid0d_estrat input/input_data.txt output/result_data.csv MODEL_NUMBER
```

Sendos os modelos:

| Modelo        | Número     |
|:-------------:|:----------:|
| SIR           | 0          |
| SEIR          | 1          |
| SEAIR         | 2          |
| SEAHIR-Qia    | 3          |


## Plotando resultados:
Para visualizar resultados utilizando o `gnuplot`:
```
gnuplot scripts/plot.gp
```