import os  # ОС
import torch  # PyTorch
from torch import nn, optim, utils  # модули PyTorch
from torchvision import datasets, transforms  # для работы с изображениями
from torchvision.models import convnext_tiny
from prepare_data import ImageProcessor  # Импорт правильного класса

class TrainModel:
    def __init__(self):
        self.data_path_save_ml = os.getcwd()  # получение текущего рабочего каталога
        self.data_dir = self.data_path_save_ml
        self.num_classes = len(os.listdir(self.data_dir))  # подсчет количества файлов, папок в data_dir
        self.num_epoch = 20
        self.batch_size = 32
        self.acters = ['Selena Gomez', 'Demi Lovato', 'Jean Reno', 'Robert De Niro', 'Tom Hanks']
        self.model = self.create_model()  # инициализация модели

    def trans(self):  # преобразование изображений
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),  # конвертация в тензор
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        dataset = datasets.ImageFolder(root=self.data_dir, transform=transform)  # загрузка данных из папки
        dataloader = utils.data.DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        return dataloader

    def create_model(self):  # создание модели
        model = convnext_tiny(weights='DEFAULT')  # исправлен параметр weights
        num_features = model.classifier[-1].in_features  # используем последний линейный слой
        model.classifier[-1] = nn.Linear(num_features, self.num_classes)  # используем количество классов из data_dir
        model.to('cpu')  # перемещение на CPU
        return model

    def train_model(self):  # обучение модели
        criterion = nn.CrossEntropyLoss()  # функция потерь
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.model.train()
        dataloader = self.trans()
        for epoch in range(self.num_epoch):
            running_loss = 0.0
            for inputs, labels in dataloader:
                inputs = inputs.to('cpu')
                labels = labels.to('cpu')
                optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
            print(f'Epoch [{epoch + 1} / {self.num_epoch}], Loss: {running_loss / len(dataloader):.4f}')
        self.save_model()

    def save_model(self):
        torch.save(self.model.state_dict(), 'model.pth')

    def preprocess_image(self, image_path):
        processor = ImageProcessor(image_path)  # используем правильный класс
        processed_image = processor.preprocess_image()  # вызываем метод обработки изображения
        return processed_image  # возвращаем обработанное изображение

    def classify_image(self, image_path):
        self.model.load_state_dict(torch.load('model.pth'))
        self.model.eval()
        image = self.preprocess_image(image_path)
        with torch.no_grad():
            outputs = self.model(image)
            res = nn.functional.softmax(outputs, dim=1)
            res_softmax_out = res.tolist()[0]
            res_class = res.argmax(dim=1).item()
        return res_softmax_out, res_class

# Пример использования класса TrainModel:
# train_model = TrainModel()
# train_model.train_model()
