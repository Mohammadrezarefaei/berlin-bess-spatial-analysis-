import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import os

def generate_and_save_data():
    print("⏳ در حال تولید داده‌های مکانی و پارامترهای شبکه برلین...")
    
    # 1. تعریف مرزهای نقشه برلین و ساخت گرید
    berlin_bbox = {'min_lon': 13.1, 'max_lon': 13.7, 'min_lat': 52.35, 'max_lat': 52.65}
    grid_size = 0.05
    polygons = []
    
    for lon in np.arange(berlin_bbox['min_lon'], berlin_bbox['max_lon'], grid_size):
        for lat in np.arange(berlin_bbox['min_lat'], berlin_bbox['max_lat'], grid_size):
            polygons.append(Polygon([
                (lon, lat),
                (lon + grid_size, lat),
                (lon + grid_size, lat + grid_size),
                (lon, lat + grid_size)
            ]))
            
    gdf_berlin = gpd.GeoDataFrame({'geometry': polygons}, crs="EPSG:4326")
    
    # 2. تولید داده‌های مصنوعی (ترافیک شبکه، قیمت زمین، پتانسیل خورشیدی)
    np.random.seed(42)
    num_cells = len(gdf_berlin)
    
    gdf_berlin['solar_potential'] = np.random.uniform(500, 2000, num_cells)
    gdf_berlin['land_price'] = np.random.uniform(100, 1500, num_cells)
    gdf_berlin['grid_congestion'] = np.random.uniform(0.1, 0.95, num_cells)
    
    # 3. ذخیره در پوشه data با فرمت استاندارد GeoJSON
    os.makedirs('data', exist_ok=True)
    output_path = 'data/berlin_grid_data.geojson'
    
    # حذف فایل قبلی اگر وجود داشت تا خطای تداخل ندهد
    if os.path.exists(output_path):
        os.remove(output_path)
        
    gdf_berlin.to_file(output_path, driver='GeoJSON')
    print(f"✅ فایل پایگاه داده مکانی با موفقیت در مسیر ساخته شد: {output_path}")

if __name__ == "__main__":
    generate_and_save_data()
