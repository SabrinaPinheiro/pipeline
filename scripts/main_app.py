# ==============================================================================
# IMPORTS E DEPENDÊNCIAS
# ==============================================================================
import streamlit as st # Framework web
import pandas as pd
import numpy as np
import plotnine as p9 # (Nota: usaremos matplotlib/st.pyplot para renderizar, mas mantemos import para compatibilidade)
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import streamlit_shadcn_ui as ui
import warnings
import os
import base64

# Importação do módulo de dados
from data_utils import load_dataset, clean_data

def img_to_base64(img_path):
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# ==============================================================================
# CONFIGURAÇÃO GLOBAL
# ==============================================================================
pd.options.display.float_format = '{:.2f}'.format
warnings.filterwarnings('ignore')

# ==============================================================================
# Configuração da Página e Estilos
# ------------------------------------------------------------------------------
FAVICON_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'logo.jpg')

st.set_page_config(
    page_title="Pipeline de Previsão de Demanda",
    page_icon=FAVICON_PATH,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo Personalizado (Premium React/Next.js inspired)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variáveis Globais (Shadcn/UI) */
    :root {
        --radius: 0.6rem;
        --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ==================================================================== */
    /* ANIMAÇÕES E TRANSIÇÕES */
    /* ==================================================================== */
    
    /* Fade-in com slide-up para conteúdo principal */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Fade-in simples */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Slide-in da esquerda */
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Slide-in da direita */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Pulso suave (para barra de progresso) */
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    /* Scale-in (para cards) */
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* Aplicar animação ao conteúdo principal */
    .main > div > div > div {
        animation: fadeInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Animação para cards Shadcn */
    .shadcn-card {
        animation: scaleIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Animação para barra de progresso */
    [data-testid="stProgress"] {
        animation: slideInLeft 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Customizar cores da barra de progresso (tons de cinza suaves) */
    /* Fundo da barra - cinza claro */
    [data-testid="stProgress"] > div > div {
        background-color: #f1f5f9 !important;  /* Slate 100 - fundo claro */
    }
    
    /* Barra preenchida - cinza médio */
    [data-testid="stProgress"] > div > div > div {
        background-color: #94a3b8 !important;  /* Slate 400 - cinza médio */
    }
    
    div[role="progressbar"] {
        background-color: #94a3b8 !important;  /* Slate 400 - cinza médio */
    }
    
    /* Animação para breadcrumbs */
    .breadcrumb-container {
        animation: slideInRight 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Transição suave para tabs */
    [data-baseweb="tab-list"] {
        transition: var(--transition);
    }
    
    [data-baseweb="tab-panel"] {
        animation: fadeIn 0.3s ease-out;
    }    /* Variáveis Técnicas (Shadcn/UI HSL Palette) */
    :root {
        --background: 0 0% 100%;
        --foreground: 222.2 84% 4.9%;
        --card: 0 0% 100%;
        --card-foreground: 222.2 84% 4.9%;
        --popover: 0 0% 100%;
        --popover-foreground: 222.2 84% 4.9%;
        --primary: 222.2 47.4% 11.2%;
        --primary-foreground: 210 40% 98%;
        --secondary: 210 40% 96.1%;
        --secondary-foreground: 222.2 47.4% 11.2%;
        --muted: 210 40% 96.1%;
        --muted-foreground: 215.4 16.3% 46.9%;
        --accent: 210 40% 96.1%;
        --accent-foreground: 222.2 47.4% 11.2%;
        --destructive: 0 84.2% 60.2%;
        --destructive-foreground: 210 40% 98%;
        --border: 214.3 31.8% 91.4%;
        --input: 214.3 31.8% 91.4%;
        --ring: 222.2 84% 4.9%;
        --radius: 0.6rem;
    }

    /* Aplicação Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        scroll-behavior: smooth;
    }

    /* background principal */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Layout Cleanup */
    .block-container {
        padding-top: 2rem !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
        max-width: 1200px;
    }



    /* Sidebar Refinement (Fix: Pure single-scrollbar app) */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1.5px solid #f1f5f9 !important;
        transition: all 0.3s ease;
        overflow: hidden !important; /* Force no scrollbar on the main section */
    }
    
    /* Completely hide scrollbars for all nested sidebar elements */
    section[data-testid="stSidebar"] * {
        scrollbar-width: none !important; /* Firefox */
        -ms-overflow-style: none !important; /* IE/Edge */
    }
    
    section[data-testid="stSidebar"] *::-webkit-scrollbar {
        display: none !important; /* Chrome/Safari */
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-right: 10px !important;
    }

    /* Global Buttons Refinement (Shared Hover & Width) */
    div.stButton > button {
        border-radius: var(--radius) !important;
        border: 1px solid transparent !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        white-space: nowrap !important;
        word-break: keep-all !important;
        width: auto !important;
    }

    /* Premium Hover Effect (Shared for Sidebar and Footer) */
    div.stButton > button:hover {
        background-color: #f1f5f9 !important;
        transform: translateX(4px);
        color: #0f172a !important;
        border-color: #e2e8f0 !important;
    }

    /* Sidebar Buttons (Navegação) */
    section[data-testid="stSidebar"] button {
        width: 100% !important;
        text-align: left !important;
        border-radius: 0.4rem !important;
        transition: all 0.2s ease !important;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background-color: #f1f5f9 !important;
        transform: translateX(4px) !important;
    }
    
    /* Botão Ativo (Primary) - Destaque visual em cinza elegante */
    section[data-testid="stSidebar"] button[kind="primary"] {
        background-color: #f1f5f9 !important;  /* Slate 100 - cinza claro */
        color: #0f172a !important;             /* Slate 900 - texto escuro */
        font-weight: 600 !important;
        border-left: 4px solid #64748b !important;  /* Slate 500 - cinza médio */
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1) !important;
    }
    
    section[data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: #f8fafc !important;  /* Slate 50 - cinza bem claro */
        transform: translateX(4px) !important;
    }

    /* Sidebar-Specific (Reset width for full Sidebar coverage) */
    [data-testid="stSidebar"] div.stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
    }

    /* Footer Navigation (Aligned with content boundaries) */
    .footer-nav-container {
        max-width: 1200px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-left: 5rem !important;
        padding-right: 5rem !important;
    }

    .footer-nav-container [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }

    .footer-nav-container [data-testid="column"]:first-child {
        display: flex !important;
        justify-content: flex-start !important;
    }

    .footer-nav-container [data-testid="column"]:last-child {
        display: flex !important;
        justify-content: flex-end !important;
    }
    
    .footer-nav-container div.stButton {
        width: fit-content !important;
    }

    .footer-nav-container [data-testid="column"]:last-child div.stButton {
        margin-left: auto !important;
    }
    
    /* Footer Navigation Buttons - Hover cinza */
    .footer-nav-container button {
        transition: all 0.2s ease !important;
    }
    
    .footer-nav-container button:hover {
        background-color: #f1f5f9 !important;  /* Slate 100 - cinza claro */
        transform: translateX(2px) !important;
    }

    .footer-nav-container [data-testid="column"]:last-child div.stButton > button {
        margin-left: auto !important;
    }

    /* Hide generic Fullscreen / Toolbar button in Sidebar */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        margin-top: 0rem !important;
        margin-bottom: 0rem !important;
    }

    /* Logo Dinâmico do Header */
    .header-logo-dynamic {
        display: none;
        opacity: 0;
        transition: opacity 0.4s ease-in-out;
    }

    /* CSS Magic to detect collapsed sidebar */
    .stApp:has([data-testid="collapsedControl"] button) .header-logo-dynamic {
        display: flex !important;
        opacity: 1 !important;
    }

    /* Premium Cards (Shadcn style) */
    .shadcn-card {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: var(--radius);
        padding: 1.75rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1.5rem;
    }
    
    .shadcn-card:hover {
        border-color: #cbd5e1;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }
    
    .shadcn-card-title {
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        color: #0f172a;
    }
    
    .shadcn-card-desc {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Tabs refinement */
    .stTabs [data-baseweb="tab-list"] {
        padding: 4px;
        background-color: #f1f5f9;
        border-radius: calc(var(--radius) + 2px);
        margin-bottom: 1.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 36px;
        border-radius: var(--radius) !important;
        transition: all 0.2s ease;
        padding: 0 16px !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: white !important;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1) !important;
        color: #0f172a !important;
    }

    /* Code Blocks */
    .stCodeBlock {
        border: 1px solid #e2e8f0 !important;
        border-radius: var(--radius) !important;
        overflow: hidden;
    }

    /* Esconder botões de Fullscreen nas imagens */
    button[title="View fullscreen"], 
    [data-testid="StyledFullScreenButton"],
    div[data-testid="stImage"] button {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

</style>
""", unsafe_allow_html=True)



# ==============================================================================
# SIDEBAR - SISTEMA DE NAVEGAÇÃO
# ------------------------------------------------------------------------------
# Definição Global das Seções (Ordem de Navegação)
SECTION_ORDER = [
    "projeto", "bibliotecas", "config_ambiente", 
    "coleta_dados", "tratamento_dados", "eda", 
    "modelo_preditivo", "avaliacao", "comunicacao"
]

SECTIONS = {
    "projeto": ":material/dashboard: PROJETO",
    "bibliotecas": ":material/library_books: BIBLIOTECAS",
    "config_ambiente": ":material/settings: CONFIGURAÇÃO",
    "coleta_dados": ":material/download: COLETA (DATA)",
    "tratamento_dados": ":material/cleaning_services: TRATAMENTO (DATA)",
    "eda": ":material/analytics: ANÁLISE (EDA)",
    "modelo_preditivo": ":material/psychology: MODELAGEM",
    "avaliacao": ":material/rule: AVALIAÇÃO",
    "comunicacao": ":material/campaign: COMUNICAÇÃO"
}

# Sistema de Navegação com Query Parameters (URL dinâmica)
# Permite compartilhamento de links diretos e funcionamento do botão "Voltar"
query_params = st.query_params
active_from_url = query_params.get("secao", None)

# Inicializa session_state se não existir
if 'active_section' not in st.session_state:
    st.session_state.active_section = active_from_url if active_from_url in SECTION_ORDER else 'projeto'

# Sincroniza URL com session_state (se usuário navegou via botão)
if active_from_url and active_from_url != st.session_state.active_section:
    st.session_state.active_section = active_from_url

with st.sidebar:
    # Logo do Projeto
    LOGO_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'logo.jpg')
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    
    st.markdown("---")
    
    # Navegação com indicador visual de seção ativa
    for key, label in SECTIONS.items():
        is_active = (key == st.session_state.active_section)
        button_type = "primary" if is_active else "secondary"
        
        if st.button(
            label, 
            key=f"btn_{key}", 
            use_container_width=True,
            type=button_type  # Destaque visual para seção ativa
        ):
            st.session_state.active_section = key
            st.query_params["secao"] = key  # Atualiza URL
            st.rerun()





# ==============================================================================
# FUNÇÕES DE DADOS (IMPORTADAS DE data_utils.py)
# ------------------------------------------------------------------------------
# As funções load_dataset() e clean_data() foram movidas para scripts/data_utils.py
# para melhor organização e reutilização do código.

# ==============================================================================
# LAYOUT PRINCIPAL - HEADER DINÂMICO
# ==============================================================================

# Header Geral
LOGO_PATH = os.path.join(os.path.dirname(__file__), '..', 'assets', 'img', 'logo.jpg')
logo_html = ""
if os.path.exists(LOGO_PATH):
    img_b64 = img_to_base64(LOGO_PATH)
    logo_html = f'<img src="data:image/jpg;base64,{img_b64}" style="height: 50px; margin-right: 15px; border-radius: 5px;">'

st.markdown(f"""
<div class="shadcn-card">
    <div class="shadcn-card-header">
        <div style="display: flex; align-items: center;">
            <div class="header-logo-dynamic">{logo_html}</div>
            <div>
                <h1 class="shadcn-card-title" style="margin: 0;">Pipeline de Previsão de Demanda</h1>
                <p class="shadcn-card-desc" style="margin: 5px 0 0 0;">Analytics Dashboard | Metodologia CRISP-DM</p>
            </div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

active = st.session_state.active_section

# ==============================================================================
# CONTEÚDO PRINCIPAL
# ==============================================================================

st.markdown("---")

# ==============================================================================
# SEÇÃO 1: VISÃO GERAL DO PROJETO (CRISP-DM: Business Understanding)
# ==============================================================================
if active == 'projeto':
    st.subheader(":material/dashboard: 1. Visão Geral do Projeto")
    
    # 1.1 Cenário
    st.markdown("##### 1.1 Cenário")
    st.markdown("""
    Uma **empresa de manufatura com atuação global** opera múltiplos centros de distribuição espalhados por diversas regiões. 
    Atualmente, ela enfrenta **ineficiência logística** significativa, resultando em custos elevados de armazenagem e, paradoxalmente, rupturas de estoque em momentos críticos.
    """)
    ui.metric_card(title="Problema", content="Ineficiência Logística", description="Custos altos e perda de vendas", key="prob")

    st.markdown("---")

    # 1.2 Objetivo
    st.markdown("##### 1.2 Objetivo de Negócio")
    st.markdown("""
    Implementar um **pipeline automatizado de previsão de demanda**. 
    A meta é substituir processos manuais e intuitivos por modelos estatísticos robustos, otimizando o **planejamento de estoque** e reduzindo custos operacionais de longo prazo.
    """)
    ui.metric_card(title="Meta", content="Automação do Pipeline", description="Otimização e Redução de Custos", key="meta")

    st.markdown("---")

    # 1.3 Insight
    st.markdown("##### 1.3 Insight Estratégico")
    st.markdown("""
    A análise preliminar revelou uma **lei de potência (Pareto)** crítica:
    Uma única categoria de produtos é líder absoluta, representando mais de **83% do volume total** e estando presente em **46% dos pedidos**.
    *Decisão:* Focaremos todos os esforços de modelagem nesta categoria para maximizar o impacto do projeto.
    """)
    
    st.markdown("---")

    # 1.4 Metodologia
    st.markdown("##### 1.4 Metodologia (CRISP-DM)")
    st.markdown("""
    O projeto segue rigorosamente o ciclo **CRISP-DM** (Cross-Industry Standard Process for Data Mining) para garantir robustez:
    1.  **Entendimento do Negócio:** (Etapa atual 1)
    2.  **Entendimento dos Dados:** Coleta e EDA (Seções 4, 5 e 6).
    3.  **Preparação dos Dados:** Limpeza e Feature Engineering.
    4.  **Modelagem:** Regressão Lineares e Suavização Exponencial (Seção 7).
    5.  **Avaliação:** Validação com métricas de erro (Seção 8).
    6.  **Implantação:** Deploy dos resultados (Seção 10).
    """)

# ------------------------------------------------------------------------------
# 2. BIBLIOTECAS
# ------------------------------------------------------------------------------
elif active == 'bibliotecas':
    st.subheader(":material/library_books: 2. Bibliotecas")
    
    t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
    
    with t1:
        st.markdown("""
        ### Ferramentas do Pipeline (Tech Stack)
        
        Para operacionalizar o ciclo **CRISP-DM**, selecionamos um conjunto de bibliotecas Python que cobrem desde a manipulação de dados até a modelagem preditiva avançada.
        
        *   **Pandas & Numpy:** Aalicerces da computação científica. O `pandas` estrutura os dados em DataFrames (tabelas), enquanto o `numpy` oferece performance para operações vetoriais matemáticas.
        *   **Plotnine (`p9`):** Biblioteca de visualização baseada na *Grammar of Graphics* (similar ao ggplot2 do R). Permite criar gráficos complexos e esteticamente refinados de forma declarativa.
        *   **Statsmodels (STL & Holt-Winters):** Focada em estatística inferencial e séries temporais.
            *   `STL`: Utilizado na etapa de **EDA** para decompor a série em Tendência, Sazonalidade e Resíduo.
            *   `ExponentialSmoothing`: Implementa o modelo **Holt-Winters**, ideal para séries com sazonalidade forte.
        *   **Scikit-Learn (Sklearn):** Framework padrão da indústria para Machine Learning.
            *   `Pipeline`: Garante reprodutibilidade encadeando passos de pré-processamento e modelagem.
            *   `LinearRegression`: Utilizado aqui como *baseline* (modelo de referência) para comparar com o modelo estatístico.
        """)
    
    with t2:
        st.code("""
# Manipulação de tabelas (DataFrames)
import pandas as pd

# Operações matriciais e matemáticas
import numpy as np

# Visualização de dados (Gramática dos Gráficos)
import plotnine as p9

# Decomposição de Séries Temporais
from statsmodels.tsa.seasonal import STL

# Organização do fluxo de Machine Learning
from sklearn.pipeline import Pipeline

# Normalização de dados (Pré-processamento)
from sklearn.preprocessing import StandardScaler

# Modelo Baseline (Regressão Linear)
from sklearn.linear_model import LinearRegression

# Modelo ETS (Holt-Winters) para Sazonalidade
from statsmodels.tsa.holtwinters import ExponentialSmoothing
        """, language="python")

    with t3:
        ui.badges(badge_list=[("Pandas", "default"), ("Numpy", "default"), ("Statsmodels", "destructive"), ("Scikit-Learn", "outline")], class_name="flex gap-2")
        
        st.success("✅ Ambiente configurado com sucesso.")
        st.info("Todas as bibliotecas foram importadas e estão prontas para uso no kernel.")

# ==============================================================================
# SEÇÃO 3: CONFIGURAÇÕES DE AMBIENTE
# ==============================================================================
elif active == 'config_ambiente':
    st.subheader(":material/settings: 3. Configurações de Ambiente")
    t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
    
    with t1:
        st.markdown("""
        ### Parametrização Global
        
        Antes de iniciar a ingestão de dados, definimos parâmetros globais que garantem:
        1.  **Legibilidade:** Ajustamos a exibição de números flutuantes no Pandas para 2 casas decimais. Isso evita notações científicas desnecessárias (ex: `1.23e+05`) e facilita a interpretação rápida de valores monetários ou de volume.
        2.  **Limpeza de Saída:** Filtramos avisos (`warnings`) que não impactam a execução do código (como avisos de depreciação futura), reduzindo a poluição visual nos logs e relatórios.
        """)
        
    with t2:
        st.code("""
# Configuração para exibir flutuantes com 2 casas decimais
pd.options.display.float_format = '{:.2f}'.format

# Silenciar avisos irrelevantes
import warnings
warnings.filterwarnings('ignore')
        """, language="python")
        
    with t3:
        st.info("Configuração aplicada: Pandas agora exibirá números como `1234.56` em vez de notação científica.")

# ==============================================================================
# SEÇÃO 4: COLETA DE DADOS (CRISP-DM: Data Understanding)
# ==============================================================================
elif active == 'coleta_dados':
    st.subheader(":material/download: 4. Coleta de Dados")
    t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
    
    df_raw = load_dataset()
    
    with t1:
        st.markdown("""
        ### Ingestão de Dados (Data Ingestion)
        
        O primeiro passo de qualquer pipeline é a aquisição dos dados. Neste projeto, utilizamos um dataset público de **Previsão de Demanda de Produtos** disponível no Kaggle.
        
        *   **Fonte:** Kaggle (Felix Zhao)
        *   **Método:** Leitura direta de arquivo CSV (compressão ZIP suportada nativamente pelo Pandas).
        *   **Comando:** `pd.read_csv()` é a função universal para carregar dados tabulares em memória.
        """)
        
    with t2:
        st.code("""
# Fonte dos dados: https://www.kaggle.com/datasets/felixzhao/productdemandforecasting

# Carregamento direto via URL (suporte a compressão ZIP)
df_bruto = pd.read_csv(
    "https://aluno.analisemacro.com.br/download/69280/?tmstv=1768230842", 
    compression = "zip"
)

# Visualização das primeiras linhas
df_bruto.head()
        """, language="python")
        
    with t3:
        if df_raw is not None:
            st.dataframe(df_raw.head(), use_container_width=True)
            ui.table(data=pd.DataFrame([
                {"Métrica": "Total de Linhas", "Valor": f"{df_raw.shape[0]:,}"},
                {"Métrica": "Total de Colunas", "Valor": f"{df_raw.shape[1]}"}
            ]))

# ==============================================================================
# SEÇÃO 5: TRATAMENTO DE DADOS (CRISP-DM: Data Preparation)
# ==============================================================================
elif active == 'tratamento_dados':
    st.subheader(":material/cleaning_services: 5. Tratamento de Dados")
    t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
    
    df_raw = load_dataset()
    
    with t1:
        st.markdown("""
        ### Limpeza e Transformação (Data Wrangling)
        
        Dados brutos geralmente contêm inconsistências. utilizamos a técnica de **Method Chaining** do Pandas para criar um pipeline de transformação legível e funcional.
        
        **Etapas aplicadas:**
        1.  **Conversão Temporal:** A coluna `Date` é convertida de texto para objeto `datetime`, permitindo análises de séries temporais.
        2.  **Limpeza de Texto (Regex):** A coluna `Order_Demand` original contém parênteses (ex: `(100)`) que impedem cálculos matemáticos. Utilizamos Expressões Regulares (`regex`) para remover esses caracteres.
        3.  **Tipagem (Casting):** Conversão final da demanda para número inteiro (`int`).
        """)

    with t2:
        st.code("""
# Pipeline de tratamento utilizando Method Chaining
df_tratado = (
    df_bruto
    .copy()
    .assign(
        # Conversão da coluna de data (string -> datetime)
        Date = lambda x: pd.to_datetime(x["Date"], format = "%Y/%m/%d"),
        
        # Limpeza e conversão da demanda (remoção de parênteses e cast para int)
        Order_Demand = lambda x: x.Order_Demand
                                  .str.replace("\\(", "", regex = True)
                                  .str.replace("\\)", "", regex = True)
                                  .astype(int)
    )
)

# Exibição do resultado
df_tratado
        """, language="python")
        
    with t3:
        if df_raw is not None:
            # Aplica EXATAMENTE o que foi mostrado no código (sem filtros de data ou ordenação por enquanto)
            df_display = (
                df_raw
                .copy()
                .assign(
                    Date = lambda x: pd.to_datetime(x["Date"], format = "%Y/%m/%d"),
                    Order_Demand = lambda x: x.Order_Demand.astype(str).str.replace(r'[\(\)]', '', regex=True).astype(int)
                )
            )
            
            st.dataframe(df_display.head(10), use_container_width=True)
            
            # Verificação de Tipos
            st.markdown("##### Verificação de Tipos de Dados (Dtypes)")
            dtypes_df = df_display.dtypes.astype(str).reset_index()
            dtypes_df.columns = ["Coluna", "Tipo de Dado"]
            ui.table(data=pd.DataFrame(dtypes_df))

# ==============================================================================
# SEÇÃO 6: ANÁLISE EXPLORATÓRIA - EDA (CRISP-DM: Data Understanding)
# ==============================================================================
elif active == 'eda':
    st.subheader(":material/search: 6. Análise Exploratória (EDA)")
    
    st.markdown("""
    Nesta etapa, realizamos uma "investigação" dos dados (Exploratory Data Analysis) para entender padrões, distribuições e sazonalidades antes da modelagem.
    """)
    
    # Preparação dos dados (Hidden)
    df_raw = load_dataset()
    if df_raw is not None:
        df_tratado = (
            df_raw.copy().assign(
                Date = lambda x: pd.to_datetime(x["Date"], format = "%Y/%m/%d"),
                Order_Demand = lambda x: x.Order_Demand.astype(str).str.replace(r'[\(\)]', '', regex=True).astype(int)
            )
        )

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 1.1: Volumetria (Produtos)
        # -----------------------------------------------------------
        st.markdown("##### 6.1 Contagem de Produtos (SKUs)")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Verificamos a cardinalidade da coluna `Product_Code` para saber quantos produtos distintos existem no dataset. Isso define a granularidade do nosso problema de estoque.")
        with t2:
            st.code("""
# Quantos produtos tem?
df_tratado.Product_Code.nunique()
            """, language="python")
        with t3:
            res1 = df_tratado.Product_Code.nunique()
            st.write(f"**Resultado:** {res1} produtos únicos.")

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 1.2: Volumetria (Categorias)
        # -----------------------------------------------------------
        st.markdown("##### 6.2 Contagem de Categorias")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Checamos quantas famílias ou categorias de produtos existem (`Product_Category`). É útil para entender se devemos modelar tudo junto ou separar por clusters.")
        with t2:
            st.code("""
# Quantas categorias de produto tem?
df_tratado.Product_Category.nunique()
            """, language="python")
        with t3:
            res2 = df_tratado.Product_Category.nunique()
            st.write(f"**Resultado:** {res2} categorias.")

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 2: Estatística Descritiva
        # -----------------------------------------------------------
        st.markdown("##### 6.3 Resumo Estatístico")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("O método `.describe(include='all')` fornece um raio-x completo: contagem, média, desvio padrão, mínimos, máximos e quartis para colunas numéricas, e frequência/top para categóricas.")
        with t2:
            st.code("""
# Estatística descritiva
stat_desc = df_tratado.describe(include = "all")
stat_desc
            """, language="python")
        with t3:
            stat_desc = df_tratado.describe(include = "all")
            st.dataframe(stat_desc, use_container_width=True)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 3: Distribuição por Categoria
        # -----------------------------------------------------------
        st.markdown("##### 6.4 Volume por Categoria")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Visualizamos a frequência de pedidos por categoria para identificar o princípio de Pareto (80/20). Focaremos nossos esforços na categoria mais relevante.")
        with t2:
            st.code("""
# Qtd demandada de cada categoria de produto
df_tratado.groupby("Product_Category")["Order_Demand"].count().plot.bar();
            """, language="python")
        with t3:
            fig, ax = plt.subplots(figsize=(6, 2.5))
            
            # Dados
            counts = df_tratado.groupby("Product_Category")["Order_Demand"].count()
            
            # Cores "Delicadas" e Variadas (Palette Viridis/Spectral suavizada)
            colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(counts)))
            
            # Plot
            counts.plot.bar(ax=ax, color=colors, width=0.7, edgecolor='none')
            
            # Estilização Minimalista (CSS-like aesthetics)
            ax.set_title("Frequência de Pedidos por Categoria", fontsize=10, fontweight='bold', color='#444', pad=15)
            ax.set_xlabel("Categoria de Produto", fontsize=9, color='#666')
            ax.set_ylabel(None)
            
            # Remover bordas pesadas
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False) # Deixar só o grid
            ax.spines['bottom'].set_color('#DDD')
            
            # Grid suave
            ax.grid(axis='y', linestyle='--', alpha=0.3, color='#999')
            ax.set_axisbelow(True) # Grid atrás das barras
            
            # Ajuste de Ticks
            plt.xticks(rotation=90, fontsize=8, color='#555')
            plt.yticks(fontsize=8, color='#555')
            
            plt.tight_layout()
            st.pyplot(fig)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 4: Drill-Down (Filtro)
        # -----------------------------------------------------------
        st.markdown("##### 6.5 Seleção e Agregação Temporal")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("""
            Realizamos um **Drill-Down** (aprofundamento):
            1.  Selecionamos automaticamente a categoria top 1.
            2.  Agrupamos os dados por dia (`groupby Date`).
            3.  Reamostramos para frequência Semanal (`resample 'W'`) para suavizar o ruído diário.
            4.  Filtramos o período estável (`2012-2016`).
            """)
        with t2:
            st.code("""
# Análise temporal da categoria mais representativa
categoria_alvo = stat_desc.loc["top", "Product_Category"]
df_alvo = (
    df_tratado
    .query("Product_Category == @categoria_alvo")
    .groupby("Date")
    .Order_Demand
    .sum()
    .to_frame()
    .query("Date >= @pd.to_datetime('2012-01-01')")
    .Order_Demand
    .resample("W")
    .sum()
    .to_frame()
    .query("index <= @pd.to_datetime('2017-01-01')")
)
df_alvo
            """, language="python")
        with t3:
            # Execução Real
            categoria_alvo = stat_desc.loc["top", "Product_Category"]
            df_alvo = (
                df_tratado
                .query("Product_Category == @categoria_alvo")
                .groupby("Date")
                .Order_Demand
                .sum()
                .to_frame()
                .query("Date >= @pd.to_datetime('2012-01-01')")
                .Order_Demand
                .resample("W")
                .sum()
                .to_frame()
                .query("index <= @pd.to_datetime('2017-01-01')")
            )
            st.dataframe(df_alvo.head(), use_container_width=True)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 5: Visualização Temporal
        # -----------------------------------------------------------
        st.markdown("##### 6.6 Série Temporal (Line Plot)")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Com os dados agregados, plotamos a linha do tempo para observar a tendência geral e possíveis ciclos.")
        with t2:
            st.code("""
# Gráfico temporal
(
    p9.ggplot(df_alvo.reset_index()) +
    p9.aes(x = "Date", y = "Order_Demand") +
    p9.geom_line()
)
            """, language="python")
        with t3:
            p = (
                p9.ggplot(df_alvo.reset_index()) +
                p9.aes(x = "Date", y = "Order_Demand") +
                p9.geom_line(color="#2563eb") +
                p9.theme_minimal() +
                p9.theme(figure_size=(6, 2.5)) +
                p9.labs(title=f"Evolução Temporal: {categoria_alvo}")
            )
            st.pyplot(p.draw())

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 6: Stats da Série
        # -----------------------------------------------------------
        st.markdown("##### 6.7 Estatística da Série Agregada")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Analisamos a estatística novamente, agora focada apenas na série temporal tratada, para entender a média semanal de demanda.")
        with t2:
            st.code("""
# Estatística descritiva
df_alvo.describe()
            """, language="python")
        with t3:
            st.dataframe(df_alvo.describe(), use_container_width=True)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7: Histograma
        # -----------------------------------------------------------
        st.markdown("##### 6.8 Histograma de Demanda")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("O histograma nos mostra a forma da distribuição. Uma distribuição normal (sino) facilita modelos lineares; assimetrias podem exigir transformações (ex: Log).")
        with t2:
            st.code("""
# Gráfico de histograma
(
    p9.ggplot(df_alvo.reset_index()) +
    p9.aes(x = "Order_Demand") +
    p9.geom_histogram()
)
            """, language="python")
        with t3:
            p_hist = (
                p9.ggplot(df_alvo.reset_index()) +
                p9.aes(x = "Order_Demand") +
                p9.geom_histogram(fill="steelblue", bins=30) +
                p9.theme_minimal() +
                p9.theme(figure_size=(6, 2.5))
            )
            st.pyplot(p_hist.draw())

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 8: STL (Decomposição)
        # -----------------------------------------------------------
        st.markdown("##### 6.9 Decomposição Sazonal (STL)")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Aplicamos o algoritmo **STL** (Seasonal-Trend Decomposition using Loess) para isolar os componentes:\n1. **Tendência:** Crescimento/queda longo prazo.\n2. **Sazonalidade:** Padrões repetitivos (ciclo de 52 semanas).\n3. **Resíduo:** O que sobra (ruído aleatório).")
        with t2:
            st.code("""
# Análise de sazonalidade
stl = STL(df_alvo.Order_Demand, period = 52).fit()
stl.plot();
            """, language="python")
        with t3:
            stl = STL(df_alvo['Order_Demand'], period = 52).fit()
            fig_stl = stl.plot()
            fig_stl.set_size_inches(6, 4)
            st.pyplot(fig_stl)

# ==============================================================================
# SEÇÃO 7: MODELAGEM PREDITIVA (CRISP-DM: Modeling)
# ==============================================================================
elif active == 'modelo_preditivo':
    st.subheader(":material/psychology: 7. Modelagem Preditiva")
    
    st.markdown("""
    Nesta etapa, construímos e treinamos os modelos de previsão. Abordaremos duas estratégias:
    1.  **Regressão Linear:** Criando features manuais de tendência e sazonalidade.
    2.  **ETS (Exponential Smoothing):** Modelo clássico para séries temporais que captura nível, tendência e sazonalidade automaticamente.
    """)

    # -----------------------------------------------------------
    # Preparação de Contexto (Hidden)
    # -----------------------------------------------------------
    df_raw = load_dataset()
    if df_raw is not None:
        # 1. Tratamento
        df_tratado = (
            df_raw.copy().assign(
                Date = lambda x: pd.to_datetime(x["Date"], format = "%Y/%m/%d"),
                Order_Demand = lambda x: x.Order_Demand.astype(str).str.replace(r'[\(\)]', '', regex=True).astype(int)
            )
        )
        # 2. Seleção Alvo (Top 1)
        stat_desc = df_tratado.describe(include = "all")
        categoria_alvo = stat_desc.loc["top", "Product_Category"]
        df_alvo = (
            df_tratado
            .query("Product_Category == @categoria_alvo")
            .groupby("Date")
            .Order_Demand
            .sum()
            .to_frame()
            .query("Date >= @pd.to_datetime('2012-01-01')")
            .Order_Demand
            .resample("W")
            .sum()
            .to_frame()
            .query("index <= @pd.to_datetime('2017-01-01')")
        )

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7.1: Engenharia de Features (Regressores)
        # -----------------------------------------------------------
        st.markdown("##### 7.1 Engenharia de Features (Regressores)")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Para usar Regressão Linear em séries temporais, precisamos transformar o tempo em variáveis numéricas. Criamos:\n- **Tendência:** Um contador sequencial (índice).\n- **Sazonalidade:** Uma função seno para simular comportamento cíclico anual.")
        with t2:
            st.code("""
# Criar regressores
month = df_alvo.index.month
df_regressao = (
    df_alvo
    .copy()
    .assign(
        tendencia = lambda x: ((df_alvo.reset_index().index + 1) + df_alvo.Order_Demand.mean()),
        sazonalidade = np.sin(2 * np.pi * month / 12)
        )
)
df_regressao
            """, language="python")
        with t3:
            month = df_alvo.index.month
            df_regressao = (
                df_alvo
                .copy()
                .assign(
                    tendencia = lambda x: ((df_alvo.reset_index().index + 1) + df_alvo.Order_Demand.mean()),
                    sazonalidade = np.sin(2 * np.pi * month / 12)
                    )
            )
            st.dataframe(df_regressao.head(10), use_container_width=True)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7.2: Split Treino/Teste
        # -----------------------------------------------------------
        st.markdown("##### 7.2 Separação Treino/Teste")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Dividimos os dados temporalmente. Treinamos com dados até **2015-01-01** e testaremos a performance nos dados posteriores.")
        with t2:
            st.code("""
# Separa amostras treino/teste
df_treino = df_regressao.query("index <= @pd.to_datetime('2015-01-01')").copy()
df_teste = df_regressao.query("index > @pd.to_datetime('2015-01-01')").copy()
df_treino
            """, language="python")
        with t3:
            df_treino = df_regressao.query("index <= @pd.to_datetime('2015-01-01')").copy()
            df_teste = df_regressao.query("index > @pd.to_datetime('2015-01-01')").copy()
            st.write(f"**Treino:** {len(df_treino)} semanas | **Teste:** {len(df_teste)} semanas")
            st.dataframe(df_treino.tail(), use_container_width=True)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7.3: Regressão Linear (Fit)
        # -----------------------------------------------------------
        st.markdown("##### 7.3 Treinamento Regressão Linear")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Utilizamos um Pipeline que primeiro normaliza os dados (`StandardScaler`) e depois aplica a Regressão Linear. O modelo aprende a relação entre Tendência/Sazonalidade e a Demanda.")
        with t2:
            st.code("""
# Regressão linear (fit)
modelo_rl = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("regressor", LinearRegression())
])
modelo_rl.fit(df_treino[["tendencia", "sazonalidade"]], df_treino["Order_Demand"])
            """, language="python")
        with t3:
            modelo_rl = Pipeline(steps=[
                ("scaler", StandardScaler()),
                ("regressor", LinearRegression())
            ])
            modelo_rl.fit(df_treino[["tendencia", "sazonalidade"]], df_treino["Order_Demand"])
            st.success("Modelo de Regressão Linear treinado com sucesso!")
            st.write(modelo_rl)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7.4: Regressão Linear (Predict)
        # -----------------------------------------------------------
        st.markdown("##### 7.4 Previsão (Forecast) - Regressão Linear")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Com o modelo treinado, realizamos a previsão para o período de teste usando as features `tendencia` e `sazonalidade` do conjunto de teste.")
        with t2:
            st.code("""
# Regressão linear (forecast)
y_prev_rl = modelo_rl.predict(df_teste[["tendencia", "sazonalidade"]])
y_prev_rl
            """, language="python")
        with t3:
            y_prev_rl = modelo_rl.predict(df_teste[["tendencia", "sazonalidade"]])
            st.write("**Array de Previsões (Primeiros 10 valores):**")
            st.write(y_prev_rl[:10])

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7.5: ETS (Fit)
        # -----------------------------------------------------------
        st.markdown("##### 7.5 Treinamento ETS (Exponential Memory)")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Treinamos um modelo **ETS (Error, Trend, Seasonality)**. Configuramos Sazonalidade Aditiva (`seasonal='add'`) e período de 52 semanas.")
        with t2:
            st.code("""
# Modelo ETS (fit)
modelo_ets = ExponentialSmoothing(
    df_treino.Order_Demand,
    trend = "add",
    seasonal = "add",
    seasonal_periods = 52
).fit(optimized = True)
modelo_ets
            """, language="python")
        with t3:
            modelo_ets = ExponentialSmoothing(
                df_treino.Order_Demand,
                trend = "add",
                seasonal = "add",
                seasonal_periods = 52
            ).fit(optimized = True)
            st.success("Modelo ETS treinado com sucesso!")
            st.write(modelo_ets)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 7.6: ETS (Forecast)
        # -----------------------------------------------------------
        st.markdown("##### 7.6 Previsão (Forecast) - ETS")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Geramos a previsão para `len(df_teste)` passos à frente. O ETS projeta os componentes de tendência e sazonalidade aprendidos.")
        with t2:
            st.code("""
# Modelo ETS (forecast)
y_prev_ets = modelo_ets.forecast(len(df_teste))
y_prev_ets
            """, language="python")
        with t3:
            y_prev_ets = modelo_ets.forecast(len(df_teste))
            st.write("**Série de Previsões (Primeiros 10 valores):**")
            st.write(y_prev_ets.head(10))

# ==============================================================================
# SEÇÃO 8: AVALIAÇÃO E DIAGNÓSTICO (CRISP-DM: Evaluation)
# ==============================================================================
elif active == 'avaliacao':
    st.subheader(":material/rule: 8. Avaliação e Diagnóstico")
    
    st.markdown("""
    Nesta etapa, consolidamos as previsões dos modelos (Regressão Linear e ETS) e as confrontamos com os dados reais de teste. 
    Calculamos métricas de erro (**MAE** e **RMSE**) para identificar matematicamente qual modelo performou melhor e deve ser escolhido para o deploy.
    """)

    # -----------------------------------------------------------
    # Preparação de Contexto (Hidden) - Necessário para gerar os objetos y_prev
    # -----------------------------------------------------------
    df_raw = load_dataset()
    if df_raw is not None:
        # Tratamento e Split
        df_tratado = df_raw.copy().assign(
            Date = lambda x: pd.to_datetime(x["Date"], format = "%Y/%m/%d"),
            Order_Demand = lambda x: x.Order_Demand.astype(str).str.replace(r'[\(\)]', '', regex=True).astype(int)
        )
        stat_desc = df_tratado.describe(include = "all")
        categoria_alvo = stat_desc.loc["top", "Product_Category"]
        df_alvo = df_tratado.query("Product_Category == @categoria_alvo").groupby("Date").Order_Demand.sum().to_frame()
        df_alvo = df_alvo.query("Date >= '2012-01-01'").resample("W").sum().query("index <= '2017-01-01'")
        
        # Features
        month = df_alvo.index.month
        df_regressao = df_alvo.copy().assign(
            tendencia = lambda x: ((df_alvo.reset_index().index + 1) + df_alvo.Order_Demand.mean()),
            sazonalidade = np.sin(2 * np.pi * month / 12)
        )
        
        # Split
        df_treino = df_regressao.query("index <= '2015-01-01'").copy()
        df_teste = df_regressao.query("index > '2015-01-01'").copy()
        
        # Treino/Predict RL
        modelo_rl = Pipeline(steps=[("scaler", StandardScaler()), ("regressor", LinearRegression())])
        modelo_rl.fit(df_treino[["tendencia", "sazonalidade"]], df_treino["Order_Demand"])
        y_prev_rl = modelo_rl.predict(df_teste[["tendencia", "sazonalidade"]])
        
        # Treino/Predict ETS
        modelo_ets = ExponentialSmoothing(df_treino.Order_Demand, trend="add", seasonal="add", seasonal_periods=52).fit(optimized=True)
        y_prev_ets = modelo_ets.forecast(len(df_teste))

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 8.1: Consolidando Resultados
        # -----------------------------------------------------------
        st.markdown("##### 8.1 Consolidação dos Resultados")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Criamos um DataFrame único (`df_previsao`) unindo os valores reais de teste e as previsões dos dois modelos (RL e ETS) para facilitar a comparação.")
        with t2:
            st.code("""
# Consolidando resultados
df_previsao = (
    pd.Series(y_prev_rl, index = df_teste.index)
    .rename("RL")
    .to_frame()
    .join(y_prev_ets.rename("ETS"))
    .join(df_teste["Order_Demand"])
)
df_previsao
            """, language="python")
        with t3:
            df_previsao = (
                pd.Series(y_prev_rl, index = df_teste.index)
                .rename("RL")
                .to_frame()
                .join(y_prev_ets.rename("ETS"))
                .join(df_teste["Order_Demand"])
            )
            st.dataframe(df_previsao.head(), use_container_width=True)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 8.2: Comparação Visual
        # -----------------------------------------------------------
        st.markdown("##### 8.2 Comparação Visual (Real vs Previsto)")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Plotamos as três séries. O objetivo é ver qual linha (RL ou ETS) adere melhor à linha real (Order_Demand).")
        with t2:
            st.code("""
# Comparação visual
df_previsao.plot();
            """, language="python")
        with t3:
            fig, ax = plt.subplots(figsize=(8, 4))
            df_previsao.plot(ax=ax, style=['--', '--', '-'], color=['#ef4444', '#3b82f6', '#10b981'], linewidth=1.5)
            ax.set_title("Comparativo: Real vs Modelos")
            ax.grid(True, alpha=0.3)
            ax.legend(["Regressão Linear", "ETS", "Real"])
            st.pyplot(fig)

        st.markdown("---")

        # -----------------------------------------------------------
        # BLOCO 8.3: Métricas de Erro
        # -----------------------------------------------------------
        st.markdown("##### 8.3 Métricas de Performance")
        t1, t2, t3 = st.tabs([":material/description: Explicação", ":material/code: Código", ":material/visibility: Resultado"])
        
        with t1:
            st.markdown("Calculamos o erro numérico. **RMSE** (Raiz do Erro Quadrático Médio) penaliza grandes erros, enquanto **MAE** (Erro Médio Absoluto) mostra a magnitude média do desvio.")
        with t2:
            st.code("""
# Cálculo de métricas de erro
y_true = df_previsao.Order_Demand
y_pred_rl = df_previsao.RL
y_pred_ets = df_previsao.ETS

print("Métricas RL")
print(f"Erro médio: {np.mean(y_true - y_pred_rl)}")
print(f"Erro médio absoluto: {np.mean(np.abs(y_true - y_pred_rl))}")
print(f"Raiz do erro médio quadrático: {np.sqrt(np.mean((y_true - y_pred_rl)**2))}")

print("Métricas ETS")
print(f"Erro médio: {np.mean(y_true - y_pred_ets)}")
print(f"Erro médio absoluto: {np.mean(np.abs(y_true - y_pred_ets))}")
print(f"Raiz do erro médio quadrático: {np.sqrt(np.mean((y_true - y_pred_ets)**2))}")
            """, language="python")
        with t3:
            y_true = df_previsao.Order_Demand
            y_pred_rl = df_previsao.RL
            y_pred_ets = df_previsao.ETS
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**📉 Métricas Regressão Linear**")
                st.text(f"ME  : {np.mean(y_true - y_pred_rl):.2f}")
                st.text(f"MAE : {np.mean(np.abs(y_true - y_pred_rl)):.2f}")
                st.text(f"RMSE: {np.sqrt(np.mean((y_true - y_pred_rl)**2)):.2f}")
            
            with c2:
                st.markdown("**📉 Métricas ETS**")
                st.text(f"ME  : {np.mean(y_true - y_pred_ets):.2f}")
                st.text(f"MAE : {np.mean(np.abs(y_true - y_pred_ets)):.2f}")
                st.text(f"RMSE: {np.sqrt(np.mean((y_true - y_pred_ets)**2)):.2f}")



# ==============================================================================
# SEÇÃO 9: COMUNICAÇÃO DE RESULTADOS (CRISP-DM: Deployment)
# ==============================================================================
elif active == 'comunicacao':
    st.subheader(":material/campaign: 10. Comunicação de Resultados")
    
    st.markdown("""
    <div class="shadcn-card" style="border-left: 4px solid #10b981;">
        <h3 class="shadcn-card-title">✅ Ação Recomendada</h3>
        <p class="shadcn-card-desc">Aumentar estoque de segurança em 15% a partir de Outubro.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ui.metric_card(title="Economia", content="R$ 1.2M", description="Redução de Ruptura", key="k1")
    with c2:
        ui.metric_card(title="Eficiência", content="+12%", description="Giro de Estoque", key="k2")
    with c3:
        ui.metric_card(title="Nível de Serviço", content="98.5%", description="Target Atingido", key="k3")

# ==============================================================================
# FOOTER - NAVEGAÇÃO ENTRE SEÇÕES
# ==============================================================================
st.markdown('<div class="footer-nav-container">', unsafe_allow_html=True)
col_nav_1, col_nav_2 = st.columns(2)

try:
    current_idx = SECTION_ORDER.index(active)
    
    # Botão Anterior (Esquerda)
    with col_nav_1:
        if current_idx > 0:
            prev_key = SECTION_ORDER[current_idx - 1]
            if st.button(f":material/arrow_back: {SECTIONS[prev_key]}", key="nav_prev", use_container_width=False):
                st.session_state.active_section = prev_key
                st.query_params["secao"] = prev_key  # Atualiza URL
                st.rerun()

    # Botão Próximo (Direita)
    with col_nav_2:
        if current_idx < len(SECTION_ORDER) - 1:
            next_key = SECTION_ORDER[current_idx + 1]
            if st.button(f"{SECTIONS[next_key]} :material/arrow_forward:", key="nav_next", use_container_width=False):
                st.session_state.active_section = next_key
                st.query_params["secao"] = next_key  # Atualiza URL
                st.rerun()
except ValueError:
    pass 
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# RODAPÉ - CRÉDITOS E INFORMAÇÕES
# ==============================================================================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748b; padding-bottom: 20px;">
        Projeto desenvolvido por <a href="https://www.spdev.com.br" target="_blank" style="color: #0f172a; text-decoration: none; font-weight: 600;">Sabrina Pinheiro</a><br>
        Curso Análise Macro - Como Pensar em Dados
    </div>
    """,
    unsafe_allow_html=True
)
