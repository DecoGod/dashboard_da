import sys
sys.path.append(sys.path[0][:-6])
import io
import pandas as pd
import psycopg2 as pg
import datetime

database = "SGM"
user = "terralab"
host = "34.23.51.180"
password = "terralab0705"

conn = pg.connect(database=database,
                  user=user,
                  host=host,
                  password=password)

def auxGetGeo(date_init, date_final, lower_request, cur):
    query = """ SELECT "Request".city,"Request".state, "Request".full_address, "Response".latitude, "Response".longitude, "Response".geoapi_id,CAST("Search".date AS DATE)
                FROM "Search", "Request", "Response"
                WHERE "Search".request_id ="Request".request_id AND "Request".request_id =  "Response".request_id AND
                      "Search".geoapi_id = "Response".geoapi_id AND
                      "Request".request_id  IN (SELECT "Search".request_id
                                                FROM "Search"
                                                WHERE (CAST("Search".date AS DATE) >= '{}' AND
                                                CAST("Search".date AS DATE) <= '{}') AND "Search".request_id <= {}
                      )
    """.format(date_init, date_final, lower_request)

    output = io.StringIO()
    cur.copy_expert(
        "COPY ({}) TO STDOUT WITH CSV HEADER".format(query), output)
    output.seek(0)
    df = pd.read_csv(output)
    df = df.drop_duplicates()
    df['city'] = [x.lower() for x in df['city']]
    return df
    
def getGeolocatedData2(date_init, date_final, lower_request):
    """
        Função que retorna os dados que foram geolocalizados no intervalo de tempo indicado e 
        que não são superiores ao 'lower_request'

        Args: 
            date_init (str) : Data minima permitida
            date_final (str) : Data máxima permitida
            lower_request (str) : Maior request aceito
        Returns:
            Pandas.DataFrame : DataFrame contendo os dados encontrados
    """
    cur = conn.cursor()
    df = pd.DataFrame()
    min_date = datetime.date.fromisoformat(date_init)
    max_date = datetime.date.fromisoformat(date_final)
    month = datetime.timedelta(days=30)
    max_range = min_date + month
    while max_range < max_date:
        auxdf = auxGetGeo(min_date, max_range, lower_request, cur)
        df = pd.concat([df, auxdf])
        min_date += month
        max_range += month
    if max_range == max_date:
        auxdf = auxGetGeo(min_date, max_range, lower_request, cur)
        df = pd.concat([df, auxdf])
    elif max_range > max_date:
        max_range = max_range - month
        tempo = max_date - max_range
        max_range += tempo
        auxdf = auxGetGeo(min_date, max_range, lower_request, cur)
        df = pd.concat([df, auxdf])
    return df

def getLowerRequest():
    """
        Função que realiza uma query no banco de dados para pegar o maior request_id da API
        que possui menor numero de requisições diarias

        Args:

        Returns:
            int : Valor do maior reques
    """
    cur = conn.cursor()
    query = """ SELECT MAX("request_id")
                FROM "Search"
                WHERE "Search".geoapi_id = (
                  SELECT "geoapi_id"
                  FROM "Geoapi"
                  WHERE "maxRequestPerDay" =(SELECT MIN("maxRequestPerDay") FROM "Geoapi") 
                  )
                  """

    cur.execute(query)
    dados = cur.fetchall()[0][0]
    return dados


def getGeolocatedData(date_init, date_final, lower_request):
    """
        Função que retorna os dados que foram geolocalizados no intervalo de tempo indicado e 
        que não são superiores ao 'lower_request'

        Args: 
            date_init (str) : Data minima permitida
            date_final (str) : Data máxima permitida
            lower_request (str) : Maior request aceito
        Returns:
            Pandas.DataFrame : DataFrame contendo os dados encontrados
    """
    cur = conn.cursor()
    query = """ SELECT "Request".city,"Request".state, "Request".full_address, "Response".latitude, "Response".longitude, "Response".geoapi_id,CAST("Search".date AS DATE)
                FROM "Search", "Request", "Response"
                WHERE "Search".request_id ="Request".request_id AND "Request".request_id =  "Response".request_id AND
                      "Search".geoapi_id = "Response".geoapi_id AND
                      "Request".request_id  IN (SELECT "Search".request_id
                                                FROM "Search"
                                                WHERE (CAST("Search".date AS DATE) >= '{}' AND
                                                CAST("Search".date AS DATE) <= '{}') AND "Search".request_id <= {}
                      )
    """.format(date_init, date_final, lower_request)

    output = io.StringIO()
    cur.copy_expert(
        "COPY ({}) TO STDOUT WITH CSV HEADER".format(query), output)
    output.seek(0)
    df = pd.read_csv(output)
    df = df.drop_duplicates()
    df['city'] = [x.lower() for x in df['city']]
    print('Pegou dados')
    return df


def getMinDate():
    """
        Função que realiza uma query SQL na base de dados e informa qual a menor data disponível 
        para acessar os dados

        Args:

        Returns:
            str: Menor data disponível no formato YYYY-MM-DD
    """
    cur = conn.cursor()
    query = """ SELECT MIN(CAST("Search".date AS DATE))
                FROM "Search"
    """
    output = io.StringIO()
    cur.copy_expert(
        "COPY ({}) TO STDOUT WITH CSV HEADER".format(query), output)
    output.seek(0)
    df = pd.read_csv(output)
    date_min = df.iloc[0, 0]
    return date_min


def getMaxDate():
    """
        Função que realiza uma query SQL na base de dados e informa qual a maior data disponível 
        para acessar os dados

        Args:

        Returns:
            str: Maior data disponível no formato YYYY-MM-DD
    """
    cur = conn.cursor()
    output = io.StringIO()
    query = """ SELECT MAX(CAST("Search".date AS DATE))
                FROM "Search"
    """
    cur.copy_expert(
        "COPY ({}) TO STDOUT WITH CSV HEADER".format(query), output)
    output.seek(0)
    df = pd.read_csv(output)
    date_min = df.iloc[0, 0]
    return date_min
