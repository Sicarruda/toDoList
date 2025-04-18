## Resumo do Projeto
Este é um projeto de lista de tarefas (To-Do List) desenvolvido com Python e Django. Ele permite que os usuários criem, visualizem, atualizem e excluam tarefas de forma simples e eficiente.

## APIs Usadas
- **Django REST Framework**: Para a criação de APIs RESTful.
- **SQLite**: Banco de dados padrão para armazenar as tarefas.

## Estrutura do Projeto
```
toDoList/
├── manage.py
├── toDoList/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── db.sqlite3
```

## Como Iniciar o Projeto
1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/toDoList.git
    cd toDoList
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Realize as migrações do banco de dados:
    ```bash
    python manage.py migrate
    ```

5. Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

6. Acesse o projeto no navegador em: [http://127.0.0.1:8000](http://127.0.0.1:8000)