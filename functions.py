import psycopg2
import io
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta, date
from typing import Dict
from data_access import *

def get_successful_geocode(data_init: str, data_final: str) -> pd.DataFrame:
    """
    Retorna um DataFrame contendo informações sobre o número de requisições bem-sucedidas realizadas no intervalo de tempo 
    especificado.

    Args:
        data_init (str): Data inicial no formato 'yyyy-mm-dd'.
        data_final (str): Data final no formato 'yyyy-mm-dd'.

    Returns:
        pd.DataFrame: DataFrame contendo as colunas 'geoapi_id', 'date', 'count', onde cada linha representa uma contagem do número de geocodificações bem-sucedidas para cada API geocodificadora em uma determinada data.
    """
    cur = conn.cursor()
    query = """ SELECT geoapi_id, CAST("Search".date AS DATE), COUNT(*) as count
            FROM "Search"
            JOIN "Request" ON "Search".request_id = "Request".request_id 
            WHERE "Search".generated_response = 't'
              AND "Search".date >= '{}'::date AND "Search".date <= '{}'::date
            GROUP BY 1, 2
        """.format(data_init, data_final)
    
    output = io.StringIO()
    cur.copy_expert(
        "COPY ({}) TO STDOUT WITH CSV HEADER".format(query), output)
    output.seek(0)
    df = pd.read_csv(output)
    return df

def get_fails_geocode(data_init: str, data_final: str) -> pd.DataFrame:
    """
        Retorna um DataFrame contendo informações sobre o número de requisições que falharam (não tiveram resposta válida)
        realizadas no intervalo de tempo especificado.

        Args:
            data_init (str): Data inicial no formato 'yyyy-mm-dd'.
            data_final (str): Data final no formato 'yyyy-mm-dd'.

        Returns:
            pd.DataFrame: DataFrame contendo as colunas 'geoapi_id', 'date', 'count', onde cada linha representa uma contagem do número
            de geocodificações falhas para cada API geocodificadora em uma determinada data.
    """
    cur = conn.cursor()
    query = """ SELECT geoapi_id, CAST("Search".date AS DATE), COUNT(*) as count
            FROM "Search"
            JOIN "Request" ON "Search".request_id = "Request".request_id 
            WHERE "Search".generated_response = 'f'
              AND "Search".date >= '{}'::date AND "Search".date <= '{}'::date
            GROUP BY 1, 2
        """.format(data_init, data_final)
    output = io.StringIO()
    cur.copy_expert(
        "COPY ({}) TO STDOUT WITH CSV HEADER".format(query), output)
    output.seek(0)
    df = pd.read_csv(output)
    return df

def graph_hit_fails(success: pd.DataFrame, fails: pd.DataFrame) -> go.Figure:
    """
        Retorna um gráfico interativo do tipo histograma mostrando o número de geocodificações bem-sucedidas e malsucedidas
        (que falharam) para cada API geocodificadora.

        Args:
            success (pd.DataFrame): DataFrame contendo as colunas 'geoapi_id', 'date', 'count', representando as
            geocodificações bem-sucedidas.
            fails (pd.DataFrame): DataFrame contendo as colunas 'geoapi_id', 'date', 'count', representando as
            geocodificações que falharam.

        Returns:
            go.Figure: Gráfico interativo do tipo histograma contendo duas barras empilhadas para cada API geocodificadora,
            representando o número de geocodificações bem-sucedidas e malsucedidas (falhas).
    """
    fails = fails.groupby('geoapi_id').agg('sum', numeric_only=True).reset_index()
    success = success.groupby('geoapi_id').agg('sum', numeric_only=True).reset_index()
    success = success.merge(fails["count"].to_frame(),left_index=True,right_index=True)
    success = success.rename(columns={'geoapi_id': 'API',
                                    'count_x': 'Geocodificações',
                                    'count_y': 'Falhas'})

    success['Acertos'] = success['Geocodificações'] - \
        success['Falhas']

    fails_and_hits = pd.concat([
        pd.DataFrame().assign(API=success['API'],
                                PASS="Acerto",
                                Geo=success['Acertos']),
        pd.DataFrame().assign(API=success['API'],
                                PASS="Falha",
                                Geo=success['Falhas'])
    ]).sort_values(by='API')

    fig = px.histogram(fails_and_hits,
                        x="API",
                        y="Geo",
                        color='PASS',
                        barmode='group',
                        height=600,
                        width=1450,
                        text_auto=True,
                        labels={"PASS":"Geocodificações"}
                        ).update_yaxes(title='Geocodificações',
                                        tickformat=".2s")
    fig.update_layout(font=dict(size=12),
                      template="plotly_dark",
                      height=300,
                      width=800,
                     )
    return fig