# 🍕 Pedido Manager

> Sistema web Full Stack para gerenciamento e automação de pedidos de uma pizzaria.

O **Pedido Manager** é uma aplicação completa projetada para centralizar todo o fluxo de pedidos de uma pizzaria, reunindo recursos dedicados para clientes, painel de administração, tela operacional da cozinha e acompanhamento logístico de entregas. O projeto separa totalmente as responsabilidades entre o front-end e o back-end, operando de forma 100% integrada.

**Status:** Em desenvolvimento contínuo 🚀

---

## 🚀 Demonstração e Publicação

- **Hospedagem do Front-end:** Publicado na Vercel.
- **Banco de Dados:** PostgreSQL hospedado e gerenciado via Supabase.

---

## 🎯 Funcionalidades Principais

### 🔒 Conta e Acesso
- **Autenticação Segura:** Cadastro e login de usuários com autenticação por token Bearer (JWT).
- **Proteção de Rotas:** Bloqueio de acessos não autorizados nas rotas da aplicação.
- **Níveis de Acesso (RBAC):** Diferenciação clara de permissões entre usuários comuns (clientes) e administradores/funcionários.

### 📝 Fluxo de Pedidos
- **Criação Interativa:** Seleção dinâmica de produtos, sabores, tamanhos e quantidades.
- **Checkout Clara:** Exibição detalhada dos itens selecionados, valores parciais e cálculo total do pedido.
- **Acompanhamento de Status:** Atualização em tempo real do progresso do pedido para o cliente.
- **Logística:** Inclusão e associação do endereço de entrega ao pedido realizado.

### 💳 Pagamento e Cancelamento
- **Opções de Checkout:** Suporte visual para seleção de formas de pagamento (PIX, Cartão e Dinheiro).
- **Regras de Negócio Avançadas:** Fluxo de cancelamento automatizado com aplicação de regra de multa caso o prazo de tolerância configurado seja ultrapassado.
  - *Nota: A exibição de formas de pagamento representa a escolha do usuário e não necessariamente uma integração direta com gateways de pagamento bancário.*

### 🍳 Administração e Cozinha
- **Gestão Operacional:** Painel administrativo dedicado para consulta e triagem de todos os pedidos ativos.
- **Monitor da Cozinha:** Área exclusiva de produção para os pizzaiolos visualizarem os itens de cada pedido e marcarem a conclusão dos preparos.

### 🛵 Módulo de Entrega
- **Painel do Entregador:** Listagem inteligente dos pedidos prontos despachados para rota.
- **Segurança na Entrega:** Sistema de confirmação de entrega concluída mediante inserção de código de validação.

### 📊 Painel e Histórico
- **Dashboard Operacional:** Painel com métricas e informações rápidas sobre o andamento diário da pizzaria.
- **Histórico de Pedidos:** Acesso a todas as compras anteriores do cliente e área de edição do perfil do usuário.

---

## 🛠️ Tecnologias Utilizadas

### Front-end
- **React** & **TypeScript**
- **Vite** (Build Tool de alto desempenho)
- **Tailwind CSS** (Estilização utilitária e responsiva)
- **React Router** (Gerenciamento de rotas SPA)
- **Lucide React** (Pacote de ícones modernos)

### Back-end
- **Python** & **FastAPI**
- **SQLAlchemy** (ORM para mapeamento de dados)
- **Alembic** (Gerenciador de migrações de banco de dados)
- **PostgreSQL** (Banco de dados relacional robusto)

---

## 🏗️ Arquitetura e Organização

O front-end e o back-end rodam em ambientes totalmente isolados um do outro. A árvore abaixo exemplifica a distribuição estrutural das pastas do repositório:

```text
pedido-manager/
├── frontend/
│   └── src/
│       ├── pages/
│       ├── lib/
│       └── ...
└── back-end/
    ├── main.py
    ├── models.py
    ├── auth_router.py
    ├── order_router.py
    ├── produto_router.py
    ├── classes.py
    ├── dependencies.py
    └── ...
```

---

## ⚙️ Como Executar o Projeto Localmente

### Pré-requisitos
- **Node.js** e gerenciador **npm** instalados.
- **Python 3.10+** configurado no sistema.
- Instância do **PostgreSQL** (local ou remota via Supabase).
- Cliente **Git** ativo.

### 1. Clonar o Repositório
```bash
git clone URL_DO_SEU_REPOSITORIO
cd NOME_DO_REPOSITORIO
```

### 2. Configurar e Iniciar o Back-end
```bash
cd back-end
python -m venv venv
```
- No Windows, ative o ambiente virtual com:
```bash
venv\Scripts\activate
```
- Instale as dependências contidas no arquivo do projeto:
```bash
pip install -r requirements.txt
```
- Crie um arquivo chamado `.env` na raiz da pasta `back-end/` e adicione sua string de conexão:
```env
DATABASE_URL=sua_url_de_conexao_postgresql
```
- Aplique as migrações do banco de dados para estruturar o PostgreSQL:
```bash
alembic upgrade head
```
- Inicie o servidor assíncrono da API FastAPI:
```bash
uvicorn main:app --reload
```
A documentação interativa e gerada automaticamente pelo Swagger ficará ativa no endereço: `http://127.0.0.1:8000/docs`.

### 3. Configurar e Iniciar o Front-end
Abra um terminal paralelo e execute os seguintes comandos:
```bash
cd frontend
npm install
```
- Crie um arquivo chamado `.env` na raiz da pasta `frontend/` informando a rota da API:
```env
VITE_API_URL=http://127.0.0.1:8000
```
- Execute o servidor de desenvolvimento do Vite:
```bash
npm run dev
```
O console exibirá o endereço `localhost` correto gerado para você acessar o site no navegador.

---

## 🔑 Variáveis de Ambiente

| Variável | Escopo | Finalidade |
| :--- | :--- | :--- |
| `DATABASE_URL` | Backend | String de autenticação e conexão com o banco PostgreSQL |
| `VITE_API_URL` | Frontend | Endereço HTTP base para comunicação com as rotas da API |

> ⚠️ **Segurança Importante:** Nunca commite ou envie os arquivos `.env` para repositórios públicos. Adicione-os sempre ao arquivo `.gitignore`. Variáveis iniciadas com o prefixo `VITE_` ficam visíveis ao navegador, portanto, nunca insira chaves ou segredos privados nelas.

---

## 🗄️ Banco de Dados e Migrações

Todas as alterações estruturais nas tabelas do banco de dados PostgreSQL são controladas pelo **Alembic**.

- Para aplicar novas migrações pendentes:
  ```bash
  alembic upgrade head
  ```
- Para verificar a versão de revisão atual do seu banco:
  ```bash
  alembic current
  ```

---

## 🤖 Uso de Inteligência Artificial

Durante o desenvolvimento deste projeto, foram utilizadas ferramentas de Inteligência Artificial como apoio focado na criação, organização estrutural e correções pontuais da interface do front-end. Todas as sugestões geradas pelas ferramentas foram criticamente analisadas, adaptadas e refinadas manualmente para garantir a aderência às regras de negócio propostas na API.

---

## 🔮 Próximas Melhorias (Roadmap de Evolução)

- [ ] Implementação de Testes Automatizados no Back-end com `pytest`.
- [ ] Aprimoramento da persistência e lógica do carrinho de compras.
- [ ] Ampliação de indicadores visuais e gráficos no Dashboard administrativo.
- [ ] Refinamento e polimento na listagem do histórico de pedidos do usuário.

---

## 👤 Autor

Desenvolvido por **Carlos Eduardo**.

⭐ *Se você achou este projeto interessante ou útil para os seus estudos, considere deixar uma estrela no repositório!*
