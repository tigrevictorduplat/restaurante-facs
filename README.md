# restaurante-facs

Projeto de conexão Cliente-Servidor para gerenciamento de reservas em restaurante.

---

## 👤 Para Usuários: Instalação e Uso

### Funcionalidades

- **Atendente**: Criar e cancelar reservas de mesas.
- **Garçom**: Confirmar reservas.
- **Gerente**: Gerar relatórios de reservas por período, por mesa e de mesas confirmadas.

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando.

> **Observação para Windows:**  
> Certifique-se de que a virtualização está ativada na BIOS do seu computador para que o Docker funcione corretamente.  
> Procure no YouTube por "como ativar virtualização BIOS [marca do seu computador]" caso tenha dúvidas.

---

### Passo a passo para rodar o sistema

1. **Baixe o projeto**

   Abra o terminal (Prompt de Comando, PowerShell ou Terminal do VS Code) e execute:

   ```sh
   git clone https://github.com/seu-usuario/restaurante-facs.git
   cd restaurante-facs
   ```

2. **Inicie a aplicação**

   No terminal, execute:

   ```sh
   docker-compose up --build
   ```

   O Docker irá:
   - Baixar e iniciar um container MySQL, criando o banco de dados automaticamente.
   - Iniciar a API Flask, disponível em [http://localhost:5000](http://localhost:5000).

   > **Atenção:** Não abra o XAMPP nem o MySQL local. O Docker já cuida de tudo!

3. **Usando a aplicação**

   Existem duas formas de usar o sistema:

   - **Via terminal interativo (recomendado para iniciantes):**

     Para acessar os menus de Atendente, Garçom ou Gerente, use os comandos abaixo em um novo terminal:

     ```sh
     docker-compose exec web python atendente.py
     docker-compose exec web python garcom.py
     docker-compose exec web python gerente.py
     ```

     Siga as instruções que aparecerem na tela.

   - **Via API HTTP (avançado):**

     Você pode usar ferramentas como Postman, Insomnia ou até mesmo o navegador para fazer requisições HTTP para [http://localhost:5000](http://localhost:5000).

4. **Parar a aplicação**

   Para desligar tudo, pressione `CTRL+C` no terminal onde rodou o Docker, depois execute:

   ```sh
   docker-compose down
   ```

---

### Dicas e Solução de Problemas

- **Erro de input() no Docker:**  
  Sempre use `docker-compose exec web python atendente.py` (ou `garcom.py`, `gerente.py`) para rodar scripts interativos. Não tente rodar esses scripts diretamente com `docker-compose up`.

- **Portas ocupadas:**  
  Se a porta 3306 (MySQL) ou 5000 (Flask) já estiverem em uso, feche outros programas que possam estar usando essas portas (como XAMPP ou MySQL Workbench).

- **Banco de dados limpo:**  
  O banco é recriado toda vez que o container é iniciado do zero. Para manter os dados entre execuções, adapte o volume do serviço `db` no `docker-compose.yml`.

---

## 👩‍💻 Para Colaboradores/Desenvolvedores

### Estrutura dos Arquivos

- `server.py`: API Flask principal (backend HTTP).
- `crud.py`: Operações de banco de dados MySQL.
- `atendente.py`, `garcom.py`, `gerente.py`: Interfaces de linha de comando para cada perfil.
- `banco_restaurante.sql`: Script de criação e popularização do banco de dados.
- `Dockerfile` e `docker-compose.yml`: Para empacotamento e execução com Docker.
- `requirements.txt`: Lista de dependências Python.

### Atualizando a aplicação

Se atualizar algum arquivo do projeto (código, dependências, scripts SQL), rode:

```sh
docker-compose down
docker-compose up --build
```

O parâmetro `--build` garante que o Docker irá reconstruir a imagem com as alterações feitas no seu projeto.

### Boas práticas para desenvolvimento

- Sempre teste suas alterações localmente usando Docker antes de enviar para o repositório.
- Se adicionar novas dependências Python, lembre-se de atualizar o `requirements.txt`:
  ```sh
  pip freeze > requirements.txt
  ```
- Prefira usar variáveis de ambiente para credenciais e configurações sensíveis.
- Documente suas alterações no código e, se possível, atualize este README.

---

Se tiver dúvidas, procure por "Como instalar o Docker Desktop" no YouTube ou consulte a documentação oficial do Docker.

---
