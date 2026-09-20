import os

def create_project_structure():
    print("🚀 در حال ساخت ساختار ریپازیتوری Berlin BESS Spatial Analysis...")
    
    # تعریف پوشه‌ها و فایل‌های درون آن‌ها
    repo_structure = {
        "src": ["__init__.py", "spatial_logic.py"],       # کدهای منطق مکانی و پردازش داده‌ها
        "tests": ["__init__.py", "test_spatial.py"],      # کدهای تست واحد (Unit Tests)
        "data": [],                                       # محل قرارگیری فایل‌های GeoJSON یا CSV (در صورت وجود)
        "notebooks": [],                                  # محل نگهداری فایل‌های ژوپیتر (مثل فایلی که در گام قبل ساختیم)
        "outputs": [],                                    # محل ذخیره خروجی‌ها یا نقشه‌های ثابت
        ".": [                                            # فایل‌های ریشه (Root) پروژه
            "app.py", 
            "requirements.txt", 
            "README.md", 
            ".gitignore"
        ]
    }

    # ایجاد پوشه‌ها و فایل‌ها
    for folder, files in repo_structure.items():
        # ساخت پوشه
        if folder != ".":
            os.makedirs(folder, exist_ok=True)
            path_prefix = folder + "/"
        else:
            path_prefix = ""
            
        # ساخت فایل‌ها
        for file in files:
            file_path = f"{path_prefix}{file}"
            # اگر فایل از قبل وجود نداشت، آن را بساز
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    # نوشتن محتوای پیش‌فرض برای برخی فایل‌های کلیدی
                    if file == "requirements.txt":
                        f.write("streamlit\nstreamlit-folium\npandas\nnumpy\ngeopandas\nfolium\nshapely\nbranca\npytest\n")
                    elif file == ".gitignore":
                        f.write("__pycache__/\n*.pyc\n.pytest_cache/\nvenv/\n.env\n")
                    elif file == "README.md":
                        f.write("# 🗺️ Berlin BESS Spatial Analysis (Peak Shaving)\n\nInteractive GIS tool for optimal Battery Energy Storage System (BESS) placement in Berlin.")
                    else:
                        f.write("") # ساخت فایل خالی برای بقیه موارد
                print(f"  ├── Created file: {file_path}")
            else:
                print(f"  ├── Already exists: {file_path}")

    print("\n✅ ساختار پروژه با موفقیت ایجاد شد! حالا می‌توانید کدنویسی را شروع کنید.")

if __name__ == "__main__":
    create_project_structure()
