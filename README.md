# Визуализация облета танка
Цель: помощью NeRF сделать видео-рендер некоторого объекта (объект должен быть реальным в вашем распоряжении, а не датасет), на котором он вращается (камера вокруг него) на полный оборот вокруг вертикальной оси
 
Задачи
1. Найти подходящее решение, можно использовать готовые 
2. Собрать датасет для своего объекта. Просьба сделать такое фото, чтобы было понятно, что это не из интернета. Например, на фоне этого сообщения или с собой и так далее
3. Путем обучения NeRF-сети получить представление объекта
4. С помощью обученной NeRF-сети сгенерировать короткий ролик, где объект вращается (камера вокруг него) на полный оборот вокруг вертикальной оси

## Порядок выполнения
1. Был собран датасет с танком (со всех соторон на 360 градусов) - в папке dataset
2. В файле colmap.py была выполнена обработка датасета с поощью COLMAP
3. В файле colmap_to_json.py с помощью скрипта colmap2nerf.py был получен файл transforms.json (для обучения модели)
4. В директорию nurf_data был скопирован датасет (в папку images)
5. Был запущен скрипт обучения модели
 ```bash
ns-train nerfacto --data {data_dir} --output-dir {output_dir} --max-num-iterations 3000 --pipeline.datamanager.camera-res-scale-factor 0.5
 ```
6. Рендеринг видео
```bash
ns-render spiral --load-config "C:\Users\NNtrack\nurf\nurf\result\nurf_data\nerfacto\2025-05-22_151843\config.yml" --output-path "C:\Users\NNtrack\nurf\nurf\result\nurf_data\nerfacto\2025-05-22_151843\render.mp4" --radius 3.0 
```

## Итоговый результат
