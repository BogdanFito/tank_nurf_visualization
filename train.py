import os
from pathlib import Path
from nerfstudio.utils.scripts import run_command

# 1. Настройка окружения для Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Решает проблемы с дублированием библиотек
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Явно указываем GPU

# 2. Пути к данным
data_dir = Path(r"C:\Users\NNtrack\nurf\nurf\nurf_data")
output_dir = Path(r"C:\Users\NNtrack\nurf\nurf\result")
output_dir.mkdir(exist_ok=True, parents=True)

# 3. Команда обучения с оптимизациями для Windows
train_cmd = f"""
ns-train nerfacto \
    --data {data_dir} \
    --output-dir {output_dir} \
    --vis tensorboard \
    --pipeline.model.background-color white \
    --max-num-iterations 20000 \
    --save-only-latest-checkpoint True \
    --pipeline.datamanager.camera-res-scale-factor 0.8 \
    --pipeline.model.disable-scene-contraction True \
    --machine.num-devices 1
"""

# 4. Запуск обучения с обработкой ошибок
try:
    print("Запуск обучения...")
    run_command(train_cmd, verbose=True)

    # Проверка успешного завершения
    if any((output_dir / "nerfacto").glob("*/config.yml")):
        print("\nОбучение успешно завершено!")
    else:
        print("\nОбучение завершено, но выходные файлы не найдены")
except Exception as e:
    print(f"\nОшибка обучения: {str(e)}")
    print("\nРекомендации:")
    print("1. Убедитесь, что CUDA установлена (nvidia-smi в командной строке)")
    print("2. Попробуйте уменьшить разрешение: --pipeline.datamanager.camera-res-scale-factor 0.5")
    print("3. Проверьте наличие transforms.json в папке с данными")