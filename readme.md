# Dashboard Intere

## Inteligência Territorial para Resiliência

O dashboard do projeto "Inteligência Territorial para a Resiliência: Sistematização e Integração de Indicadores para HIS no Estado de São Paulo", desenvolvido no âmbito do CONTRATO nº 033/2025, decorrente do Edital de Pesquisa do CAU SP, foi concebido para facilitar a consulta, a exploração e a visualização dos indicadores produzidos durante a pesquisa.

O projeto tem como objetivo apoiar profissionais e gestores públicos — em especial arquitetos, urbanistas e demais agentes envolvidos no planejamento territorial — na formulação e execução de políticas e ações voltadas ao fortalecimento da resiliência climática e territorial, com ênfase na Habitação de Interesse Social (HIS) e nas populações em situação de vulnerabilidade.

[Acesse](http://google.com) o projeto online.

## Instalação do ambiente para desenvolvimento

### Opção 1: Instalar usando mise + uv

O [mise](https://mise.jdx.dev) é uma ferramenta de gestão de ambientes, variáveis, e tarefas por projeto.

A vantagem de utilizar o mise em comparação com o uv ou pip, é que ele instala as ferramentas necesárias
(python3.12, uv), automaticamente gerencia o virtual environment, e controla as tarefas executadas, 
mas não há motivos para utilizar necessariamente o mise, pode utilizar diretamente o uv ou pip se não
possuir o mise instalado.

Para instalar o ambiente e dependências usando o mise, habilite o mise no diretório via:

```sh
# Habilite mise, confiando no diretório
mise trust
```

Esse comando deverá criar um `virtual environment` com python3.12 em `.venv`. Em seguida, instale 
as dependências, você pode instalar facilmente usando:

```sh
# Instala dependências
mise run install
```

Que irá invocar o uv para instalar as dependência descritas no requirements.txt

Para iniciar a aplicação, basta executar:

```sh
# Inicia a aplicação em ambiente de desenvolvimento
mise run dev
```

### Opção 2: Instalar usando uv

O [uv](https://docs.astral.sh/uv/) é uma versão rápida do pip, o substituindo de maneira transparente.

É recomendado que crie um `virtual environment` usando:

```sh
# Criar virtual environment
uv venv
```

Você pode ativá-lo usando:

```sh
# Ativar o virtual environment
# Você sempre deve ativar esse environment antes de rodar a aplicação, ou instalar dependências
source .venv/bin/activate
```

Para instalar as dependências com o uv, execute:

```sh
# Instala dependências
uv pip install -r requirements.txt
```

Para iniciar a aplicação, basta executar:

```sh
# Inicia a aplicação em ambiente de desenvolvimento
uv run app.py
```

### Opção 3: Instalar usando pip

Você também pode instalar e rodar a aplicação apenas com python e pip.

É recomendado que crie um `virtual environment` usando:

```sh
# Criar virtual environment
python3 -m venv .venv
```

Você pode ativá-lo usando:

```sh
# Ativar o virtual environment
# Você sempre deve ativar esse environment antes de rodar a aplicação, ou instalar dependências
source .venv/bin/activate
```

Para instalar as dependências com o pip, execute:

```sh
# Instala dependências
pip install -r requirements.txt
```

Para iniciar a aplicação, basta executar:

```sh
# Inicia a aplicação em ambiente de desenvolvimento
python3 app.py
```
