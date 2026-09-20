import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from src.spatial_logic import normalize, calculate_suitability

@pytest.fixture
def sample_gdf():
    polygons = [
        Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        Polygon([(1, 1), (2, 1), (2, 2), (1, 2)])
    ]
    gdf = gpd.GeoDataFrame({'geometry': polygons}, crs="EPSG:4326")
    gdf['solar_potential'] = [1000, 2000]
    gdf['land_price'] = [500, 1500]
    gdf['grid_congestion'] = [0.2, 0.8]
    return gdf

def test_normalize_normal():
    series = pd.Series([10, 20, 30])
    norm = normalize(series)
    assert norm.iloc[0] == 0.0
    assert norm.iloc[2] == 1.0
    assert norm.iloc[1] == 0.5

def test_normalize_inverse():
    series = pd.Series([10, 20, 30])
    norm_inv = normalize(series, inverse=True)
    assert norm_inv.iloc[0] == 1.0
    assert norm_inv.iloc[2] == 0.0

def test_calculate_suitability(sample_gdf):
    w_grid, w_land, w_solar = 0.5, 0.3, 0.2
    result_gdf = calculate_suitability(sample_gdf, w_grid, w_land, w_solar)
    best_score = result_gdf['suitability_score'].max()
    assert best_score == pytest.approx(0.7)
    assert result_gdf.iloc[0]['suitability_score'] == pytest.approx(0.7)
    assert result_gdf.iloc[1]['suitability_score'] == pytest.approx(0.3)
