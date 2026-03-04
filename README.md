# 📊 Pipeline de Previsão de Demanda | Analytics Dashboard

> **Aplicação interativa de Data Science** implementando um pipeline completo de previsão de demanda seguindo a metodologia **CRISP-DM**, com interface premium inspirada em React/Next.js (Shadcn/UI).

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Visão Geral

### Contexto de Negócio

Empresa de manufatura global enfrenta **ineficiência logística** com custos elevados de armazenagem e rupturas de estoque. Este projeto automatiza a previsão de demanda usando modelos estatísticos robustos.

### Objetivo

Dashboard educacional e operacional que demonstra um pipeline completo de Data Science, desde a ingestão de dados até a comunicação de resultados, seguindo as 6 etapas do **CRISP-DM**.

### Destaques

- ✅ **Interface Premium:** Design Shadcn/UI com paleta HSL, fonte Inter e micro-animações
- ✅ **Navegação Intuitiva:** 9 seções CRISP-DM com sidebar + footer navigation
- ✅ **Didática Transparente:** Cada etapa técnica com 3 tabs (Explicação, Código, Resultado)
- ✅ **Modelos Comparativos:** Regressão Linear vs ETS (Holt-Winters)
- ✅ **Métricas Rigorosas:** MAE e RMSE para validação de performance

---

## 🚀 Quick Start

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Instalação

1. **Clone o repositório** (ou descompacte o projeto)

   ```bash
   cd "AM_Projeto - Pipeline de Previsão de Demanda"
   ```

2. **Crie um ambiente virtual** (recomendado)

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

### Execução

```bash
streamlit run scripts/main_app.py
```

A aplicação abrirá automaticamente em: **http://localhost:8501**

> **Nota Windows:** Se houver erro, use `python -m streamlit run scripts/main_app.py`

---

## 📂 Estrutura do Projeto

```
AM_Projeto - Pipeline de Previsão de Demanda/
│
├── assets/
│   └── img/
│       └── logo.jpg                    # Logo do projeto (sidebar + header + favicon)
│
├── data/
│   └── Historical Product Demand.csv   # Dataset Kaggle (Felix Zhao)
│
├── doc/
│   ├── PRD.md                          # Product Requirements Document
│   └── configuracao_ambiente.md        # Guia de setup do venv
│
├── scripts/
│   ├── data_utils.py                   # 🆕 Funções de dados (load, clean)
│   └── main_app.py                     # Aplicação Streamlit principal
│
├── venv/                                # Ambiente virtual (não versionado)
│
├── README.md                            # Este arquivo
└── requirements.txt                     # Dependências Python
```

---

## 🛠️ Stack Tecnológico

### Core Framework

| Biblioteca              | Versão  | Função                                       |
| ----------------------- | ------- | -------------------------------------------- |
| **Streamlit**           | ≥1.28.0 | Framework web interativo                     |
| **streamlit-shadcn-ui** | Latest  | Componentes UI premium (badges, metric_card) |

### Data Science

| Biblioteca       | Versão  | Função                                       |
| ---------------- | ------- | -------------------------------------------- |
| **pandas**       | ≥1.5.0  | Manipulação de DataFrames e séries temporais |
| **numpy**        | ≥1.21.0 | Operações matemáticas vetorizadas            |
| **statsmodels**  | ≥0.13.0 | STL (decomposição) e ETS (Holt-Winters)      |
| **scikit-learn** | ≥1.0.0  | Pipeline, StandardScaler, LinearRegression   |

### Visualização

| Biblioteca     | Versão  | Função                              |
| -------------- | ------- | ----------------------------------- |
| **plotnine**   | ≥0.10.0 | Grammar of Graphics (ggplot2 style) |
| **matplotlib** | ≥3.5.0  | Backend de renderização             |

---

## 📚 Navegação do Dashboard

### Estrutura de Seções (CRISP-DM)

| #   | Seção                 | Ícone                | Descrição                                      |
| --- | --------------------- | -------------------- | ---------------------------------------------- |
| 1   | **Projeto**           | 🎯 dashboard         | Contexto de negócio, objetivos e metodologia   |
| 2   | **Bibliotecas**       | 📚 library_books     | Tech stack e justificativas técnicas           |
| 3   | **Configuração**      | ⚙️ settings          | Parametrização global (float format, warnings) |
| 4   | **Coleta (Data)**     | 📥 download          | Ingestão do dataset (Kaggle CSV)               |
| 5   | **Tratamento (Data)** | 🧹 cleaning_services | Limpeza via Method Chaining (regex, datetime)  |
| 6   | **Análise (EDA)**     | 📊 analytics         | 9 sub-blocos: volumetria, gráficos, STL        |
| 7   | **Modelagem**         | 🧠 psychology        | Feature engineering, RL Pipeline, ETS          |
| 8   | **Avaliação**         | 📏 rule              | Métricas (MAE, RMSE), comparação visual        |
| 9   | **Comunicação**       | 📢 campaign          | Recomendações de negócio, KPIs simulados       |

### Padrão de Conteúdo (Tabs Didáticas)

Cada seção técnica (2-8) segue o padrão:

- **📄 Explicação:** Teoria e contexto de negócio
- **💻 Código:** Código-fonte executável e comentado
- **👁️ Resultado:** Output real (DataFrames, gráficos, métricas)

---

## 🎨 Design System

### Paleta de Cores (Shadcn/UI HSL)

- **Background:** `#f8fafc` (Slate 50)
- **Foreground:** `#0f172a` (Slate 900)
- **Cards:** Branco com borda `#e2e8f0`
- **Hover:** Background `#f1f5f9` + translateX(4px)

### Tipografia

- **Fonte:** Inter (Google Fonts)
- **Pesos:** 300, 400, 500, 600, 700
- **Títulos:** 1.6rem, peso 700, letter-spacing -0.04em

### Componentes Premium

- **Cards:** Border-radius 0.6rem, sombra dupla, hover effect
- **Tabs:** Estilo "pill" (fundo cinza, ativa branca)
- **Buttons:** Full-width na sidebar, auto-width no footer
- **Scrollbar:** Oculta na sidebar, padrão do OS no main

---

## 🔬 Pipeline de Dados

### 1. Fonte de Dados

- **Dataset:** Historical Product Demand (Kaggle - Felix Zhao)
- **Período:** 2011-2017 (filtrado para 2012-2017)
- **Granularidade:** Diária → Reamostragem semanal

### 2. Transformações (Method Chaining)

```python
df_tratado = (
    df_raw.copy()
    .assign(
        Date = lambda x: pd.to_datetime(x['Date'], format="%Y/%m/%d"),
        Order_Demand = lambda x: (
            x['Order_Demand']
            .astype(str)
            .str.replace(r'[\(\)]', '', regex=True)
            .astype(int)
        )
    )
    .dropna(subset=['Date'])
    .query("Date >= '2012-01-01' and Date <= '2017-01-01'")
    .sort_values('Date')
)
```

### 3. Agregação

- **Groupby:** Soma diária por categoria
- **Resample:** Frequência semanal (`'W'`)
- **Foco:** Categoria top 1 (83% do volume)

---

## 🤖 Modelos Implementados

### Modelo 1: Regressão Linear (Baseline)

**Features Engineered:**

- **Tendência:** Índice sequencial + média da demanda
- **Sazonalidade:** `np.sin(2 * π * month / 12)`

**Pipeline:**

```python
Pipeline([
    ("scaler", StandardScaler()),
    ("regressor", LinearRegression())
])
```

### Modelo 2: ETS (Exponential Smoothing)

**Configuração:**

- **Tendência:** Aditiva (`trend="add"`)
- **Sazonalidade:** Aditiva (`seasonal="add"`)
- **Período:** 52 semanas (sazonalidade anual)

**Treinamento:**

```python
ExponentialSmoothing(
    df_treino.Order_Demand,
    trend="add",
    seasonal="add",
    seasonal_periods=52
).fit(optimized=True)
```

### Split Temporal

- **Treino:** Até 2015-01-01
- **Teste:** Após 2015-01-01

---

## � Métricas de Avaliação

### Métricas Calculadas

| Métrica  | Descrição               | Objetivo                                       |
| -------- | ----------------------- | ---------------------------------------------- |
| **ME**   | Mean Error              | Detectar viés (sub/super estimação)            |
| **MAE**  | Mean Absolute Error     | Magnitude média do erro                        |
| **RMSE** | Root Mean Squared Error | Penaliza grandes desvios (métrica prioritária) |

### Visualização Comparativa

Gráfico de linha com 3 séries:

- **Real:** `#10b981` (verde) - linha sólida
- **Regressão Linear:** `#ef4444` (vermelho) - tracejado
- **ETS:** `#3b82f6` (azul) - tracejado

---

## 🎓 Metodologia CRISP-DM

### 6 Fases Implementadas

1. **Business Understanding** → Seção 1 (Projeto)
2. **Data Understanding** → Seções 4-6 (Coleta, Tratamento, EDA)
3. **Data Preparation** → Seção 5 (Method Chaining, Resample)
4. **Modeling** → Seção 7 (RL + ETS)
5. **Evaluation** → Seção 8 (MAE, RMSE, Comparação)
6. **Deployment** → Seção 9 (Comunicação de Resultados)

---

## 💡 Insights Estratégicos

### Descobertas do EDA

- **Lei de Pareto:** 1 categoria representa **83% do volume total**
- **Sazonalidade:** Ciclo anual de 52 semanas (detectado via STL)
- **Tendência:** Crescimento moderado no período 2012-2017

### Recomendações de Negócio (Simuladas)

- **Economia:** R$ 1.2M (redução de ruptura de estoque)
- **Eficiência:** +12% (melhoria no giro de estoque)
- **Nível de Serviço:** 98.5% (target atingido)

---

## 🔧 Configurações Avançadas

### Caching (Performance)

Funções cacheadas com `@st.cache_data`:

- `load_dataset()` - Evita reload do CSV
- `clean_data()` - Evita reprocessamento

### Responsividade

- **Layout:** Wide mode (`layout="wide"`)
- **Max-Width:** 1200px (conteúdo principal)
- **Sidebar:** Colapsável (logo dinâmica no header)

### Acessibilidade

- **Contraste:** WCAG AA compliant
- **Scrollbar:** Sistema operacional padrão (main page)
- **Navegação:** Teclado-friendly (Streamlit nativo)

---

## 🏗️ Organização do Código

### Modularização

O projeto segue uma **modularização mínima** para melhor organização:

- **`scripts/data_utils.py`**: Funções de carregamento e limpeza de dados
  - `load_dataset()`: Carrega o CSV do Kaggle
  - `clean_data()`: Pipeline de transformação (Method Chaining)
  - Ambas com `@st.cache_data` para performance

- **`scripts/main_app.py`**: Interface Streamlit e lógica de apresentação
  - Navegação entre seções
  - Visualizações e gráficos
  - Tabs didáticas (Explicação, Código, Resultado)

### Âncoras de Navegação

O código usa **banners visuais** para facilitar navegação no editor:

```python
# ==============================================================================
# SEÇÃO 6: ANÁLISE EXPLORATÓRIA - EDA (CRISP-DM: Data Understanding)
# ==============================================================================
```

**Como usar:**

- `Ctrl+F` → Digite "SEÇÃO 7" → Vai direto para Modelagem
- `Ctrl+Shift+O` (VS Code) → Veja a estrutura do arquivo

---

## 📝 Documentação Adicional

- **[PRD.md](doc/PRD.md):** Especificação completa do produto (design, funcionalidades, roadmap)
- **[main_app.py](scripts/main_app.py):** Código-fonte comentado da aplicação

---

## 🤝 Contribuindo

Este é um projeto educacional. Sugestões de melhoria são bem-vindas:

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/melhoria`)
3. Commit suas mudanças (`git commit -m 'Adiciona feature X'`)
4. Push para a branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais como parte do curso **"Como Pensar com Dados"** da Análise Macro.

---

## 👤 Autor

**Sabrina Pinheiro**  
🌐 [spdev.com.br](https://www.spdev.com.br)  
📧 Contato via website

---

## 🙏 Agradecimentos

- **Análise Macro** - Curso "Como Pensar com Dados"
- **Kaggle** - Dataset (Felix Zhao)
- **Shadcn/UI** - Inspiração de design
- **Streamlit** - Framework web

---

<div align="center">

**Desenvolvido com ❤️ usando Python, Streamlit e muita Ciência de Dados**

</div>
