import geopandas as gpd
import pandas as pd
import urllib.request
import os

from caching import memory


@memory.cache
def load_gdf() -> pd.DataFrame:
    """Dataframe de dados de geolocalização"""

    # Carregar dados
    gdf = gpd.read_file("./data/SP_Municipios_2025/SP_Municipios_2025.shp")
    gdf = gdf.to_crs(4674)
    gdf["CD_MUN"] = gdf["CD_MUN"].astype(str)
    gdf = gdf.sort_values("NM_MUN").reset_index(drop=True)

    gdf["id"] = gdf.index.astype(str)
    return gdf


@memory.cache
def get_simplified_geometry_background(light=False):
    """Geometria simplificada para o mapa de fundo (todos os municípios em cinza)"""
    gdf = load_gdf()
    tolerance = 0.008 if light else 0.005
    return gdf.simplify(tolerance).__geo_interface__


@memory.cache
def get_simplified_geometry_foreground(light=False):
    """Geometria simplificada para o mapa em foco (municípios com índices)"""
    gdf_filtrado = load_df_irct_filtrado()
    if light:
        tolerance = 0.008
    elif os.getenv("LIGHT", "false") == "true":
        tolerance = 0.002
    else:
        tolerance = 0.0002
    return gdf_filtrado.simplify(tolerance).__geo_interface__


@memory.cache
def get_simplified_geometry_clusters(light=False):
    """Geometria simplificada para o mapa de clusters"""
    gdf_filtrado = load_df_clusters_filtrado()
    if light:
        tolerance = 0.008
    elif os.getenv("LIGHT", "false") == "true":
        tolerance = 0.002
    else:
        tolerance = 0.0002
    return gdf_filtrado.simplify(tolerance).__geo_interface__


@memory.cache
def load_clusters():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/clusters.csv"
    )


@memory.cache
def load_caracteristicas_clusters():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/caracteristicas_clusters.csv"
    )


@memory.cache
def load_df_indicadores() -> pd.DataFrame:
    """Dataframe de indicadores criados pela equipe"""

    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/indicadores.csv"
    )


@memory.cache
def load_df_cidades():
    """Dataframe com a lista de cidades presentes no gdf"""

    df = load_df_indicadores()
    return df["Município"].unique()


@memory.cache
def load_df_irct_filtrado():
    """Dataframe com união dos dados de indicadores IRCT com georef"""
    df = load_df_indicadores()
    df_irct = df[
        [
            "Código IBGE",
            "Município",
            "Mitigação",
            "Adaptação",
            "Déficit Habitacional",
            "Vulnerabilidade Social",
            "Índice de Resiliência Climática e Territorial",
        ]
    ]
    df_irct["Código IBGE"] = df_irct["Código IBGE"].astype("str")
    gdf = load_gdf()
    return gdf.merge(df_irct, left_on="CD_MUN", right_on="Código IBGE")


@memory.cache
def load_df_clusters_filtrado():
    """Dataframe com união dos dados de clusters com georef"""
    df = load_clusters()
    df_irct = df[
        [
            "Código IBGE",
            "Município",
            "Mitigação",
            "Adaptação",
            "Déficit Habitacional",
            "Vulnerabilidade Social",
            "Índice de Resiliência Climática e Territorial",
        ]
    ]
    df_irct["Código IBGE"] = df_irct["Código IBGE"].astype("str")
    gdf = load_gdf()
    return gdf.merge(df_irct, left_on="CD_MUN", right_on="Código IBGE")


@memory.cache
def load_df_unidades():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/fontes_unidades.csv"
    )


@memory.cache
def load_df_recomendacoes():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/recomendacoes.csv"
    )

@memory.cache
def load_df_textos_home():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/textos_home.csv"
    )


@memory.cache
def load_df_textos_agrupamentos():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/textos_agrupamentos.csv"
    )
@memory.cache
def load_sobre():
    url = "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/sobre.md"
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

@memory.cache
def load_equipe():
    url = "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/equipe.md"
    with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')

@memory.cache
def load_df_arquitetos():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/arquitetos.csv"
    )