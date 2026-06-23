<div align="center">
   <h1>MBA Engenharia de Software com IA</h1>
   <h2>Desafio 1 - Full Cycle</h2>
</div>

## Passo a passo para executar o projeto

### 1. Baixe o projeto

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/ortegavan/mba-desafio-1.git
cd mba-desafio-1
```

### 2. Crie e ative o ambiente virtual (venv)

O venv é um ambiente Python isolado, só deste projeto. Ele evita que as bibliotecas
deste projeto se misturem com as de outros.

Crie o ambiente (só na primeira vez):

```bash
python3 -m venv venv
```

Ative o ambiente (toda vez que for trabalhar no projeto):

```bash
# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

Como saber se deu certo: o início da linha do seu terminal vai passar a mostrar `(venv)`.

### 3. Instale as dependências

Com o `(venv)` ativo, instale as bibliotecas do projeto:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente (`.env`)

O projeto guarda informações sensíveis (como sua chave da OpenAI) num arquivo `.env` que nunca é enviado para o GitHub.

**a) Crie o seu `.env` a partir do modelo:**

```bash
# macOS / Linux
cp .env.example .env

# Windows (PowerShell)
copy .env.example .env
```

**b) Abra o arquivo `.env` no seu editor e preencha os valores.** Ele deve ficar assim:

```env
OPENAI_API_KEY=sk-cole-sua-chave-secreta-aqui
OPENAI_EMBEDDING_MODEL='text-embedding-3-small'
OPENAI_LLM_MODEL='gpt-5-nano'
DATABASE_URL='postgresql+psycopg://postgres:postgres@localhost:5432/rag'
PG_VECTOR_COLLECTION_NAME='desafio1'
PDF_PATH='document.pdf'
```

#### Como obter a `OPENAI_API_KEY`

1. Acesse **https://platform.openai.com/api-keys**
2. Faça login e clique para criar uma nova chave secreta
3. Copie a chave assim que ela aparecer (você não consegue vê-la de novo depois) e cole no seu `.env`

### 5. Suba o banco de dados

O banco de dados (PostgreSQL com a extensão pgVector) roda dentro do Docker, então você não precisa instalar banco nenhum na sua máquina.

**Suba o banco:**

```bash
docker compose up -d
```

**Confira se subiu certo:**

```bash
docker compose ps
```

Você deve ver o container do banco com status `running` / `healthy`. 

### 6. Fazer a ingestão do PDF

Agora vamos ler o PDF e guardá-lo no banco. Este passo você roda apenas uma vez (ou de novo se trocar o PDF).

```bash
python3 src/ingest.py
```

### 7. Conversar com o PDF (o chat)

Finalmente, inicie o chat no terminal:

```bash
python3 src/chat.py
```

Faça suas perguntas. Teste uma coisa que está no PDF e outra que não está, para ver os dois comportamentos:

```
Faça sua pergunta: Qual o faturamento da empresa Alfa Energia S.A.?
Faça sua pergunta: Qual é a capital da França?
```

A segunda deve responder "Não tenho informações necessárias para responder sua pergunta." porque a resposta não está no documento. Para encerrar o chat, digite `sair` (ou pressione `Ctrl+C`).

### 8. Desligar o banco quando terminar

Quando você acabar de usar, desligue o container do Docker para liberar recursos.

**Desligar (mantendo os dados já ingeridos):**

```bash
docker compose down
```

**Desligar e apagar tudo (banco zerado):** se quiser começar do zero (por exemplo, para ingerir um PDF diferente), apague também o volume de dados:

```bash
docker compose down -v
```
