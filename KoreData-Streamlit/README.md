# Aplicação em Python/Streamlit

## Preparar o Ambiente
Para preparar o ambiente, é preciso primeiramente instalar os pacotes necessários, o que pode ser feito por meio o comando:
```
pip install -r requirements.txt
```
Opcionalmente é possível instalar os pacotes dentro de um ambiente virtual python (venv), realizando os seguintes comandos:
```
python -m venv .
./Scripts/Activate.ps1
```
Assim será ativado o ambiente python para um terminal powershell no windows, bastando utilizar em seguida o comando para instalar os pacotes necessários.

## Rodando a Aplicação
Após instalar os pacotes necessários, basta rodar o seguinte comando dentro da pasta KoreData-Streamlit/
```
streamlit run connection.py
```
As configurações do banco de dados estão no arquivo .streamlit/secrets.toml caso queira editá-las