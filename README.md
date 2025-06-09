# restaurante-facs

Projeto de conexão Cliente-Servidor para gerenciamento de reservas em restaurante.

## Funcionalidades

- **Atendente**: Criar e cancelar reservas de mesas.
- **Garçom**: Confirmar reservas.
- **Gerente**: Gerar relatórios de reservas por período, por mesa e de mesas confirmadas.

## Estrutura

- `app.py`: API Flask principal.
- `crud.py`: Operações de banco de dados MySQL.
- `atendente.py`, `garcom.py`, `gerente.py`: Interfaces de linha de comando para cada perfil.
- `banco_restaurante.sql`: Script de criação e popularização do banco de dados.
- `Dockerfile` e `docker-compose.yml`: Para empacotamento e execução com Docker.

## Como rodar com Docker

### Pré-requisitos

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados.

### Passos

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/restaurante-facs.git
   cd restaurante-facs
   ```

2. **Inicie os containers:**
   ```sh
   docker-compose up --build
   ```

   Isso irá:
   - Subir um container MySQL com o banco já criado a partir de `banco_restaurante.sql`
   - Subir o backend Flask em outro container, acessível em [http://localhost:5000](http://localhost:5000)

3. **Acesse a aplicação:**
   - Use os scripts `atendente.py`, `garcom.py` e `gerente.py` para interagir via terminal:
     ```sh
     docker-compose exec web python atendente.py
     docker-compose exec web python garcom.py
     docker-compose exec web python gerente.py
     ```

   - Ou faça requisições HTTP para a API Flask.

4. **Parar os containers:**
   ```sh
   docker-compose down
   ```

## Observações

- O banco de dados é inicializado limpo a cada vez que o container é criado.
- Para persistência de dados, adapte o volume do serviço `db` no `docker-compose.yml`.

---
