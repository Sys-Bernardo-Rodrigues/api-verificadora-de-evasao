# API_Flask_ML
API em Flask para predição de evasão universitária

## Requisitos:

1. PostgreSQL
2. Criar um banco de dados no PostgreSQL antes de executar as etapas a seguir
3. Alterar as conexões para a url, porta e banco de dados criados

## Instalação do Python
### Windows

1. Baixe o instalador do Python em <link>python.org</link>
2. Execute o instalador. Certifique-se de marcar a opção "Add Python to PATH" antes de começar a instalação.
3. Siga as instruções de instalação na tela.

### macOS
1. Você pode instalar o Python usando o Homebrew com o comando: brew install python.
2. Se você não tem o Homebrew instalado, pode baixar o instalador do Python em python.org.

### Linux
1. O Python geralmente já está instalado por padrão no Linux. 
Para verificar, execute 
<code>python3 --version</code> ou <code>python --version no terminal</code>

2. Se não estiver instalado, você pode instalá-lo usando o gerenciador de pacotes da sua distribuição
<code>sudo apt-get install python3</code>

## Configuração do Ambiente Virtual com venv

### Instalando a venv

1. Caso você ainda não tenha o venv instalado, você pode executar:

<code>pip install virtualenv</code>

### Criando um Ambiente Virtual

1. Navegue até o diretório do seu projeto usando o terminal.
2. Execute o seguinte comando para criar um ambiente virtual:

<code> python -m venv myenv </code>
3. Isso criará um diretório myenv dentro do seu diretório atual, contendo o ambiente virtual.

### Ativando o Ambiente Virtual

#### Windows

<code>myenv\Scripts\activate</code>

#### macOS/Linux

<code>source myenv/bin/activate</code>

### Desativando o Ambiente Virtual
<code>deactivate</code>

### Instalando Dependências com requirements.txt
1. Certifique-se de que o ambiente virtual esteja ativo.
2. Execute o seguinte comando para instalar as dependências listadas em requirements.txt:

<code>pip install -r requirements.txt</code>

## Orientação para criar estrutura do banco:
1. Digite no terminal com a venv ativada:

<code>flask shell</code>

1.1. Se o comando anterior não funcionar, use:

<code>python -m flask shell</code>

2. Para criar o banco de dados execute no shell do flask:
   
<code>db.create_all()</code>

3. Para sair deste terminal:
   
<code>exit()</code>

## Salvar o modelo

1. Para salvar o modelo treinado vocês precisam importar o joblib no notebook e exportar o modelo com o método dump:

<code>

from joblib import dump

dump(modelo, 'modelo_treinado.joblib')
</code>

Lembrando que o <code>modelo</code> é o objeto treinado com a biblioteca sklearn.

## Importar o modelo

1. O nome default utilizado para o modelo treinado é rf_opt.joblib, portanto caso desejam utilizar outro nome podem alterar ele na rota de /predict

## Executar a API

1. <code> python app.py </code>

Os endpoints e dados necessários para cada etapa estão específicados no código fonte.

