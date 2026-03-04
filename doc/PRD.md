# PRD: Analytics Dashboard - Pipeline de Previsão de Demanda

## 1. Visão Geral do Produto

### 1.1 Contexto de Negócio

Uma **empresa de manufatura global** com múltiplos centros de distribuição enfrenta **ineficiência logística crítica**, resultando em:

- Custos elevados de armazenagem
- Rupturas de estoque em momentos críticos
- Processos manuais e intuitivos de planejamento

### 1.2 Objetivo do Produto

Desenvolver um **Analytics Dashboard interativo** que implemente um pipeline automatizado de previsão de demanda seguindo a metodologia **CRISP-DM** (Cross-Industry Standard Process for Data Mining), substituindo processos manuais por modelos estatísticos robustos.

### 1.3 Público-Alvo

- **Primário:** Cientistas de Dados e Analistas de Negócio
- **Secundário:** Gestores de Supply Chain e Stakeholders Executivos

### 1.4 Proposta de Valor

- **Educacional:** Demonstração didática e transparente de um pipeline completo de Data Science
- **Operacional:** Ferramenta de análise e previsão de demanda com interface premium
- **Metodológica:** Implementação rigorosa do ciclo CRISP-DM com rastreabilidade total

---

## 2. Especificações de Design e UX

### 2.1 Identidade Visual (Premium React/Next.js Inspired)

#### Paleta de Cores (HSL-Based)

- **Background Principal:** `#f8fafc` (Slate 50)
- **Foreground:** `#0f172a` (Slate 900)
- **Cards:** Fundo branco com borda `#e2e8f0` (Slate 200)
- **Accent/Primary:** `#0f172a` (Slate 900)
- **Secondary:** `#f1f5f9` (Slate 100)
- **Muted Text:** `#64748b` (Slate 500)

#### Tipografia

- **Fonte:** Inter (Google Fonts) - pesos 300, 400, 500, 600, 700
- **Títulos de Card:** 1.6rem, peso 700, letter-spacing -0.04em
- **Descrições:** 0.95rem, line-height 1.6

#### Componentes UI

- **Border Radius:** 0.6rem (variável CSS `--radius`)
- **Sombras:**
  - Padrão: `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)`
  - Hover: `0 10px 15px -3px rgb(0 0 0 / 0.1)`
- **Transições:** `all 0.2s cubic-bezier(0.4, 0, 0.2, 1)`

### 2.2 Arquitetura de Layout

#### Sidebar (Navegação)

- **Largura:** Expansível/Colapsável (padrão Streamlit)
- **Background:** Branco puro
- **Borda Direita:** 1.5px solid `#f1f5f9`
- **Scrollbar:** Completamente oculta (overflow: hidden + scrollbar-width: none)
- **Padding Top:** 1rem (logo posicionada próxima ao topo)
- **Logo:** Imagem responsiva (use_container_width=True)
- **Separador:** Linha horizontal (`st.markdown("---")`) após a logo
- **Botões de Navegação:**
  - Largura: 100% (full-width)
  - Alinhamento: Esquerda (text-align: left)
  - Hover: Background `#f1f5f9` + deslocamento de 4px para direita
  - Ícones: Material Symbols (silhouette style)

#### Header Principal

- **Componente:** Card Shadcn-style
- **Logo Dinâmica:** Aparece no header quando sidebar está colapsada (CSS `:has()` selector)
- **Título:** "Pipeline de Previsão de Demanda"
- **Subtítulo:** "Analytics Dashboard | Metodologia CRISP-DM"

#### Área de Conteúdo

- **Max-Width:** 1200px
- **Padding:** 2rem (top), 5rem (left/right)
- **Centralização:** margin auto

#### Footer de Navegação

- **Layout:** 2 colunas iguais (st.columns(2))
- **Container:** Classe CSS `.footer-nav-container` com max-width 1200px
- **Alinhamento:**
  - Coluna 1 (Anterior): justify-content: flex-start
  - Coluna 2 (Próximo): justify-content: flex-end
- **Botões:** width: auto (ajusta ao conteúdo), mesmo hover effect da sidebar
- **Separador:** Linha horizontal acima do footer

### 2.3 Sistema de Navegação

#### Estrutura de Seções (9 Etapas CRISP-DM)

```python
SECTION_ORDER = [
    "projeto",           # 1. Visão Geral
    "bibliotecas",       # 2. Tech Stack
    "config_ambiente",   # 3. Configurações
    "coleta_dados",      # 4. Data Ingestion
    "tratamento_dados",  # 5. Data Wrangling
    "eda",               # 6. Exploratory Data Analysis
    "modelo_preditivo",  # 7. Modeling
    "avaliacao",         # 8. Evaluation
    "comunicacao"        # 9. Deployment/Communication
]
```

#### Ícones Material Symbols

- `:material/dashboard:` - Projeto
- `:material/library_books:` - Bibliotecas
- `:material/settings:` - Configuração
- `:material/download:` - Coleta
- `:material/cleaning_services:` - Tratamento
- `:material/analytics:` - EDA
- `:material/psychology:` - Modelagem
- `:material/rule:` - Avaliação
- `:material/campaign:` - Comunicação

### 2.4 Padrão de Conteúdo (Tabs Didáticas)

Cada seção técnica (2-8) deve seguir o padrão de **3 abas**:

```python
st.tabs([
    ":material/description: Explicação",  # Teoria e contexto
    ":material/code: Código",             # Código-fonte técnico
    ":material/visibility: Resultado"     # Output/Visualização
])
```

#### Estilização de Tabs

- **Container:** Background `#f1f5f9`, border-radius `calc(var(--radius) + 2px)`
- **Tab Ativa:** Background branco, box-shadow sutil
- **Altura:** 36px
- **Transição:** 0.2s ease

---

## 3. Especificações Técnicas

### 3.1 Stack Tecnológico

#### Core Framework

- **Streamlit:** `>=1.28.0` (Framework web principal)
- **streamlit-shadcn-ui:** Componentes premium (badges, metric_card, table)

#### Manipulação de Dados

- **pandas:** `>=1.5.0` (DataFrames e séries temporais)
- **numpy:** `>=1.21.0` (Operações matemáticas)

#### Visualização

- **plotnine:** `>=0.10.0` (Grammar of Graphics - ggplot2 style)
- **matplotlib:** `>=3.5.0` (Backend de renderização)

#### Modelagem Estatística

- **statsmodels:** `>=0.13.0`
  - `STL` (Seasonal-Trend Decomposition using Loess)
  - `ExponentialSmoothing` (Holt-Winters)
- **scikit-learn:** `>=1.0.0`
  - `Pipeline` (Encadeamento de transformações)
  - `StandardScaler` (Normalização)
  - `LinearRegression` (Modelo baseline)

### 3.2 Configuração da Aplicação

#### Page Config

```python
st.set_page_config(
    page_title="Pipeline de Previsão de Demanda",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

#### Configurações Globais

```python
pd.options.display.float_format = '{:.2f}'.format
warnings.filterwarnings('ignore')
```

### 3.3 Arquitetura de Dados

#### Fonte de Dados

- **Dataset:** Historical Product Demand (Kaggle - Felix Zhao)
- **Formato:** CSV (suporte a compressão ZIP)
- **Localização:** `data/Historical Product Demand.csv`

#### Pipeline de Transformação (Method Chaining)

```python
@st.cache_data
def clean_data(df):
    return (
        df.copy()
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

#### Agregação Temporal

- **Granularidade Original:** Diária
- **Reamostragem:** Semanal (`'W'`) para suavizar volatilidade
- **Período de Análise:** 2012-2017 (5 anos)

---

## 4. Especificações Funcionais por Seção

### 4.1 Seção 1: Visão Geral do Projeto

**Objetivo:** Apresentar o contexto de negócio e a metodologia CRISP-DM

**Componentes:**

- **1.1 Cenário:** Descrição do problema de ineficiência logística
  - Metric Card: "Problema - Ineficiência Logística"
- **1.2 Objetivo de Negócio:** Meta de automação do pipeline
  - Metric Card: "Meta - Automação do Pipeline"
- **1.3 Insight Estratégico:** Lei de Pareto (83% do volume em 1 categoria)
- **1.4 Metodologia:** Explicação das 6 etapas do CRISP-DM

### 4.2 Seção 2: Bibliotecas

**Objetivo:** Documentar o tech stack e justificar cada escolha

**Estrutura de Tabs:**

- **Explicação:** Descrição detalhada de cada biblioteca e seu papel
  - Pandas & Numpy (Computação científica)
  - Plotnine (Grammar of Graphics)
  - Statsmodels (STL e Holt-Winters)
  - Scikit-Learn (Pipeline e LinearRegression)
- **Código:** Bloco de imports comentado
- **Resultado:**
  - Badges com nomes das bibliotecas (ui.badges)
  - Mensagem de sucesso (st.success)

### 4.3 Seção 3: Configurações de Ambiente

**Objetivo:** Parametrização global para legibilidade e limpeza

**Estrutura de Tabs:**

- **Explicação:** Justificativa das configurações (float format, warnings)
- **Código:**
  ```python
  pd.options.display.float_format = '{:.2f}'.format
  warnings.filterwarnings('ignore')
  ```
- **Resultado:** Mensagem informativa sobre a aplicação

### 4.4 Seção 4: Coleta de Dados

**Objetivo:** Ingestão do dataset bruto

**Estrutura de Tabs:**

- **Explicação:** Fonte dos dados (Kaggle), método de leitura
- **Código:** `pd.read_csv()` com suporte a ZIP
- **Resultado:**
  - DataFrame (primeiras 5 linhas)
  - Tabela de métricas (Total de Linhas, Total de Colunas)

### 4.5 Seção 5: Tratamento de Dados

**Objetivo:** Limpeza e transformação via Method Chaining

**Estrutura de Tabs:**

- **Explicação:** Etapas de conversão temporal, limpeza de regex, tipagem
- **Código:** Pipeline completo de `.assign()` com lambdas
- **Resultado:**
  - DataFrame tratado (primeiras 10 linhas)
  - Tabela de verificação de tipos (dtypes)

### 4.6 Seção 6: Análise Exploratória (EDA)

**Objetivo:** Investigação profunda dos dados com 9 sub-blocos

**Sub-blocos (cada um com 3 tabs):**

1. **6.1 Contagem de Produtos:** `df.Product_Code.nunique()`
2. **6.2 Contagem de Categorias:** `df.Product_Category.nunique()`
3. **6.3 Resumo Estatístico:** `df.describe(include='all')`
4. **6.4 Volume por Categoria:** Gráfico de barras (matplotlib)
   - Cores: `plt.cm.coolwarm` (palette suavizada)
   - Estilo: Bordas removidas, grid suave
5. **6.5 Seleção e Agregação Temporal:**
   - Drill-down na categoria top 1
   - Agrupamento diário → Reamostragem semanal
   - Filtro 2012-2017
6. **6.6 Série Temporal:** Line plot (plotnine)
   - Cor: `#2563eb` (azul técnico)
   - Tema: minimal
7. **6.7 Estatística da Série:** `df_alvo.describe()`
8. **6.8 Histograma:** Distribuição de demanda (plotnine)
   - Fill: steelblue, 30 bins
9. **6.9 Decomposição STL:**
   - Período: 52 semanas (sazonalidade anual)
   - Plot: 4 painéis (Observado, Tendência, Sazonalidade, Resíduo)

### 4.7 Seção 7: Modelagem Preditiva

**Objetivo:** Treinar e comparar 2 modelos (RL vs ETS)

**Sub-blocos (cada um com 3 tabs):**

1. **7.1 Engenharia de Features:**
   - Tendência: Índice sequencial + média
   - Sazonalidade: `np.sin(2 * np.pi * month / 12)`
2. **7.2 Split Treino/Teste:** Divisão temporal (até 2015-01-01)
3. **7.3 Treinamento RL:**
   ```python
   Pipeline([
       ("scaler", StandardScaler()),
       ("regressor", LinearRegression())
   ])
   ```
4. **7.4 Previsão RL:** `modelo_rl.predict()`
5. **7.5 Treinamento ETS:**
   ```python
   ExponentialSmoothing(
       df_treino.Order_Demand,
       trend="add",
       seasonal="add",
       seasonal_periods=52
   ).fit(optimized=True)
   ```
6. **7.6 Previsão ETS:** `modelo_ets.forecast(len(df_teste))`

### 4.8 Seção 8: Avaliação e Diagnóstico

**Objetivo:** Comparar performance dos modelos com métricas

**Sub-blocos (cada um com 3 tabs):**

1. **8.1 Consolidação:** DataFrame unificado (RL, ETS, Real)
2. **8.2 Comparação Visual:** Line plot com 3 séries
   - Cores: `#ef4444` (RL), `#3b82f6` (ETS), `#10b981` (Real)
   - Estilos: Tracejado para modelos, sólido para real
3. **8.3 Métricas de Performance:**
   - 2 colunas (st.columns(2))
   - Métricas: ME (Mean Error), MAE, RMSE
   - Formato: 2 casas decimais

### 4.9 Seção 9: Comunicação de Resultados

**Objetivo:** Apresentar recomendações de negócio

**Componentes:**

- **Card de Ação:** Borda verde à esquerda, recomendação estratégica
- **3 Metric Cards:**
  - Economia: R$ 1.2M (Redução de Ruptura)
  - Eficiência: +12% (Giro de Estoque)
  - Nível de Serviço: 98.5% (Target Atingido)

---

## 5. Requisitos de Performance

### 5.1 Caching

- **Funções Cacheadas:** `load_dataset()`, `clean_data()`
- **Decorator:** `@st.cache_data`
- **Objetivo:** Evitar reprocessamento em cada interação

### 5.2 Responsividade

- **Layout:** Wide mode (layout="wide")
- **Breakpoints:** Adaptação automática via Streamlit
- **Max-Width:** 1200px para conteúdo principal

### 5.3 Acessibilidade

- **Scrollbar:** Sistema operacional padrão (main page)
- **Sidebar:** Sem scrollbar (overflow hidden)
- **Contraste:** WCAG AA compliant (texto escuro em fundo claro)

---

## 6. Estrutura de Arquivos

```
AM_Projeto - Pipeline de Previsão de Demanda/
├── assets/
│   └── img/
│       └── logo.jpg                    # Logo do projeto
├── data/
│   └── Historical Product Demand.csv   # Dataset bruto
├── doc/
│   └── PRD.md                          # Este documento
├── scripts/
│   └── main_app.py                     # Aplicação Streamlit principal
└── requirements.txt                     # Dependências Python
```

---

## 7. Critérios de Aceitação

### 7.1 Design

- [ ] Interface segue paleta HSL Shadcn/UI
- [ ] Fonte Inter aplicada globalmente
- [ ] Cards com hover effect (sombra + borda)
- [ ] Tabs com estilo "pill" (fundo cinza, ativa branca)
- [ ] Botões com hover shift de 4px
- [ ] Logo dinâmica aparece quando sidebar colapsa
- [ ] Scrollbar da sidebar completamente oculta
- [ ] Footer de navegação alinhado com conteúdo (1200px)

### 7.2 Funcionalidade

- [ ] Navegação via sidebar funcional (9 seções)
- [ ] Footer de navegação (Anterior/Próximo) funcional
- [ ] Todas as seções carregam sem erro
- [ ] Gráficos renderizam corretamente (plotnine + matplotlib)
- [ ] Métricas calculadas com precisão (MAE, RMSE)
- [ ] Caching evita reprocessamento desnecessário

### 7.3 Conteúdo

- [ ] Cada seção técnica (2-8) tem 3 tabs (Explicação, Código, Resultado)
- [ ] Código exibido é executável e comentado
- [ ] Explicações são didáticas e contextualizadas
- [ ] Resultados mostram outputs reais (não mockups)
- [ ] Narrativa segue metodologia CRISP-DM fielmente

### 7.4 Performance

- [ ] Carregamento inicial < 3 segundos
- [ ] Navegação entre seções instantânea (cache)
- [ ] Gráficos renderizam em < 1 segundo
- [ ] Sem memory leaks em sessões longas

---

## 8. Roadmap de Desenvolvimento

### Fase 1: Fundação (Semana 1)

- [ ] Setup do ambiente (venv, requirements.txt)
- [ ] Estrutura de arquivos e pastas
- [ ] Configuração do Streamlit (page_config)
- [ ] Sistema de CSS customizado (Shadcn/UI palette)

### Fase 2: Navegação e Layout (Semana 2)

- [ ] Sidebar com logo e botões de navegação
- [ ] Sistema de state management (st.session_state)
- [ ] Footer de navegação (Anterior/Próximo)
- [ ] Header dinâmico com logo colapsável

### Fase 3: Pipeline de Dados (Semana 3)

- [ ] Função de carregamento com cache
- [ ] Pipeline de limpeza (Method Chaining)
- [ ] Agregação temporal (resample semanal)
- [ ] Seleção automática da categoria top 1

### Fase 4: Conteúdo Didático (Semana 4-5)

- [ ] Seção 1: Visão Geral (texto + metric cards)
- [ ] Seção 2-3: Bibliotecas e Configurações (tabs)
- [ ] Seção 4-5: Coleta e Tratamento (tabs + dataframes)
- [ ] Seção 6: EDA completa (9 sub-blocos com gráficos)

### Fase 5: Modelagem (Semana 6)

- [ ] Feature engineering (tendência + sazonalidade)
- [ ] Split treino/teste temporal
- [ ] Treinamento RL (Pipeline + StandardScaler)
- [ ] Treinamento ETS (Holt-Winters)
- [ ] Previsões e consolidação

### Fase 6: Avaliação e Comunicação (Semana 7)

- [ ] Cálculo de métricas (ME, MAE, RMSE)
- [ ] Gráfico comparativo (Real vs Modelos)
- [ ] Seção de comunicação (cards de impacto)
- [ ] Rodapé com créditos

### Fase 7: Refinamento e Testes (Semana 8)

- [ ] Ajustes de CSS (alinhamentos, espaçamentos)
- [ ] Testes de responsividade
- [ ] Validação de cálculos
- [ ] Documentação final (README.md)

---

## 9. Métricas de Sucesso

### 9.1 Métricas Técnicas

- **Acurácia do Modelo:** RMSE < 5000 unidades (baseline)
- **Performance:** Tempo de carregamento < 3s
- **Cobertura de Testes:** 100% das seções funcionais

### 9.2 Métricas de UX

- **Clareza:** 100% das seções com explicação + código + resultado
- **Navegabilidade:** Máximo 2 cliques para qualquer seção
- **Estética:** Design premium (Shadcn/UI compliance)

### 9.3 Métricas de Negócio (Simuladas)

- **Economia Projetada:** R$ 1.2M (redução de ruptura)
- **Eficiência:** +12% (giro de estoque)
- **Nível de Serviço:** 98.5% (target atingido)

---

## 10. Anexos

### 10.1 Referências

- **Metodologia:** CRISP-DM (Cross-Industry Standard Process for Data Mining)
- **Design System:** Shadcn/UI (https://ui.shadcn.com/)
- **Dataset:** Kaggle - Product Demand Forecasting (Felix Zhao)

### 10.2 Glossário

- **CRISP-DM:** Metodologia padrão da indústria para projetos de Data Mining
- **EDA:** Exploratory Data Analysis (Análise Exploratória de Dados)
- **ETS:** Error, Trend, Seasonality (modelo de suavização exponencial)
- **MAE:** Mean Absolute Error (Erro Médio Absoluto)
- **RMSE:** Root Mean Squared Error (Raiz do Erro Quadrático Médio)
- **STL:** Seasonal-Trend Decomposition using Loess
- **Method Chaining:** Técnica de encadeamento de métodos do Pandas

### 10.3 Contato

- **Desenvolvedor:** Sabrina Pinheiro
- **Website:** https://www.spdev.com.br
- **Curso:** Análise Macro - Como Pensar em Dados

---

## 11. Estrutura de Arquivos Implementada

```
AM_Projeto - Pipeline de Previsão de Demanda/
│
├── assets/
│   └── img/
│       └── logo.jpg              # Logo do projeto (sidebar + header + favicon)
│
├── data/
│   └── Historical Product Demand.csv
│
├── doc/
│   ├── PRD.md                    # Este documento
│   └── configuracao_ambiente.md  # Guia de setup do venv
│
├── scripts/
│   ├── data_utils.py             # Funções de dados (modularização mínima)
│   └── main_app.py               # Código principal Streamlit com lógica CRISP-DM
│
├── venv/                         # Ambiente virtual (não versionado)
│
├── requirements.txt              # Dependências Python
└── README.md                     # Documentação principal
```

### Organização do Código

**Modularização Mínima:**

- **`scripts/data_utils.py`**: Funções de carregamento e limpeza de dados
  - `load_dataset()`: Carrega o CSV do Kaggle com `@st.cache_data`
  - `clean_data()`: Pipeline de transformação (Method Chaining)
- **`scripts/main_app.py`**: Interface Streamlit e lógica de apresentação
  - Navegação entre 9 seções CRISP-DM
  - Visualizações e gráficos
  - Tabs didáticas (Explicação, Código, Resultado)

**Âncoras de Navegação:**
O código usa banners visuais de 80 caracteres para facilitar navegação no editor:

```python
# ==============================================================================
# SEÇÃO 6: ANÁLISE EXPLORATÓRIA - EDA (CRISP-DM: Data Understanding)
# ==============================================================================
```

**Benefícios:**

- Navegação rápida via `Ctrl+F` (busque por "SEÇÃO 7")
- Separação clara de responsabilidades (dados vs UI)
- Reutilização de funções de dados
- Testabilidade (funções isoladas em data_utils.py)
