# COVID-19-ITA-WIN
Modelo epidemiológico estratificado baseado em compartimentos / Stratified compartment disease model 

Código fonte, configurado para copilação no Visual Studio 2015 e executável compilado no mesmo compilador, para plataforma Windows em máquinas 64bits.  

# Download

Baixe o repositório COVID-19-ITA-WIN na sua máquina. Para isso, basta clicar no
ícone verde no canto superior da página do GitHub, "Clone or download", e selecionar "download 
Zip".

# Compilação

A versão atual é fornecida com o binário compilado para computadores de arquitetura
64bits. Em tese, os binários devem funcionar em qualquer sistema Windows operando 
em uma máquina 64bits. A seguir são apresentadas as intruções para a compilação
do programa caso os executáveis fornecidos não funcionem. 

Dentro de um prompt de comando do Windows, de preferência o prompt de comando 
do visual studio 2015, acesse a pasta local onde o arquivo 
COVID-19-ITA-WIN foi descompactado:
```
CD C:\<DIRETÓRIO LOCAL>\COVID-19-ITA-WIN
```
Em seguida, entre no diretório build:
```
CD C:\<DIRETÓRIO LOCAL>\COVID-19-ITA-WIN\build
```
Para gerar o projeto a ser compilado pelo Visual Studio 2015, rode o programa 
premake5 no diretório. Para isso o programa premake5 precisa estar instalado no 
computador (link: https://premake.github.io/download.html) e o prompt de 
comando do Windows deve ser capaz indentificá-lo, estando o caminho para o executável
especificado no PATH do sistema. Para gerar os arquivos de projeto do
Visual Studio 2015, utilize o comando 
```
premake5 vs2015
```
Em seguida, no mesmo diretório, compile o programa utilizando a ferramenta
msbuild do Visual Studio 2015, digitando o comando 
```
msbuild COVID-19-ITA.sln /t:rebuild /p:configure=release 
```
Se o procedimento tiver sido bem sucedido, os executáveis csv_to_input.exe e  
spatial_covid0d_estrat.exe devem ter sido criados na pasta 
C:\\<DIRETÓRIO LOCAL>\COVID-19-ITA-WIN\bin. 

Por último, execute alguns testes para verificar se os executáveis estão 
funcionando. Vá para a pasta raiz:
```
CD ..
```
Gere o arquivo de input dos cenários, digitando o comando:
```
bin\csv_to_input.exe cenarioBR
```
Rode o programa principal, executando o comando
```
bin\spatial_covid0d_estrat.exe input\generated-input.txt output\result_data.csv 3
```
Para verificar se os resultados foram gerados corretamente, acesse a planilha de 
resultados result_data.csv na pasta C:\\<DIRETÓRIO LOCAL>\COVID-19-ITA-WIN\output

Alternativamente, rode o script de pós-processamento plot_output_SEAHIR.py no 
python 2.7
```
CD scripts
```
```
python plot_output_SEAHIR_BR.py
```
Note que uma versão do Python 2.7 precisa estar instalado na máquina, 
https://www.python.org/download/releases/2.7/, com suporte
para os pacotes numpy e matplotlib, geralmente distribuídas na versão padrão. 

# Instrução de execução

## Criando/Modificando um cenário:
Os cenários se encontram na pasta \input\cenarios. Na mesma, encontram-se as 
pastas cenarioBR, cenarioSP e cenarioSJC, correspondendo respectivamente aos 
cenarios do Brasil, do Estado de São Paulo e do município de São José dos Campos.

Cada pasta de cenário deve conter no mínimo os arquivos: 
```
demographic_data.csv 
epidemiology_data.csv 
contact_matrix_all.csv 
contact_matrix_home.csv 
contact_matrix_school.csv
contact_matrix_work.csv 
contact_matrix_other.csv  
```
O arquivo demographic_data.csv contém especificações demográficas do cenário. 
O arquivo epidemiology_data.csv contém os parâmetros epidemiológicos. Os arquivos
 contact_matrix_all.csv, contact_matrix_home.csv, contact_matrix_school.csv, 
 contact_matrix_work.csv e contact_matrix_other.csv contém as matrizes de 
 contato do país analisado. Esses arquivos podem e devem ser modificados para 
 o estudo do impacto de variações de parâmetros sobre os resultados ou para 
 introduzir parâmetros demográficos ou epidemiológicos.   
 
 O script cenario_generator.py deve ser utilizado para gerar e especificar o 
 cenário. Esse script toma alguns parâmetros de entrada para poder gerar o cenário,
 que são todos necessários para sua execução, por exemplo,   
 ```
 CD scripts
python cenario_generator -i cenarioBR -d 0 27 75 200 -m 3 -I0 50 -R0 8.0 
 ```
onde as opções tem tem os seguintes significado
 ```
 cenario_generator -i [nome do folder do cenario] -d [DIA0] [DIA1] [DIA2] [DIA3] -m [MODELO#] -I0 [INFECTADOS INICIAIS] -R0 [NÚMERO DE REPRODUÇÃO] 
 ```
Note que os dias [DIA0], [DIA1], ... etc correspondem ao início de um determinado
bloco de intervenção. Os tipos de intervenções precisam ser "hard coded", 
por enquanto, mas as matrizes especificando os casos definidos na seção 3.6 do 
relatório estão todas implementadas: basta substituí-las no script.

Na configuração padrão, temos o seguinte cenário de intervenção:
````
[DAY0] a [DAY1]: nenhuma intervenção
[DAY1] a [DAY2]: Lock down com isolamento de idoso, redução global de 20% por epi
[DAY2] a [DAY3]: Fechamento de escola, distanciamento social e isolamento de idoso, , redução global de 20% por epi
[DAY3] a [DAY4]: Redução global de 20% por epi
````

O script cenario_generator produz uma mensagem indicando se a operação foi bem
sucedida. Em caso de sucesso, os arquivos parameters.csv, beta_gama.csv e 
initial.csv serão criadas na pasta do cenário. Esses arquivos são necessários 
para a execução do código csv_to_input.exe.  

## Gerando um arquivo de input a partir de um cenário:

Para gerar o arquivo de input, é necessário voltar para o diretório principal 
```
CD ..
```
e executar
```
bin\csv_to_input [nome do cenário]
```

e.g.
```
bin\csv_to_input cenarioBR
```

## Executando a simulação:
No diretório principal, executar o seguinte comando:

```
bin\spatial_covid0d_estrat input\input_data.txt output\result_data.csv MODEL_NUMBER
```

Sendos os modelos:

| Modelo        | Número     |
|:-------------:|:----------:|
| SIR           | 0          |
| SEIR          | 1          |
| SEAIR         | 2          |
| SEAHIR-Qia    | 3          |


## Plotando resultados: 

Os resultados do modelo SEAHIR podem ser plotados utilizando o script plot_output_SEAHIR_BR.py, 
para os resultados do cenário cenarioBR. Para isso, entre novamente na pasta
scripts
```
CD scripts
```
e execute, por exemplo,
```
python plot_output_SEAHIR_BR -d 0 27 75 200 -s 50
```
onde as opções tem os seguintes significado
 ```
 plot_output_SEAHIR_BR -d [DIA0] [DIA1] [DIA2] [DIA3] -s [Fator de correção] 
 ```
A opção -s fornece o fator de correção a multiplicar as notificações oficiais, 
para corrigir o efeito das subnotificações.  

Para plotar os resultados de São Paulo e São José dos Campos, 
usar plot_output_SEAHIR_SP.py e plot_output_SEAHIR_SJC.py .

Futuramente será construído um script geral plot_output.py para plotar qualquer 
modelo dado um cenário/região qualquer.  

# Quicktest

A seguir apresentamos as instruções para a execução completa da simulação, 
desde a construção do cenário:  

````
C:\[Diretório Atual]> CD C:\[Diretório local]\COVID-19-ITA-WIN
C:\[Diretório local]\COVID-19-ITA-WIN> CD scripts
C:\[Diretório local]\COVID-19-ITA-WIN\scripts> python cenario_generator -i cenarioBR -d 0 27 75 200 -m 3 -I0 50 -R0 8.0
C:\[Diretório local]\COVID-19-ITA-WIN\scripts> CD ..
C:\[Diretório local]\COVID-19-ITA-WIN> bin\csv_to_input.exe cenarioBR
C:\[Diretório local]\COVID-19-ITA-WIN> bin\spatial_covid0d_estrat.exe input\generated-input.txt output\result_data.csv 3
C:\[Diretório local]\COVID-19-ITA-WIN> CD scripts
C:\[Diretório local]\COVID-19-ITA-WIN\scripts> python plot_output_SEAHIR_BR -d 0 27 75 200 -s 50
````