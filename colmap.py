import os
import subprocess
from pathlib import Path
from nerfstudio.process_data.colmap_utils import run_colmap
import torch

# 1. Настройка путей (используйте raw strings)
image_dir = Path(r"C:\Users\NNtrack\nurf\nurf\dataset")  # Замените на реальный путь
colmap_dir = Path(r"C:\Program Files\COLMAP\COLMAP-3.8-windows-no-cuda")
colmap_bat = colmap_dir / "COLMAP.bat"
workspace_path = Path(r"C:\Users\NNtrack\nurf\nurf\colmap_output")  # Создайте эту папку заранее

# 2. Проверка существования путей
if not colmap_bat.exists():
    raise FileNotFoundError(f"COLMAP.bat не найден по пути: {colmap_bat}")
if not image_dir.exists():
    raise FileNotFoundError(f"Папка с изображениями не найдена: {image_dir}")

# 3. Создание рабочей директории
workspace_path.mkdir(exist_ok=True, parents=True)

try:
    # Вариант 1: Через nerfstudio (может не работать на Windows)
    run_colmap(
        image_dir=str(image_dir),
        colmap_cmd=str(colmap_bat),  # Явное указание пути к COLMAP.bat
        camera_model="OPENCV",
        verbose=True,
        matching_method="exhaustive",
        colmap_args="--quality high"
    )
except Exception as e:
    print(f"Ошибка при вызове через nerfstudio: {e}")
    print("Пробуем альтернативный метод...")

    # Вариант 2: Прямой вызов COLMAP (более надежный на Windows)
    cmd = [
        str(colmap_bat),
        "automatic_reconstructor",
        "--image_path", str(image_dir),
        "--workspace_path", str(workspace_path),
        "--camera_model", "OPENCV",
        "--quality", "high",
        "--use_gpu", "1" if torch.cuda.is_available() else "0"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("COLMAP успешно завершил работу!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка COLMAP (код {e.returncode}):")
        print("1. Убедитесь, что CUDA установлена (для GPU-версии)")
        print("2. Попробуйте запустить COLMAP вручную через командную строку:")
        print("   ", " ".join(f'"{x}"' if " " in x else x for x in cmd))