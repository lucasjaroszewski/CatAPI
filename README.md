# Cat API

Desenvolvido com o __FastAPI Framework__, o projeto trata-se da construção de uma API _(Application Programming Interface)_. Os principais recursos a serem implementados são: a manutenção do CRUD _(Create, Read, Update and Delete)_  quanto as chamadas feitas ao back-end relacionadas aos gatos; e a validação dos códigos desenvolvida com o pytest para que incosistências não ocorram.


## Como executar o projeto

A execução é feita com o auxílio do __Poetry__, um pacote do Python que descomplicou a gestão das dependências do projeto.

```bash
# Instale o Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Clone o repositório
git clone https://github.com/lucasjaroszewski/CatAPI

# Acesse a pasta criada
cd CatAPI

# Acesse o Poetry Shell
poetry shell

# Instale os requerimentos
poetry update

# Execute o servidor através do Uvicorn
uvicorn app.main:app --reload
```

## Documentação

### Métodos

```bash
# Todos métodos disponíveis em:
http://127.0.0.1:8000/docs

```

### Testes

```bash
# Para execução dos testes acesse /CatAPI/
poetry shell
poetry update
python -m pytest tests
```
