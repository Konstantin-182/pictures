import os  # для работы с операционной системой
import torchvision.transforms as transforms  # для преобразований изображений
from PIL import Image  # модуль для работы с изображениями в Python

class ImageProcessor:
    def __init__(self, image_path):  # метод инициализации
        self.data_path_save_ml = os.getcwd()  # сохраняем текущую директорию
        self.data_dir = os.path.join(self.data_path_save_ml, 'pictures')  # определяем директорию для хранения изображений
        os.makedirs(self.data_dir, exist_ok=True)  # создаем каталог, если он не существует
        self.img_path = image_path  # путь к изображению

    def preprocess_image(self):  # метод предварительной обработки изображения
        # выполняем все преобразования, необходимые для обработки изображения перед его передачей в модель
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),  # конвертация в тензор
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        image = Image.open(self.img_path)  # открываем изображение по указанному пути
        image = transform(image).unsqueeze(0)  # применяем преобразование и добавляем размерность
        return image  # возвращаем обработанное изображение

if __name__ == '__main__':
    # Пример использования
    image_path = 'path_to_your_image.jpg'  # замените на ваш путь к изображению
    processor = ImageProcessor(image_path)
    processed_image = processor.preprocess_image()
    print("Изображение успешно обработано.")
