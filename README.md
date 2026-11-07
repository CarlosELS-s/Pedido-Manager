
# 🍕 Pedido Manager

### Sistema de gerenciamento de pedidos para pizzarias

O **Pedido Manager** é uma aplicação web desenvolvida para facilitar o gerenciamento de pedidos de uma pizzaria, permitindo acompanhar as etapas de produção, controlar entregas e administrar clientes e produtos em um único lugar.

O projeto utiliza uma arquitetura com frontend e backend separados, oferecendo uma interface moderna, responsiva e integrada a uma API.

---

## 📸 Sobre o projeto

O Pedido Manager foi desenvolvido para digitalizar e organizar o fluxo de trabalho de uma pizzaria, desde o gerenciamento dos pedidos até o acompanhamento das entregas.

A aplicação possui diferentes áreas de gerenciamento, permitindo que cada etapa da operação seja acompanhada de maneira organizada.

## 🚀 Funcionalidades

### 👤 Usuários e autenticação
- Cadastro de usuários.
- Login com autenticação por token JWT.
- Controle de acesso às funcionalidades.
- Identificação de usuários administradores.
- Área de perfil do usuário.

### 📦 Gerenciamento de pedidos
- Criação e visualização de pedidos.
- Consulta dos pedidos cadastrados.
- Visualização dos itens de cada pedido.
- Acompanhamento dos valores.
- Cancelamento de pedidos.
- Controle dos estados dos pedidos.

### 👨‍🍳 Gerenciamento da cozinha
- Visualização dos pedidos em produção.
- Acompanhamento dos pedidos finalizados.
- Atualização do status para pronto.

### 🚚 Controle de entregas
- Acompanhamento dos pedidos prontos.
- Gerenciamento dos pedidos em entrega.
- Confirmação de entrega por código.

### 🛠️ Administração
- Dashboard administrativo.
- Visualização de estatísticas dos pedidos.
- Gerenciamento de produtos.
- Gerenciamento de usuários.
- Acompanhamento da operação da pizzaria.

### 👀 Modo demonstração
- Acesso como visitante.
- Visualização de telas administrativas.
- Exibição de dados fictícios.
- Navegação em modo somente leitura.
- Separação entre os dados demonstrativos e os dados reais.

---

## 🧰 Tecnologias utilizadas

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS
- React Router DOM
- Lucide React

### Backend
- Python
- FastAPI
- SQLAlchemy
- JWT (JSON Web Token)
- Alembic

### Banco de dados
- PostgreSQL
- Supabase

### Hospedagem
- Vercel — Frontend
- Render — Backend
- Supabase — Banco de dados

---

## 🏗️ Arquitetura do projeto

O sistema é dividido em duas aplicações principais:

```text
Pedido-Manager/
│
├── back-end/
│   ├── main.py
│   ├── models.py
│   ├── auth_router.py
│   ├── order_router.py
│   ├── produto_router.py
│   ├── dependecies.py
│   ├── routers/
│   ├── alembic/
│   └── requirements.txt
│
└── pedido-manager/
    ├── src/
    │   ├── components/
    │   ├── context/
    │   ├── lib/
    │   └── pages/
    ├── public/
    ├── package.json
    └── vite.config.ts
```

*Estrutura ilustrativa: os nomes e a organização podem variar conforme a versão do repositório.*

---

## 💻 Como executar o projeto localmente

### 1. Pré-requisitos

Antes de começar, instale:

- Python
- Node.js e npm
- Git
- Uma instância PostgreSQL ou projeto Supabase

### 2. Clonar o repositório

```bash
git clone https://github.com/CarlosELS-s/Pedido-Manager.git
```

Entre na pasta do projeto:

```bash
cd Pedido-Manager
```

### 3. Configurar o backend

Entre na pasta do backend:

```bash
cd back-end
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente em um arquivo `.env`:

```env
DATABASE_URL=sua_url_do_postgresql
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
```

**Importante:** substitua os valores de exemplo pelas configurações reais. Nunca publique senhas ou chaves secretas no GitHub.

Execute as migrações do banco de dados, se necessário:

```bash
alembic upgrade head
```

Inicie o servidor:

```bash
python -m uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

### 4. Configurar o frontend

Abra outro terminal e entre na pasta do frontend:

```bash
cd pedido-manager
```

Instale as dependências:

```bash
npm install
```

Crie um arquivo `.env` na pasta do frontend:

```env
VITE_API_URL=http://127.0.0.1:8000
```

Inicie a aplicação:

```bash
npm run dev
```

O frontend ficará disponível no endereço informado pelo Vite, normalmente:

```text
http://localhost:5173
```

---

## 🌐 Deploy e hospedagem

O projeto pode ser publicado utilizando serviços separados para frontend, backend e banco de dados.

| Serviço | Plataforma |
|---|---|
| Frontend | Vercel |
| Backend | Render |
| Banco de dados | Supabase |

### Configuração do frontend na Vercel

Build Command:

```bash
npm run build
```

Output Directory:

```text
dist
```

Install Command:

```bash
npm install
```

Variável de ambiente:

```env
VITE_API_URL=https://SEU-BACKEND.onrender.com
```

### Configuração do backend no Render

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Configure também as variáveis de ambiente necessárias, como `DATABASE_URL`, `SECRET_KEY` e `ALGORITHM`.

---

## 🔐 Segurança

O projeto utiliza autenticação baseada em JWT para controlar o acesso às funcionalidades protegidas.

Entre os mecanismos utilizados estão:

- Autenticação por token.
- Verificação de permissões.
- Separação entre usuários comuns e administradores.
- Proteção de rotas da API.
- Separação dos dados fictícios do modo demonstração.

As credenciais e configurações privadas devem ser armazenadas em variáveis de ambiente.

---

## 📚 Documentação da API

O backend utiliza FastAPI, que disponibiliza documentação interativa automaticamente.

Após iniciar o servidor, acesse:

```text
/docs
```

Nessa página é possível visualizar os endpoints e testar as requisições da API.

---

## 🎯 Objetivo do projeto

O objetivo do Pedido Manager é aplicar conhecimentos de desenvolvimento Full Stack na construção de uma aplicação real de gerenciamento comercial.

O desenvolvimento envolve integração entre frontend e backend, autenticação, persistência de dados, gerenciamento de estados, APIs REST e publicação em serviços de hospedagem.

---

## 👨‍💻 Desenvolvedor

**Carlos Eduardo Leite da Silva**

Projeto desenvolvido como aplicação prática de estudos e desenvolvimento Full Stack.

---

## 📄 Licença

Este projeto ainda não possui uma licença de distribuição especificada.

---

<p align="center">
  Desenvolvido com dedicação e tecnologia. 🍕
</p>
