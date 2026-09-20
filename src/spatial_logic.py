# src/spatial_logic.py

import geopandas as gpd

def load_data(filepath="data/berlin_grid_data.geojson"):
    """بارگذاری دیتابیس مکانی از مسیر پیش‌فرض"""
    return gpd.read_file(filepath)

def normalize(series, inverse=False):
    """نرمال‌سازی داده‌ها بین صفر و یک با قابلیت معکوس کردن مقادیر"""
    if inverse:
        return (series.max() - series) / (series.max() - series.min())
    return (series - series.min()) / (series.max() - series.min())

def calculate_suitability(gdf, w_grid, w_land, w_solar):
    """محاسبه امتیاز نهایی بر اساس وزن‌های دریافتی از کاربر"""
    gdf['norm_solar'] = normalize(gdf['solar_potential'])
    gdf['norm_land'] = normalize(gdf['land_price'], inverse=True)
    gdf['norm_grid'] = normalize(gdf['grid_congestion'])

    gdf['suitability_score'] = (
        (gdf['norm_grid'] * w_grid) + 
        (gdf['norm_land'] * w_land) + 
        (gdf['norm_solar'] * w_solar)
    )
    
    # مرتب‌سازی بر اساس بهترین امتیاز
    return gdf.sort_values(by='suitability_score', ascending=False)
