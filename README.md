🍕 Pedido Manager
Sistema web para gerenciamento de pedidos de uma pizzaria. O projeto
reúne recursos para clientes, administração, cozinha e acompanhamento de
entregas.
Status: em desenvolvimento contínuo.

Sobre o projeto
O Pedido Manager é uma aplicação Full Stack com frontend em React e
TypeScript, backend em Python com FastAPI e banco de dados PostgreSQL. O
PostgreSQL é hospedado no Supabase, e o frontend pode ser publicado na
Vercel.

O objetivo é centralizar o fluxo de pedidos, desde a criação até a
preparação e entrega.
Funcionalidades
Conta e acesso
- Cadastro e login de usuários.
- Autenticação por token Bearer.
- Proteção de rotas.
- Diferenciação entre usuários comuns e administradores.
Pedidos
- Criação e visualização de pedidos.
- Seleção de produtos, sabores, tamanhos e quantidades.
- Exibição dos itens e valores.
- Acompanhamento do status.
- Inclusão de endereço de entrega.
- Consulta de CEP com a API ViaCEP para auxiliar o preenchimento do
  endereço.
Pagamento e cancelamento
- Opções de forma de pagamento, como PIX, cartão e dinheiro.
- Fluxos de finalização e cancelamento.
- Regra de multa de cancelamento após o prazo de tolerância
  configurado.
A exibição de formas de pagamento não significa necessariamente que
exista integração com bancos ou processamento automático de
pagamentos.

Administração e cozinha
- Consulta administrativa dos pedidos.
- Visualização dos itens de cada pedido.
- Área da cozinha para acompanhar a produção.
- Acompanhamento de pedidos prontos.
Entrega
- Listagem de pedidos em entrega.
- Visualização do endereço.
- Confirmação de entrega por código.
Painel e histórico
- Dashboard com informações operacionais.
- Histórico de pedidos.
- Área de perfil do usuário.
Tecnologias
Frontend - React - TypeScript - Vite - Tailwind CSS - React Router -
Lucide React

Backend - Python - FastAPI - SQLAlchemy - Alembic - PostgreSQL

Serviços - Supabase --- hospedagem do PostgreSQL. - Vercel ---
publicação do frontend. - ViaCEP --- consulta de CEP.
Arquitetura e organização
O frontend e o backend são projetos separados. A estrutura conhecida
inclui:
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
    ├── dependecies.py
    └── ...
A estrutura é ilustrativa; outros arquivos e pastas podem existir no
repositório.
Como executar localmente
Pré-requisitos
- Node.js e npm.
- Python 3.
- PostgreSQL local ou projeto no Supabase.
- Git.
1. Clonar o repositório
git clone URL_DO_SEU_REPOSITORIO
cd NOME_DO_REPOSITORIO
Substitua os valores de exemplo pelo endereço e nome reais do seu
repositório.
2. Preparar o backend
cd back-end
python -m venv venv
No Windows, ative o ambiente:
venv\Scripts\activate
Instale as dependências, caso exista requirements.txt:
pip install -r requirements.txt
Crie um arquivo .env na pasta do backend:
DATABASE_URL=sua_url_de_conexao_postgresql
Aplique as migrações do Alembic:
alembic upgrade head
Inicie a API, considerando que a instância FastAPI esteja definida como
app em main.py:
uvicorn main:app --reload
A documentação interativa costuma ficar disponível em
http://127.0.0.1:8000/docs, se estiver habilitada.
3. Preparar o frontend
Em outro terminal:
cd frontend
npm install
Crie um arquivo .env na pasta do frontend:
VITE_API_URL=http://127.0.0.1:8000
Inicie o Vite:
npm run dev
O terminal informará o endereço local da aplicação.
Os comandos consideram uma configuração padrão de Vite, FastAPI e
Alembic. Se o package.json, o arquivo de dependências ou os módulos
do seu projeto tiverem nomes diferentes, siga a configuração real do
repositório.

Variáveis de ambiente
  Variável         Local      Finalidade
  DATABASE_URL   Backend    Conexão com o PostgreSQL
VITE_API_URL   Frontend   Endereço base da API
Segurança
- Não envie arquivos .env para o GitHub.
- Não coloque senhas, tokens ou chaves privadas no código.
- Configure as variáveis também no serviço de hospedagem.
- Variáveis VITE_ são expostas ao navegador; nunca coloque segredos
  nelas.
Publicação
Frontend na Vercel
1. Importe o repositório do GitHub.
2. Configure o diretório do frontend como raiz do projeto, se
   necessário.
3. Defina VITE_API_URL com a URL pública do backend.
4. Execute o deploy.
Banco no Supabase
1. Crie ou selecione um projeto Supabase.
2. Obtenha a URL de conexão PostgreSQL.
3. Configure DATABASE_URL no ambiente do backend.
4. Execute as migrações do Alembic.
O backend também precisa estar hospedado em um serviço que execute
Python/FastAPI e configurado para aceitar requisições do domínio do
frontend.
Fluxo geral de um pedido
1. O cliente acessa sua conta.
2. Cria um pedido e seleciona produtos e opções.
3. Informa o endereço de entrega.
4. Segue para a etapa de pagamento.
5. A equipe acompanha o pedido pela administração e pela cozinha.
6. O pedido avança pelos status implementados no sistema.
7. A entrega pode ser confirmada por código.
Os status e as regras finais dependem da implementação atual do backend.
Banco de dados e migrações
O projeto utiliza PostgreSQL com Alembic para versionar alterações no
esquema do banco.

Aplicar migrações:
alembic upgrade head
Consultar a revisão atual:
alembic current
Mantenha os arquivos de migração no controle de versão para reproduzir a
estrutura do banco em outros ambientes.
Contribuição
Sugestões e melhorias são bem-vindas.
1. Faça um fork.
2. Crie uma branch:
git checkout -b minha-melhoria
3. Faça e teste suas alterações.
4. Registre um commit:
git commit -m "Descreve a melhoria"
5. Envie a branch:
git push origin minha-melhoria
6. Abra um Pull Request explicando as mudanças.
Próximas melhorias
Ideias de evolução --- não representam necessariamente funcionalidades
já concluídas: - Aprimorar o carrinho. - Revisar e completar o fluxo de
endereço. - Evoluir o acompanhamento da entrega. - Melhorar o histórico
de pedidos. - Ampliar os indicadores do dashboard. - Adicionar testes
automatizados.
🤖 Uso de Inteligência Artificial
Durante o desenvolvimento deste projeto, foram utilizadas ferramentas de Inteligência Artificial como apoio na criação, organização e correção de partes do frontend.

As sugestões geradas foram analisadas, adaptadas e integradas ao projeto durante o desenvolvimento.
Autor
Desenvolvido por Carlos Eduardo.
⭐ Se gostou do projeto, considere deixar uma estrela no repositório.
