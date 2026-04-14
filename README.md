# 🌡️ Pipeline de Dados com IoT e Docker

> Disciplina: **Disruptive Architectures: IoT, Big Data e IA** — UniFECAF

## 📋 Sobre o Projeto

Pipeline de dados end-to-end que:
1. Lê leituras de temperatura de dispositivos IoT (dataset Kaggle)
2. Processa e armazena no **PostgreSQL** via **Docker**
3. Cria **3 views SQL** para análise
4. Exibe **dashboard interativo** com Streamlit e Plotly

## 🏗️ Arquitetura

```
IOT-temp.csv → ingest.py → PostgreSQL (Docker) → dashboard.py → Streamlit
                                   ↓
                             3 Views SQL
```

## 🛠️ Tecnologias

| Tecnologia | Versão | Finalidade |
|-----------|--------|------------|
| Python | 3.10+ | Linguagem principal |
| Docker | 24+ | Containerização do banco |
| PostgreSQL | 15 | Armazenamento dos dados |
| Pandas | 2.2 | Processamento do CSV |
| SQLAlchemy | 2.0 | Conexão com banco |
| Streamlit | 1.32 | Dashboard interativo |
| Plotly | 5.19 | Gráficos interativos |

## 📁 Estrutura

```
pipeline-iot/
├── src/
│   ├── ingest.py        # Lê CSV e insere no PostgreSQL
│   └── dashboard.py     # Dashboard Streamlit
├── data/
│   └── IOT-temp.csv     # Dataset Kaggle (baixar manualmente)
├── docs/
│   └── documentacao.pdf # Documentação teórica
├── sql/
│   └── views.sql        # 3 views SQL documentadas
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

## 🚀 Como Executar

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/pipeline-iot.git
cd pipeline-iot
```

### 2. Baixar o dataset
Acesse: https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices  
Salve o arquivo `IOT-temp.csv` na pasta `data/`

### 3. Subir o PostgreSQL com Docker
```bash
docker compose up -d
```

### 4. Criar ambiente virtual e instalar dependências
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 5. Executar a ingestão
```bash
python src/ingest.py
```

### 6. Abrir o dashboard
```bash
streamlit run src/dashboard.py
```
Acesse: http://localhost:8501

## 🗃️ Views SQL

| View | Propósito | Insight |
|------|-----------|---------|
| `avg_temp_por_dispositivo` | Temperatura média/mín/máx por sensor | Detecta dispositivos anômalos |
| `leituras_por_hora` | Contagem e média por hora do dia | Revela padrões operacionais |
| `temp_max_min_por_dia` | Variação térmica diária | Identifica eventos e tendências |

## 📊 Dataset

- **Nome:** Temperature Readings: IoT Devices
- **Fonte:** [Kaggle](https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices)
- **Registros:** ~97.600 leituras
