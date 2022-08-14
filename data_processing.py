import logging
import pandas as pd
from helper import get_current_date


def data_processing():
    """Function to process the data into 3 tables using pandas"""

    logger = logging.getLogger(__name__)
    logger.info(f"Starting to process the data...")

    # Get the current date in 2 string formats
    year_month_str, date_str = get_current_date()

    # Load the 3 csv
    df_museos = pd.read_csv(f"./museos/{year_month_str}/museos-{date_str}.csv", dtype={"cod_area": str})
    df_bibliotecas = pd.read_csv(
        f"./bibliotecas/{year_month_str}/bibliotecas-{date_str}.csv",
        na_values=["s/d"],
        dtype={"Cod_tel": str, "Teléfono": str},
    )
    df_salas_cine = pd.read_csv(
        f"./salas_cine/{year_month_str}/salas_cine-{date_str}.csv",
        na_values=["s/d"],
        dtype={"cod_area": str, "Teléfono": str},
    )

    """Process to make table 1"""
    logger.info(f"Creating table 1...")

    # Get a new df with the required columns
    df_museos_1 = df_museos.drop(
        columns=[
            "Observaciones",
            "subcategoria",
            "piso",
            "Latitud",
            "Longitud",
            "TipoLatitudLongitud",
            "Info_adicional",
            "fuente",
            "jurisdiccion",
            "año_inauguracion",
            "actualizacion",
        ]
    )

    df_bibliotecas_1 = df_bibliotecas.drop(
        columns=[
            "Observacion",
            "Subcategoria",
            "Departamento",
            "Piso",
            "Información adicional",
            "Latitud",
            "Longitud",
            "TipoLatitudLongitud",
            "Fuente",
            "Tipo_gestion",
            "año_inicio",
            "Año_actualizacion",
        ]
    )

    df_salas_cine_1 = df_salas_cine.drop(
        columns=[
            "Observaciones",
            "Departamento",
            "Piso",
            "Información adicional",
            "Latitud",
            "Longitud",
            "TipoLatitudLongitud",
            "Fuente",
            "tipo_gestion",
            "Pantallas",
            "Butacas",
            "espacio_INCAA",
            "año_actualizacion",
        ]
    )

    # Join cod_area with telefono and then drop cod_area
    df_museos_1["cod_area"].fillna(" ", inplace=True)
    df_museos_1["telefono"] = df_museos_1["cod_area"] + " " + df_museos_1["telefono"]
    df_museos_1.drop(columns=["cod_area"], inplace=True)

    df_bibliotecas_1["Cod_tel"].fillna(" ", inplace=True)
    df_bibliotecas_1["Teléfono"] = df_bibliotecas_1["Cod_tel"] + " " + df_bibliotecas_1["Teléfono"]
    df_bibliotecas_1.drop(columns=["Cod_tel"], inplace=True)

    df_salas_cine_1["cod_area"].fillna(" ", inplace=True)
    df_salas_cine_1["Teléfono"] = df_salas_cine_1["cod_area"] + " " + df_salas_cine_1["Teléfono"]
    df_salas_cine_1.drop(columns=["cod_area"], inplace=True)

    # Rename columns to normalize the information
    col_names = [
        "cod_localidad",
        "id_provincia",
        "id_departamento",
        "categoria",
        "provincia",
        "localidad",
        "nombre",
        "domicilio",
        "código postal",
        "número de teléfono",
        "mail",
        "web",
    ]

    df_museos_1.columns = df_bibliotecas_1.columns = df_salas_cine_1.columns = col_names

    table_1 = pd.concat([df_museos_1, df_bibliotecas_1, df_salas_cine_1])

    """Process to make table 2"""
    logger.info(f"Creating table 2...")

    # Create first part of table 2
    table_2_1 = table_1.groupby(["categoria"]).categoria.count().to_frame().T
    table_2_1.reset_index(inplace=True)
    table_2_1.drop(columns=["index"], inplace=True)

    # Create second part of table 2
    s_1 = df_museos.groupby(["fuente"]).fuente.count().to_frame()
    s_2 = df_bibliotecas.groupby(["Fuente"]).Fuente.count().to_frame()
    s_3 = df_salas_cine.groupby(["Fuente"]).Fuente.count().to_frame()
    s_2.columns = s_3.columns = ["fuente"]
    table_2_2 = pd.concat([s_1, s_2, s_3]).T
    table_2_2.reset_index(inplace=True)
    table_2_2.drop(columns=["index"], inplace=True)

    # Create third part of table 3
    table_2_3 = table_1.groupby(["provincia", "categoria"]).categoria.count().to_frame().T
    table_2_3.reset_index(inplace=True)
    table_2_3.drop(columns=[("index", "")], inplace=True)
    table_2_3.columns = table_2_3.columns.to_flat_index()
    columns = [f"{x[0]}_{x[1]}" for x in table_2_3.columns]
    table_2_3.columns = columns

    # Concatenate the 3 tables
    table_2 = pd.concat([table_2_1, table_2_2, table_2_3], axis=1)

    """Process to make table 3"""
    logger.info(f"Creating table 3...")

    grouped1 = df_salas_cine.groupby(["Provincia"]).sum()[["Pantallas", "Butacas"]]
    grouped2 = df_salas_cine.groupby(["Provincia"]).count()["espacio_INCAA"].to_frame()
    table_3 = pd.concat([grouped1, grouped2], axis=1).reset_index()
    table_3.columns = ["Provincias", "Cantidad de pantallas", "Cantidad de butacas", "Cantidad de espacios INCAA"]

    tables = [table_1, table_2, table_3]

    logger.info(f"Finish to process the data")

    return tables
