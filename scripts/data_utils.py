"""
Data Utilities Module
=====================

Módulo responsável por funções de carregamento e processamento de dados.
Separado do main_app.py para melhor organização e reutilização.

Funções:
    - load_dataset(): Carrega o dataset bruto do CSV
    - clean_data(): Aplica pipeline de limpeza e transformação
"""

import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_dataset():
    """
    Carrega o dataset Historical Product Demand do arquivo CSV.
    
    Returns:
        pd.DataFrame: Dataset bruto com colunas originais
        None: Se o arquivo não for encontrado
    
    Raises:
        st.error: Exibe mensagem de erro no Streamlit se arquivo não existir
    """
    DATA_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'Historical Product Demand.csv')
    )
    
    if not os.path.exists(DATA_PATH):
        st.error(f"Arquivo não encontrado: {DATA_PATH}")
        return None
    
    return pd.read_csv(DATA_PATH)


@st.cache_data
def clean_data(df):
    """
    Aplica pipeline de limpeza e transformação nos dados brutos.
    
    Transformações aplicadas:
        1. Conversão de Date (string → datetime)
        2. Limpeza de Order_Demand (remoção de parênteses via regex)
        3. Conversão de Order_Demand (string → int)
        4. Remoção de valores nulos em Date
        5. Filtro temporal (2012-2017)
        6. Ordenação por data
    
    Args:
        df (pd.DataFrame): DataFrame bruto do load_dataset()
    
    Returns:
        pd.DataFrame: DataFrame limpo e transformado
    
    Example:
        >>> df_raw = load_dataset()
        >>> df_clean = clean_data(df_raw)
        >>> df_clean.dtypes
        Date            datetime64[ns]
        Order_Demand             int64
        ...
    """
    return (
        df.copy()
        .assign(
            Date = lambda x: pd.to_datetime(x['Date'], format="%Y/%m/%d"),
            Order_Demand = lambda x: (
                x['Order_Demand'].astype(str).str.replace(r'[\(\)]', '', regex=True).astype(int)
            )
        )
        .dropna(subset=['Date'])
        .query("Date >= '2012-01-01' and Date <= '2017-01-01'")
        .sort_values('Date')
    )
