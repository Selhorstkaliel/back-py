# LIMITCLEAN — Sistema de Serviços de Limpeza/Rating

Mono-repo para um sistema completo de gestão de serviços (Limpeza/Rating PF/PJ), com cadastro de clientes, descontos dinâmicos, emissão de contrato PDF, dashboard e RBAC.  
**Stack:** Next.js 14/React 18, FastAPI, Python 3.11+, Ruby (scheduler worker), SQLite, JWT Ed25519, Argon2id, Tailwind (dark neon), shadcn/ui.

## Estrutura

```
limitclean/
├─ README.md
├─ .env.example
├─ /server              # FastAPI (Python)
│  ├─ pyproject.toml
│  ├─ alembic.ini
│  ├─ /alembic
│  ├─ /app
│  │  ├─ main.py
│  │  ├─ deps.py
│  │  ├─ config.py
│  │  ├─ db.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ security.py
│  │  ├─ validators/
│  │  │  └─ cpf_cnpj.py
│  │  ├─ routes/
│  │  │  ├─ auth.py
│  │  │  ├─ users.py
│  │  │  ├─ entries.py
│  │  │  ├─ stats.py
│  │  │  ├─ charts.py
│  │  │  ├─ profile.py
│  │  │  ├─ support.py
│  │  │  └─ contract.py
│  │  ├─ services/
│  │  │  ├─ discounts.py
│  │  │  └─ contract.py
│  │  └─ utils/
│  │     ├─ dates.py
│  │     └─ money.py
│  └─ /data
│     └─ dev.sqlite
├─ /worker              # Ruby scheduler
│  ├─ Gemfile
│  ├─ config.rb
│  └─ scheduler.rb
└─ /web                 # Next.js (JavaScript)
   ├─ package.json
   ├─ next.config.js
   ├─ tailwind.config.js
   ├─ postcss.config.js
   ├─ .env.local
   ├─ app/
   │  ├─ layout.js
   │  ├─ globals.css
   │  ├─ middleware.js
   │  ├─ (auth)/auth/login/page.js
   │  └─ (protected)/
   │     ├─ page.js
   │     ├─ dashboard/page.js
   │     ├─ cadastro/page.js
   │     ├─ support/page.js
   │     └─ config/page.js
   ├─ components/...
   ├─ lib/fetch.js
   ├─ store/filters.js
   └─ hooks/...
```

---

## Passos para rodar localmente

1. **Back-end (FastAPI)**
```bash
cd server
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # ou poetry install
alembic upgrade head
uvicorn app.main:app --reload
```

2. **Worker (Ruby)**
```bash
cd worker
bundle install
ruby scheduler.rb
```

3. **Front-end (Next.js)**
```bash
cd web
npm install
npm run dev
```

4. **Acesse**: http://localhost:3000  
Login: `Kaliel` / `kaskolk14`

---

## Variáveis de ambiente (exemplo)

- `/server/.env`
```
PORT=3001
NODE_ENV=development
SQLITE_PATH=./data/dev.sqlite
JWT_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----"
JWT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
FRONTEND_ORIGIN=http://localhost:3000
CPF_CNPJ_PUBLIC_API="https://ws.hubdodesenvolvedor.com.br/v2/cpf-cnpj/?cpfcnpj="
```
> Se não existirem chaves Ed25519, elas serão geradas automaticamente no 1º start.

- `/web/.env.local`
```
BASE_API_URL=http://localhost:3001
```

- `/worker/.env`
```
SQLITE_PATH=../server/data/dev.sqlite
```

---

## Scripts

- **Server**:  
  - `pip install -r requirements.txt`  
  - `alembic upgrade head`  
  - `uvicorn app.main:app --reload`
- **Worker**:  
  - `bundle install`  
  - `ruby scheduler.rb`
- **Web**:  
  - `npm install`  
  - `npm run dev`

---

## Testes

- **Back-end (Pytest)**:  
  - `pytest`
- **Front-end (Jest/RTL, Playwright)**:  
  - `npm test`, `npx playwright test`
- **Worker (Ruby)**:  
  - `ruby test_scheduler.rb` (se houver)

---

## Critérios essenciais

- Login seguro (JWT Ed25519 em cookie httpOnly)
- Dashboard com KPIs/gráficos filtráveis
- Cadastro validando CPF/CNPJ (API + fallback), uploads, contrato PDF
- Scheduler Ruby alterando status
- Configurações CRUD por papel
- Tickets de suporte
- Sem tokens em localStorage
- Código limpo, documentado, testável

---

**Dúvidas?** Veja o código de cada pasta ou abra um issue.