from pathlib import Path
import subprocess
import shutil
import sys

# Пути (лучше использовать абсолютные)
colmap_dir = Path(r"C:\Users\NNtrack\nurf\nurf\colmap_output").resolve()
colmap_dir_2 = Path(r"C:\Program Files\COLMAP\COLMAP-3.8-windows-no-cuda").resolve()
output_dir = Path(r"C:\Users\NNtrack\nurf\nurf\nurf_data").resolve()
sparse_dir = colmap_dir / "sparse" / "0"
colmap_bat = (colmap_dir_2 / "COLMAP.bat").resolve()

# Создаем выходной каталог если не существует
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Проверка существования файлов COLMAP
required_files = ["cameras.bin", "images.bin", "points3D.bin"]
missing_files = [f for f in required_files if not (sparse_dir / f).exists()]

if missing_files:
    print(f"Отсутствуют файлы COLMAP: {missing_files}")
    print("Попробуйте перезапустить COLMAP:")
    print(f"colmap automatic_reconstructor --image_path {colmap_dir / 'images'} --workspace_path {colmap_dir}")
    sys.exit(1)

# 2. Попытка конвертации через Python
try:
    from nerfstudio.process_data.colmap_utils import colmap_to_json

    colmap_to_json(
        recon_dir=colmap_dir,
        output_dir=output_dir
    )
    print("Успешно создано через colmap_to_json()")
except Exception as e:
    print(f"Ошибка Python-конвертации: {e}")

    # 3. Альтернатива: конвертация в TXT и обработка
    try:
        # Проверяем существование COLMAP.bat
        if not colmap_bat.exists():
            raise FileNotFoundError(f"COLMAP.bat не найден по пути: {colmap_bat}")

        # Конвертируем бинарные файлы в TXT
        subprocess.run([
            str(colmap_bat), "model_converter",
            "--input_path", str(sparse_dir),
            "--output_path", str(sparse_dir),
            "--output_type", "TXT"
        ], check=True)

        # Создаем transforms.json вручную
        subprocess.run([
            "python", "-m", "colmap2nerf",
            "--colmap_matcher", "exhaustive",
            "--aabb_scale", "16",
            "--images", str(colmap_dir / "images"),
            "--text", str(sparse_dir),
            "--out", str(output_dir / "transforms.json")
        ], check=True)

        print("Успешно создано через colmap2nerf.py")

    except Exception as alt_e:
        print(f"Ошибка альтернативного метода: {alt_e}")
        print("\nРучное решение:")
        print("1. Откройте командную строку в папке проекта")
        print(f"2. Выполните: colmap model_converter --input_path {sparse_dir} --output_path {sparse_dir} --output_type TXT")
        print(f"3. Затем: python -m nerfstudio.scripts.colmap2nerf --images {colmap_dir / 'images'} --text {sparse_dir} --out {output_dir / 'transforms.json'}")
        sys.exit(1)