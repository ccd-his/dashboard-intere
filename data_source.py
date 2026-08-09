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
    # gdf.simplify(tolerance=0.005)

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
def load_df_indicadores():
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
def load_df_irct():
    """Dataframe com índice de Resiliência Climática Territorial"""

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
    return df_irct


@memory.cache
def load_df_irct_filtrado():
    """Dataframe com união dos dados de indicadores IRCT com georef"""
    gdf = load_gdf()
    df_irct = load_df_irct()
    return gdf.merge(df_irct, left_on="CD_MUN", right_on="Código IBGE")
