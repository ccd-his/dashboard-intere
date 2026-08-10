import geopandas as gpd
import pandas as pd

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
def get_simplified_geometry(dataframe: pd.DataFrame, background: bool = False):
    """
    Simplifica a geometria dos mapas
    Sem simplificar, os mapas do estado de SP consomem 40MB+ para exibir, isso consome banda,
    processamento no servidor e processamento no dispositivo, o mapa fica pesado desnecessariamente.

    Valores maiores indicam mapas mais simplificados

    background indica que o dataframe está sendo usado para segundo plano, não precisa ser tão fiel
    quanto o mapa em foco
    """
    if background:
        return dataframe.simplify(0.005).__geo_interface__
    else:
        return dataframe.simplify(0.0002).__geo_interface__

    # Sem simplificar
    # if background:
    #     return dataframe.__geo_interface__
    # else:
    #     return dataframe.__geo_interface__


@memory.cache
def load_clusters():
    return pd.read_csv(
        "https://raw.githubusercontent.com/ccd-his/dashboard-intere/refs/heads/main/data/clusters.csv"
    )


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
def load_df_irct_filtrado(df: pd.DataFrame):
    """Dataframe com união dos dados de indicadores IRCT com georef"""
    # TODO: Descrever melhor este dataframe/função
    # Costumava pegar o dataframe indicadores, mas agrupamento repete usando clusters.csv

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
