import marimo

__generated_with = "0.11.0"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Visualización de datos de cultivos en Canarias

        ```
        conda install geopandas folium seaborn
        ```
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Importar datos""")
    return


@app.cell
def _():
    import geopandas as gpd
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    import folium
    from folium import GeoJson, GeoJsonPopup, GeoJsonTooltip


    import json

    # Configuración de estilo
    plt.figure(figsize=(10, 6))
    rcParams['figure.figsize'] = 8, 6
    sns.set_context('talk')

    # Quito notación científica
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    shp_files = [
        'dat/tenerife/TF_MCultivos_2021.shp',
        'dat/el-hierro/EH_MCultivos_2022.shp',
        'dat/fuerteventura/FV_MCultivos_2020.shp',
        'dat/gran-canaria/GC_MCultivos_2019.shp',
        'dat/la-gomera/LG_MCultivos_2023.shp',
        'dat/lanzarote/LZ_MCultivos_2020.shp',
        'dat/la-palma/LP_MCultivos_2022.shp'
    ]
    return (
        GeoJson,
        GeoJsonPopup,
        GeoJsonTooltip,
        folium,
        gpd,
        json,
        pd,
        plt,
        rcParams,
        shp_files,
        sns,
    )


@app.cell
def _(gpd, pd, shp_files):
    islands_gdfs = []
    for shp in shp_files:
        gdf = gpd.read_file(shp)
        islands_gdfs.append(gdf)

    gdf = gpd.GeoDataFrame(pd.concat(islands_gdfs, ignore_index=True))
    gdf.head()
    return gdf, islands_gdfs, shp


@app.cell
def _(gdf):
    len(gdf)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Limpieza de datos""")
    return


@app.cell
def _(gdf):
    gdf.columns = [col.lower() for col in gdf.columns] # Paso a minúsculas
    gdf.head()
    return


@app.cell
def _(gdf):
    columsn_cleanup = [col for col in gdf.columns if col.endswith('_co')] + ['borde_na', 'disemi_na', 'fecha']
    gdf_1 = gdf.drop(columsn_cleanup, axis=1)
    gdf_1.head()
    return columsn_cleanup, gdf_1


@app.cell
def _(gdf_1):
    gdf_1.info()
    return


@app.cell
def _(gdf_1, pd):
    def show_missing_data():
        total = gdf_1.isnull().sum().sort_values(ascending=False)
        percent_1 = gdf_1.isnull().sum() / gdf_1.isnull().count() * 100
        percent_2 = round(percent_1, 1).sort_values(ascending=False)
        _missing_data = pd.concat([total, percent_2], axis=1, keys=['total', 'pct'])
        return _missing_data[_missing_data.total > 0]
    _missing_data = show_missing_data()
    _missing_data
    return (show_missing_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Viendo los datos, hay un 37% de cultivos que no tienen categoría ni agrupación. Por otro lado, hay un pequeño porcentaje de cultivos que no tienene espeficada la técnica de cultivo. Vamos a corregir primero las categorías y agrupaciones.""")
    return


@app.cell
def _(gdf_1):
    categorias = gdf_1[['cultivo_na', 'categoria', 'agrupacion']].sort_values(by='categoria', na_position='last')
    categorias = categorias.loc[gdf_1.categoria.notnull() & gdf_1.agrupacion.notnull()].drop_duplicates().reset_index(drop=True)
    categorias
    return (categorias,)


@app.cell
def _(categorias, gdf_1):
    tmp = gdf_1.merge(categorias, how='left', on='cultivo_na')
    tmp.head()
    return (tmp,)


@app.cell
def _(gdf_1, tmp):
    gdf_1['categoria'] = tmp['categoria_y'].copy()
    gdf_1['agrupacion'] = tmp['agrupacion_y'].copy()
    gdf_1[gdf_1.categoria.isnull()]
    return


@app.cell
def _(show_missing_data):
    _missing_data = show_missing_data()
    _missing_data
    return


@app.cell
def _(gdf_1):
    gdf_1[gdf_1.categoria.isnull() & gdf_1.agrupacion.isnull()].cultivo_na.unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Los datos de `Pastos Pastizal` y `Pastos Tagasaste` no tienen categoría por lo que voy a inputarselo manualmente viendo la documentación del dataset. Revisando el documento PDF [METODOLOGÍA DEL MAPA DE CULTIVOS DE CANARIAS](https://opendata.sitcan.es/upload/medio-rural/gobcan_mapa-cultivos_metodologia.pdf), los cultivos de Tagasaste y Pastizal se clasifican como **Cereales y Leguminosas**. Por este motivo, voy a aplicarles la categoría de `Otros` y la agrupación `Cereales, Leguminosas y Forrajeras`.""")
    return


@app.cell
def _(gdf_1):
    gdf_1.loc[(gdf_1.cultivo_na == 'Pastos Pastizal') | (gdf_1.cultivo_na == 'Pastos Tagasaste'), 'categoria'] = 'Otros'
    gdf_1.loc[(gdf_1.cultivo_na == 'Pastos Pastizal') | (gdf_1.cultivo_na == 'Pastos Tagasaste'), 'agrupacion'] = 'Cereales, Leguminosas y Forrajeras'
    gdf_1.loc[gdf_1.cultivo_na == 'Pastos Tagasaste', 'cultivo_na'] = 'Tagasaste'
    gdf_1[gdf_1.cultivo_na == 'Pastos Pastizal'].head()
    return


@app.cell
def _(gdf_1):
    gdf_1['tecnica_na'].unique()
    return


@app.cell
def _(gdf_1):
    gdf_1.loc[gdf_1.tecnica_na.isnull(), 'tecnica_na'] = 'No aplica'
    return


@app.cell
def _(gdf_1):
    gdf_1['tecnica_na'] = gdf_1['tecnica_na'].apply(lambda x: 'No aplica' if x == '' else x)
    gdf_1['tecnica_na'].unique()
    return


@app.cell
def _(gdf_1):
    gdf_1['regadio_na'] = gdf_1['regadio_na'].apply(lambda x: 'Si' if x == 'Sí' else x)
    gdf_1['regadio_na'].unique()
    return


@app.cell
def _(gdf_1):
    gdf_1['abandon_type'] = gdf_1['abandon_na'].apply(lambda x: 'Abandonado' if x in ['Sí, cultivo abandonado'] else 'Prolongado' if x == 'Sí, prolongado' else 'Reciente' if x == 'Sí, reciente' else 'No aplica')
    return


@app.cell
def _(gdf_1):
    gdf_1['abandon_na'] = gdf_1['abandon_na'].apply(lambda x: 'Si' if x != 'No' else 'No')
    return


@app.cell
def _(gdf_1):
    gdf_1['area_ha'] = gdf_1['area_m2'] / 1000
    return


@app.cell
def _(gdf_1):
    gdf_1.head()
    return


@app.cell
def _(show_missing_data):
    _missing_data = show_missing_data()
    _missing_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Ya tengo los datos limpios y listos para ser consultados""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Para simplificar el dataset voy a convertir las asociaciones en el cultivo principal (por ejemplo, Asociacion Viña-Barbecho será Viña):""")
    return


@app.cell
def _(gdf_1):
    def print_categorias():
        print(f'Categorías: {gdf_1.categoria.unique()}\n')
        print(f'Agrupaciones: {gdf_1.agrupacion.unique()}\n')
        print(f'Cultivos: {gdf_1.cultivo_na.unique()}\n')
    print_categorias()
    return (print_categorias,)


@app.cell
def _(gdf_1):
    gdf_1.loc[gdf_1.agrupacion.str.contains('^Pastoreo', regex=True), ['agrupacion', 'categoria', 'cultivo_na']] = 'Pastoreo'
    return


@app.cell
def _(gdf_1):
    gdf_1['agrupacion'] = gdf_1['agrupacion'].str.replace('^A\\. ', '', regex=True)
    gdf_1.loc[gdf_1.agrupacion == 'Templados', 'agrupacion'] = 'Frutales Templados'
    return


@app.cell
def _(gdf_1):
    gdf_1['cultivo_na'] = gdf_1['cultivo_na'].str.replace('^Asociación ', '', regex=True)
    gdf_1['cultivo_na'] = gdf_1['cultivo_na'].str.split('-').str[0]
    return


@app.cell
def _(print_categorias):
    print_categorias()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Exploración inicial de datos""")
    return


@app.cell
def _(gdf_1):
    gdf_1.isla_na.unique()
    return


@app.cell
def _(print_categorias):
    print_categorias()
    return


@app.cell
def _(gdf_1):
    gdf_1['tecnica_na'].unique()
    return


@app.cell
def _(gdf_1):
    gdf_1['abandon_na'].unique()
    return


@app.cell
def _(gdf_1):
    gdf_1['regadio_na'].unique()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Procesado de datos: unión con municipios""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Finalmente, voy a mergear un shp con las delimitaciones de los municipios de cada isla para sacar métricas sobre los cultivos desglosados por cada municipio""")
    return


@app.cell
def _(gpd):
    gdf_mun = gpd.read_file('dat/municipios/municipios.shp', encoding='utf-8')
    gdf_mun.columns = [col.lower() for col in gdf_mun.columns] # Paso a minúsculas
    gdf_mun.head(3)
    return (gdf_mun,)


@app.cell
def _(gdf_mun):
    gdf_mun_1 = gdf_mun[['etiqueta', 'geometry']]
    gdf_mun_1.head()
    return (gdf_mun_1,)


@app.cell
def _(gdf_1, gdf_mun_1):
    gdf_2 = gdf_1.to_crs(gdf_mun_1.crs)
    return (gdf_2,)


@app.cell
def _(gdf_2, gdf_mun_1, gpd):
    gdf_joined_mun = gpd.sjoin(gdf_2, gdf_mun_1, how='left', predicate='covered_by')
    gdf_joined_mun = gdf_joined_mun.rename(columns={'etiqueta': 'municipio'})
    gdf_joined_mun = gdf_joined_mun.drop(['index_right'], axis=1)
    gdf_joined_mun.head()
    return (gdf_joined_mun,)


@app.cell
def _(gdf_joined_mun):
    len(gdf_joined_mun[gdf_joined_mun.municipio.isnull()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Mostrando en el mapa las parcelas de cultivo que no tienen municipio asignado, podemos observar que dichas parcelas no han sido asignadas a un municipio ya que caen justo en las lindes de algunos municipios por lo que le merge no le asigna ningún municipio.

        Para arreglarlo, dependiendo del porcentaje de área que caiga en cada municipio, se asignará a un municipio u a otro.
        """
    )
    return


@app.cell
def _(GeoJson, folium, gdf_joined_mun):
    gdf_joined_mun_no_muni = gdf_joined_mun[gdf_joined_mun.municipio.isnull()].to_crs(epsg=4326)

    center = [28.1464, -15.4293]
    map = folium.Map(location=center, zoom_start=7.5)
    GeoJson(gdf_joined_mun_no_muni).add_to(map)
    map
    return center, gdf_joined_mun_no_muni, map


@app.cell
def _(gdf_joined_mun, gdf_mun_1):
    gdf_joined_mun_1 = gdf_joined_mun.to_crs(epsg=4083)
    gdf_mun_projected = gdf_mun_1.to_crs(epsg=4083)
    return gdf_joined_mun_1, gdf_mun_projected


@app.cell
def _(gdf_mun_projected, gpd):
    def calcular_municipio_segun_area_overlay(parcela):
        """
        Calcula el municipio para una parcela basándose en el mayor porcentaje de área intersectada.

        Parameters:
            parcela (GeoSeries): Fila del GeoDataFrame de parcelas.

        Returns:
            str: Nombre del municipio con mayor área intersectada o None si no hay intersección.
        """
        parcela_gdf = gpd.GeoDataFrame([parcela], geometry='geometry', crs=gdf_mun_projected.crs)

        intersecciones = gpd.overlay(parcela_gdf, gdf_mun_projected, how='intersection')

        if intersecciones.empty:
            print('Este es empty')
            return None

        intersecciones['area_interseccion'] = intersecciones.geometry.area

        municipio_mayor_area = intersecciones.loc[intersecciones['area_interseccion'].idxmax(), 'etiqueta']

        return municipio_mayor_area
    return (calcular_municipio_segun_area_overlay,)


@app.cell
def _(calcular_municipio_segun_area_overlay, gdf_joined_mun_1, pd):
    gdf_joined_mun_1['municipio'] = gdf_joined_mun_1.apply(lambda row: calcular_municipio_segun_area_overlay(row) if pd.isnull(row['municipio']) else row['municipio'], axis=1)
    gdf_joined_mun_1.head()
    return


@app.cell
def _(gdf_joined_mun_1):
    gdf_joined_mun_1[gdf_joined_mun_1.municipio.isnull()]
    return


@app.cell
def _(gdf_joined_mun_1):
    gdf_3 = gdf_joined_mun_1.copy()
    return (gdf_3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Visualización de datos""")
    return


@app.cell
def _(print_categorias):
    print_categorias()
    return


@app.cell
def _(gdf_3):
    gdf_abandonada = gdf_3[(gdf_3['categoria'] == 'Superficie agrícola no utilizada') | (gdf_3['abandon_na'] == 'Si')]['area_m2'].sum()
    gdf_cultivada_o_pastoreo = gdf_3[~((gdf_3['categoria'] == 'Superficie agrícola no utilizada') | (gdf_3['abandon_na'] == 'Si'))]['area_m2'].sum()
    gdf_cultivado = gdf_3[~((gdf_3['categoria'] == 'Superficie agrícola no utilizada') | (gdf_3['categoria'] == 'Pastoreo') | (gdf_3['abandon_na'] == 'Si'))]
    return gdf_abandonada, gdf_cultivada_o_pastoreo, gdf_cultivado


@app.cell
def _(gdf_abandonada, gdf_cultivada_o_pastoreo, pd, plt, sns):
    _data = {'Tipo de Superficie': ['Abandonada', 'Cultivada y pastoreo'], 'Área (m²)': [gdf_abandonada, gdf_cultivada_o_pastoreo]}
    _df_plot = pd.DataFrame(_data)
    plt.figure(figsize=(8, 8))
    colors = sns.color_palette('Set1')
    plt.pie(_df_plot['Área (m²)'], labels=_df_plot['Tipo de Superficie'], autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Distribución de la Superficie Agrícola')
    plt.show()
    return (colors,)


@app.cell
def _(gdf_abandonada, gdf_cultivada_o_pastoreo, pd, plt, sns):
    _data = {'Tipo de Superficie': ['Abandonada o sin uso', 'Cultivada'], 'Superficie (m2)': [gdf_abandonada, gdf_cultivada_o_pastoreo]}
    _df_plot = pd.DataFrame(_data)
    sns.barplot(data=_df_plot, y='Tipo de Superficie', x='Superficie (m2)', hue='Tipo de Superficie', orient='h', palette='Set1')
    plt.title('Comparación de Superficie: Abandonada o Sin Uso vs Cultivada')
    plt.xlabel('Superficie Total (m2)')
    plt.ylabel('Tipo de Superficie')
    plt.show()
    return


@app.cell
def _(gdf_cultivado, pd, plt, sns):
    cultivo_areas = gdf_cultivado.groupby('cultivo_na')['area_m2'].sum().reset_index()
    cultivo_areas = cultivo_areas.sort_values(by='area_m2', ascending=False)
    top_20 = cultivo_areas.head(17)
    _otros = pd.DataFrame({'cultivo_na': ['Otros'], 'area_m2': [cultivo_areas.iloc[17:]['area_m2'].sum()]})
    cultivo_areas_top = pd.concat([top_20, _otros])
    sns.barplot(data=cultivo_areas_top, x='area_m2', y='cultivo_na', hue='cultivo_na', palette='Set1', orient='h', legend=False)
    plt.title('Top 20 cultivos por área cultivada (m²)')
    plt.xlabel('Superficie Total (m²)')
    plt.ylabel('Cultivo')
    plt.show()
    return cultivo_areas, cultivo_areas_top, top_20


@app.cell
def _(gdf_cultivado, pd, plt, sns):
    cultivos_por_isla = gdf_cultivado.groupby(['isla_na', 'cultivo_na'])['area_m2'].sum().reset_index()
    cultivos_por_isla['area_ha'] = cultivos_por_isla['area_m2'] / 10000
    islas = cultivos_por_isla['isla_na'].unique()
    for isla in islas:
        cultivos_isla = cultivos_por_isla[cultivos_por_isla['isla_na'] == isla]
        cultivos_isla = cultivos_isla.sort_values(by='area_ha', ascending=False)
        top_10 = cultivos_isla.head(10)
        _otros = pd.DataFrame({'isla': [isla], 'cultivo_na': ['Otros'], 'area_ha': [cultivos_isla.iloc[10:]['area_ha'].sum()]})
        cultivos_isla_top = pd.concat([top_10, _otros])
        plt.figure(figsize=(8, 6))
        sns.barplot(data=cultivos_isla_top, x='area_ha', y='cultivo_na', orient='h', palette='Set1', hue='cultivo_na', dodge=False, legend=False)
        plt.title(f'Distribución de cultivos en {isla}')
        plt.xlabel('Superficie Total (ha)')
        plt.ylabel('Cultivo')
        plt.tight_layout()
        plt.show()
    return (
        cultivos_isla,
        cultivos_isla_top,
        cultivos_por_isla,
        isla,
        islas,
        top_10,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Se puede observar que la distribución de los cultivos en cada isla es diferente según su extensión, clima, etc. Aunque la platanera sea el cultivo con mayor superficie utilizada, en algunas islas no es el cultivo con mayor superficie. Por ejemplo, en Lanzarote el cultivo con mayor superficie dedicada es la viña.""")
    return


@app.cell
def _(gdf_cultivado, plt):
    df_grouped = gdf_cultivado.groupby(['cultivo_na', 'regadio_na'])['area_ha'].sum().reset_index()

    # Calcular el total de área por cultivo
    total_area = gdf_cultivado.groupby('cultivo_na')['area_ha'].sum().reset_index()
    total_area.rename(columns={'area_ha': 'total_area'}, inplace=True)

    # Unir el total al DataFrame original
    df_normalized = df_grouped.merge(total_area, on='cultivo_na')

    # Calcular el porcentaje
    df_normalized['percentage'] = (df_normalized['area_ha'] / df_normalized['total_area']) * 100

    # Crear la tabla pivotada para barras apiladas
    df_pivot = df_normalized.pivot(index='cultivo_na', columns='regadio_na', values='percentage').fillna(0)
    df_sorted = df_pivot.sort_values(by='Si', ascending=False)

    # Crear la gráfica apilada con datos ordenados
    plt.figure(figsize=(12, 6))
    df_sorted.plot(kind='bar', stacked=True, color=['#4c72b0', '#dd8452'], figsize=(12, 6))

    # Ajustar etiquetas y título
    plt.xlabel('Cultivo')
    plt.ylabel('Porcentaje (%)')
    plt.title('Porcentaje de área por cultivo según uso de regadío')
    plt.xticks(rotation=45, ha='right')

    # Ajustar la leyenda
    plt.legend(
        title='Uso de Regadío',
        labels=['No', 'Sí'],
        loc='lower left',  # Ubicar la leyenda en la parte inferior izquierda
        bbox_to_anchor=(0, -0.9)  # Ajustar el desplazamiento hacia abajo
    )

    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()
    return df_grouped, df_normalized, df_pivot, df_sorted, total_area


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
