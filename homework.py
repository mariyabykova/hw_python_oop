from dataclasses import asdict, dataclass
from typing import Dict, List

MIN_IN_H = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.

    Аргументы:
    training_type -- вид тренировки
    duration -- продолжительность тренировки (часы)
    distance -- расстояние (км)
    speed -- скорость (км/ч)
    calories -- израсходованные килокалории (ккал)
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    default_message = (
        'Тип тренировки: {training_type};'
        ' Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км;'
        ' Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self, info_message: str = default_message) -> str:
        return info_message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки.

    Аргументы:
    action -- количество совершенных действий
    duration -- продолжительность тренировки (часы)
    weight -- вес (кг)
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод get_spent_calories обязательно'
            'должен быть переопределен в дочерних классах'
        )
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:

        mean_speed = self.get_mean_speed()
        specific_calories = (
            (self.COEFF_CALORIE_1 * mean_speed - self.COEFF_CALORIE_2)
            / self.M_IN_KM
        )
        duration_min = self.duration * MIN_IN_H
        spent_calories = specific_calories * self.weight * duration_min
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Аргумент:
    height -- рост (см)
    """

    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029

    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        mean_speed = self.get_mean_speed()
        specific_calories = (
            self.COEFF_CALORIE_1 * self.weight
            + mean_speed**2 // self.height
            * self.COEFF_CALORIE_2 * self.weight
        )
        spent_calories = (
            specific_calories
            * self.duration
            * MIN_IN_H
        )
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание.

    Аргументы:
    length_pool -- длина бассейна (м)
    count_pool -- сколько раз пользователь пересек бассейн
    """

    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        length = self.length_pool * self.count_pool
        mean_speed = length / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        average_speed = self.get_mean_speed()
        spent_calories = (
            (average_speed + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: Dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
        except KeyError:
            print(
                f'{workout_type} - неизвестный тип тренировки.'
                f'workout_type может включать'
                f'только следующие виды тренировок:'
                f'"SWM", "RUN", "WLK"'
            )
        main(training)
