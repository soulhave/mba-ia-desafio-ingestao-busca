# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema RAG (Retrieval-Augmented Generation) para ingestão e busca de documentos PDF usando PostgreSQL com pgvector e OpenAI.

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+
- Chave de API da OpenAI
- Documento PDF para ingestão (já incluído: `document.pdf`)

## 🚀 Como Executar

### 1. Subir o Docker (PostgreSQL + pgvector)

Primeiro, inicie o banco de dados PostgreSQL com suporte a pgvector:

```bash
docker compose up -d
```

Este comando irá:
- Iniciar um container PostgreSQL 17 com pgvector
- Criar o banco de dados `rag`
- Configurar o usuário `postgres` com senha `postgres`
- Expor a porta `5432`
- Executar automaticamente a extensão pgvector

**Verificar se está funcionando:**
```bash
docker compose ps
```

Você deve ver os containers `postgres_rag` e `bootstrap_vector_ext` rodando.

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sua_chave_api_aqui
OPENAI_MODEL=text-embedding-3-small

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=documentos

# PDF Configuration
PDF_PATH=document.pdf
```

**Importante:** Substitua `sua_chave_api_aqui` pela sua chave real da OpenAI.

### 3. Configurar Ambiente Python

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Ingestão dos Dados

Execute o script de ingestão para processar o documento PDF:

```bash
python src/ingest.py
```

**O que acontece durante a ingestão:**
- O PDF é carregado e dividido em chunks de 1000 caracteres com overlap de 150
- Cada chunk é convertido em embedding usando o modelo `text-embedding-3-small`
- Os embeddings são armazenados no PostgreSQL usando pgvector
- Você verá a mensagem: "✅ Ingestão concluída com sucesso! X documentos foram processados"

**Troubleshooting da ingestão:**
- Verifique se o arquivo `document.pdf` existe na raiz do projeto
- Confirme se as variáveis de ambiente estão configuradas corretamente
- Certifique-se de que o Docker está rodando e o banco está acessível

### 5. Usar o Chat

Após a ingestão bem-sucedida, você pode fazer perguntas sobre o documento:

```bash
python src/chat.py
```

**Como usar o chat:**
1. Execute o comando acima
2. Digite sua pergunta quando solicitado
3. O sistema irá:
   - Buscar os chunks mais relevantes do documento
   - Usar o GPT-5-mini para gerar uma resposta baseada no contexto
   - Responder apenas com informações presentes no documento

**Exemplo de uso:**
```
PERGUNTA: Qual é o tema principal do documento?
RESPOSTA: [Resposta baseada no conteúdo do PDF]
```

## 🔧 Arquitetura do Sistema

### Componentes Principais:

1. **PostgreSQL + pgvector**: Armazena embeddings vetoriais dos documentos
2. **OpenAI Embeddings**: Converte texto em vetores para busca semântica
3. **LangChain**: Framework para processamento de documentos e RAG
4. **PyPDF**: Carregamento e processamento de PDFs

### Fluxo de Funcionamento:

1. **Ingestão**: PDF → Chunks → Embeddings → PostgreSQL
2. **Busca**: Pergunta → Embedding → Similaridade → Contexto
3. **Geração**: Contexto + Pergunta → GPT → Resposta

## 📁 Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── docker compose.yml          # Configuração do PostgreSQL + pgvector
├── requirements.txt            # Dependências Python
├── document.pdf               # Documento para ingestão
├── .env                       # Variáveis de ambiente (criar)
├── README.md                  # Este arquivo
└── src/
    ├── ingest.py              # Script de ingestão
    ├── search.py              # Lógica de busca e RAG
    └── chat.py                # Interface de chat
```

## 🛠️ Troubleshooting

### Problemas Comuns:

**Erro de conexão com banco:**
- Verifique se o Docker está rodando: `docker compose ps`
- Confirme se a porta 5432 está livre
- Teste a conexão: `psql postgresql://postgres:postgres@localhost:5432/rag`

**Erro de API OpenAI:**
- Verifique se a chave API está correta no `.env`
- Confirme se tem créditos suficientes na conta OpenAI

**Erro de ingestão:**
- Verifique se o arquivo `document.pdf` existe
- Confirme se todas as variáveis de ambiente estão definidas

**Erro de módulos Python:**
- Ative o ambiente virtual: `source venv/bin/activate`
- Reinstale as dependências: `pip install -r requirements.txt`

## 🧹 Limpeza

Para parar e remover os containers:

```bash
docker compose down -v
```

Para remover completamente os dados:

```bash
docker compose down -v --rmi all
```

## 📝 Notas Importantes

- O sistema responde apenas com base no conteúdo do documento ingerido
- Se uma pergunta não estiver no contexto, o sistema responderá: "Não tenho informações necessárias para responder sua pergunta"
- O modelo usado para embeddings é `text-embedding-3-small` (padrão) ou configurável via `OPENAI_MODEL`
- O modelo usado para geração de respostas é `gpt-5-mini`
- Os chunks têm tamanho de 1000 caracteres com overlap de 150 para melhor contexto