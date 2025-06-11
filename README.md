# 🍽️ Sistema de Gerenciamento de Reservas de Restaurante | restaurante-facs

Este é um sistema completo para simular e gerenciar o processo de reservas em um restaurante fictício. Ele oferece uma API HTTP robusta para interação e interfaces de linha de comando para diferentes perfis de usuário (Atendente, Garçom, Gerente), tudo empacotado para fácil execução com Docker.

## 👥 Integrantes

- **Celso Argolo** - 12724148715
- **Mateus Guirra** - 12724135176
- **Victor Duplat Tigre** - 12724117641
- **Victor Leôncio** - 12724128419
- **Pedro Henrique Fernandes Santos** - 12724141308
- **Felipe Borges dos Santos** - 12724148878

## ✨ Visão Geral do Projeto

O objetivo principal deste projeto é demonstrar uma arquitetura de aplicação em três camadas:

1.  **Interface do Usuário (Cliente):** Scripts de terminal interativos (`atendente.py`, `garcom.py`, `gerente.py`) que simulam as ações diárias dos funcionários do restaurante.
2.  **Lógica de Negócios (API/Servidor):** Uma API RESTful desenvolvida com Flask que processa as requisições dos clientes, aplica as regras de negócio do restaurante (como validação de datas, horários e disponibilidade de mesas) e interage com o banco de dados.
3.  **Armazenamento de Dados (Banco de Dados):** Um banco de dados MySQL que persiste todas as informações de reservas e mesas.

Toda a infraestrutura é orquestrada via **Docker**, proporcionando um ambiente de desenvolvimento e execução consistente e isolado, sem a necessidade de instalações manuais complexas de bancos de dados ou dependências.

## 🚀 Funcionalidades Principais

Este sistema permite que os usuários realizem as seguintes operações através de seus respectivos perfis:

* **Atendente:**
    * Criar novas reservas, com validações de data (passado, dias de funcionamento), horário (passado, expediente do restaurante), capacidade de pessoas, e disponibilidade da mesa (se já está reservada ou não).
    * Cancelar reservas existentes.
* **Garçom:**
    * Confirmar reservas, indicando que o cliente compareceu e liberando a mesa para futuras reservas.
* **Gerente:**
    * Gerar relatórios detalhados de reservas atendidas e não atendidas em um período específico.
    * Consultar todas as reservas feitas para uma mesa específica.
    * Visualizar a relação de mesas que tiveram reservas confirmadas.

## 💡 Por Que Flask e Comunicação via API?

A escolha da arquitetura e das tecnologias foi estratégica para simular um ambiente de aplicação moderno e escalável:

* **Flask (Python Web Framework):**
    * **Simplicidade e Leveza:** Flask é um microframework, ideal para construir APIs de forma rápida e com pouca sobrecarga. Ele nos permite focar diretamente na lógica da API sem a complexidade de frameworks maiores.
    * **Flexibilidade:** Permite definir rotas e manipular requisições HTTP de forma direta e intuitiva, sendo perfeito para uma API RESTful.
    * **Ecossistema Python:** Integra-se facilmente com o restante do código Python (como o módulo `crud.py` e os scripts clientes) e aproveita a vasta gama de bibliotecas Python.

* **Comunicação via API HTTP (RESTful):**
    * **Padrão da Indústria:** APIs HTTP RESTful são o padrão de facto para comunicação entre sistemas na web. Elas são amplamente compreendidas, fáceis de usar e depurar.
    * **Desacoplamento:** Permite que o frontend (nossos scripts de terminal, mas que também poderia ser uma interface web ou mobile) seja completamente independente do backend. As duas partes podem ser desenvolvidas por equipes diferentes, em linguagens diferentes, desde que sigam o contrato da API.
    * **Escalabilidade:** Facilita a expansão. Se no futuro o restaurante precisasse de um aplicativo móvel, um sistema de autoatendimento, ou integrar-se com parceiros, a mesma API pode ser reutilizada.
    * **Contras de Outras Abordagens:**
        * **gRPC:** Embora mais performático e ideal para microsserviços internos com comunicação de alta velocidade, gRPC adicionaria uma camada extra de complexidade (definição de Protobuf, compilação de stubs) que não é necessária para a escala e o propósito deste projeto de demonstração.
        * **Sockets/WebSockets:** Sockets oferecem comunicação de baixo nível e seriam adequados para cenários de comunicação em tempo real (ex: chat, jogos). No entanto, para requisições de "solicitação-resposta" típicas de operações de CRUD em um sistema de reservas, o modelo stateless da API HTTP é mais apropriado e mais simples de implementar e escalar.

---

## 👤 Para Usuários: Instalação e Uso

### Pré-requisitos

- [**Git**](https://git-scm.com/) instalado em sua máquina ou fazer o download diretamente do .zip do repositório.
-   [**Docker Desktop**](https://www.docker.com/products/docker-desktop/) instalado e rodando em sua máquina.

> **Observação para Windows:**
> Certifique-se de que a virtualização está ativada na BIOS do seu computador para que o Docker funcione corretamente. Procure no YouTube por "como ativar virtualização BIOS [marca do seu computador]" caso tenha dúvidas.
>
> **Importante:** Este projeto é projetado para rodar com Docker. Você *não* precisa instalar MySQL, Python ou configurar um servidor web (como XAMPP) manualmente. O Docker cuida de todo o ambiente!

### Passo a passo para rodar o sistema

1.  **Baixe o projeto**

    Abra o terminal (Prompt de Comando, PowerShell, Terminal do VS Code ou Git Bash) e execute:

    ```sh
    git clone [https://github.com/seu-usuario/restaurante-facs.git](https://github.com/seu-usuario/restaurante-facs.git)
    cd restaurante-facs
    ```

2.  **Inicie a aplicação**

    No terminal, a partir do diretório `restaurante-facs`, execute:

    ```sh
    docker-compose up --build
    ```

    O Docker irá orquestrar o seguinte:
    * **Serviço `db`:** Baixará/construirá uma imagem MySQL, criará um container, configurará o banco de dados `banco_restaurante` e importará os dados iniciais (`banco_restaurante.sql`).
    * **Serviço `web`:** Construirá a imagem da sua API Flask, instalará as dependências Python e iniciará o servidor da API.

    A API Flask estará disponível em `http://localhost:5000`.

3.  **Usando a aplicação**

    Enquanto o `docker-compose up` estiver rodando em um terminal, abra **um novo terminal** para interagir com a aplicação.

    -   **Via terminal interativo (recomendado para iniciantes):**

        Para acessar o menu centralizado do Restaurante, use o comando abaixo em seu **novo terminal**:
   
         ```sh
            docker-compose exec web python app.py
         ```
         Ou especifique caso queira rodar apenas um script cliente (atendente, garçom ou gerente):
        
        ```sh
         docker-compose exec web python atendente_script.py
         docker-compose exec web python garcom_script.py
         docker-compose exec web python gerente_script.py
        ```

        Siga as instruções que aparecerão na tela.

    -   **Via API HTTP (para desenvolvedores ou testes avançados):**

        Você pode usar ferramentas como Postman, Insomnia, `curl` ou até mesmo o navegador para fazer requisições HTTP diretamente para `http://localhost:5000` (substitua pelo IP do seu Docker se necessário).

4.  **Parar a aplicação**

    Para desligar todos os serviços do Docker, vá para o terminal onde você rodou `docker-compose up`, pressione `CTRL+C` e, em seguida, execute:

    ```sh
    docker-compose down
    ```

---

### 🚨 Dicas e Solução de Problemas

-   **"Erro de input() no Docker" ou script não interativo:**
    Sempre use `docker-compose exec web python <nome_do_script.py>` (ex: `atendente_script.py`) para rodar scripts que esperam input do usuário. Não tente rodar esses scripts diretamente via `docker-compose up` pois o processo não será interativo.
-   **"Portas ocupadas" (Erro `Address already in use`):**
    Se as portas 3306 (MySQL) ou 5000 (Flask) já estiverem em uso em seu sistema, feche outros programas que possam estar usando essas portas (como outras instâncias do MySQL, XAMPP, ou outras aplicações web).
-   **"Banco de dados limpo ao reiniciar":**
    Por padrão, o container do banco de dados é recriado (e o `banco_restaurante.sql` é executado) toda vez que você roda `docker-compose up --build` ou `docker-compose up` após um `docker-compose down`. Para persistir os dados entre reinícios, você pode configurar um volume persistente para o serviço `db` no seu `docker-compose.yml`.

---

## 👩‍💻 Para Colaboradores/Desenvolvedores

### Estrutura dos Arquivos

-   `app.py`: O coração da API Flask (backend HTTP), define as rotas e orquestra a lógica de negócio.
-   `crud.py`: Módulo responsável por todas as operações de C.R.U.D. (Criar, Ler, Atualizar, Deletar) diretamente no banco de dados MySQL.
-   `config.py`: Arquivo de configurações globais para o restaurante (horários, dias de funcionamento, capacidade de mesas, etc.).
-   `atendente_script.py`, `garcom_script.py`, `gerente_script.py`: Interfaces de linha de comando (CLI) que atuam como clientes, interagindo com a API.
-   `utils.py`: Funções utilitárias de apoio (ex: separadores de linha para o terminal).
-   `banco_restaurante.sql`: Script SQL para criação do esquema do banco de dados e popularização inicial com dados de exemplo.
-   `Dockerfile` e `docker-compose.yml`: Arquivos de configuração do Docker para empacotar e orquestrar a aplicação (API e banco de dados).
-   `requirements.txt`: Lista de dependências Python necessárias para o projeto.

### Atualizando a Aplicação (Reconstrução do Docker)

Se você fizer alterações significativas no código-fonte, nas dependências Python (`requirements.txt`) ou no script SQL do banco de dados (`banco_restaurante.sql`), você precisará reconstruir as imagens Docker.

No terminal, execute:

```sh
docker-compose down
docker-compose up --build
```

O parâmetro `--build` garante que o Docker irá reconstruir a imagem do serviço `web` (e `db`, se houver alterações no Dockerfile dele) com as últimas alterações feitas no seu projeto.

### Boas Práticas para Desenvolvimento

-   Sempre teste suas alterações localmente usando Docker antes de enviar para o repositório.
-   Se adicionar novas bibliotecas Python, lembre-se de atualizar o `requirements.txt` para que o Docker inclua a nova dependência:
    ```sh
    pip freeze > requirements.txt
    ```
-   Prefira usar variáveis de ambiente para credenciais e configurações sensíveis (ex: senhas de banco de dados).
-   Documente suas alterações no código através de comentários claros e, se aplicável, atualize este README.

---

## 📋 Exemplo de Dados Iniciais: Tabela de Reservas

Ao rodar o sistema pela primeira vez com Docker, o banco já vem preenchido com reservas de exemplo. Veja abaixo como ficam os dados iniciais da tabela `tb_reservas`:

| idReserva | dataReserva | horaReserva | nomeCliente     | quantidadePessoas | statusReservaConfirmada | idMesaReserva |
|-----------|-------------|-------------|-----------------|-------------------|-------------------------|---------------|
| 1         | 2025-06-11  | 14:00:00    | Ana Silva       | 2                 | 1                       | 1             |
| 2         | 2025-06-11  | 16:30:00    | Bruno Souza     | 4                 | 0                       | 2             |
| 3         | 2025-06-12  | 19:00:00    | Carlos Lima     | 3                 | 1                       | 3             |
| 4         | 2025-06-12  | 21:30:00    | Daniela Rocha   | 5                 | 0                       | 4             |
| 5         | 2025-06-13  | 15:00:00    | Eduardo Alves   | 2                 | 1                       | 5             |
| 6         | 2025-06-13  | 18:00:00    | Fernanda Dias   | 6                 | 0                       | 6             |
| 7         | 2025-06-14  | 14:30:00    | Gabriel Pinto   | 2                 | 1                       | 7             |
| 8         | 2025-06-14  | 17:00:00    | Helena Costa    | 4                 | 0                       | 8             |
| 9         | 2025-06-16  | 20:00:00    | Igor Martins    | 3                 | 1                       | 9             |
| 10        | 2025-06-16  | 22:30:00    | Juliana Ramos   | 2                 | 0                       | 10            |
| 11        | 2025-06-17  | 14:00:00    | Kleber Souza    | 5                 | 1                       | 1             |
| 12        | 2025-06-17  | 16:30:00    | Larissa Melo    | 2                 | 0                       | 2             |
| 13        | 2025-06-18  | 19:00:00    | Marcos Silva    | 4                 | 1                       | 3             |
| 14        | 2025-06-18  | 21:30:00    | Nathalia Cruz   | 3                 | 0                       | 4             |
| 15        | 2025-06-19  | 15:00:00    | Otávio Lima     | 2                 | 1                       | 5             |
| 16        | 2025-06-19  | 18:00:00    | Patrícia Dias   | 6                 | 0                       | 6             |
| 17        | 2025-06-20  | 14:30:00    | Quésia Pinto    | 2                 | 1                       | 7             |
| 18        | 2025-06-20  | 17:00:00    | Rafael Costa    | 4                 | 0                       | 8             |
| 19        | 2025-07-02  | 20:00:00    | Sabrina Martins | 3                 | 1                       | 9             |
| 20        | 2025-07-03  | 19:00:00    | Tiago Ramos     | 2                 | 0                       | 10            |

Legenda:
-   **statusReservaConfirmada**: `1` = Confirmada, `0` = Não confirmada
