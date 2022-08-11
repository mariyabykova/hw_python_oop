class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        info_message = (f'Тип тренировки: {self.training_type};'
                        f' Длительность: {self.duration:.3f} ч.;'
                        f' Дистанция: {self.distance:.3f} км;'
                        f' Ср. скорость: {self.speed:.3f} км/ч;'
                        f' Потрачено ккал: {self.calories:.3f}.')
        return info_message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        COEFF_CALORIE_1 = 18
        COEFF_CALORIE_2 = 20
        mean_speed = self.get_mean_speed()
        specific_calories = (
            (COEFF_CALORIE_1 * mean_speed - COEFF_CALORIE_2)
            / self.M_IN_KM
        )
        duration_min = self.duration * self.MIN_IN_H
        spent_calories = specific_calories * self.weight * duration_min
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1 = 0.035
        COEFF_CALORIE_2 = 0.029
        mean_speed = self.get_mean_speed()
        specific_calories = (
            COEFF_CALORIE_1 * self.weight
            + mean_speed**2 // self.height
            * COEFF_CALORIE_2 * self.weight
        )
        spent_calories = (
            specific_calories
            * self.duration
            * self.MIN_IN_H
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        length = self.length_pool * self.count_pool
        mean_speed = length / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        COEFF_CALORIE_1 = 1.1
        COEFF_CALORIE_2 = 2
        average_speed = self.get_mean_speed()
        spent_calories = (
            (average_speed + COEFF_CALORIE_1)
            * COEFF_CALORIE_2
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict: dict[str, Training] = {'SWM': Swimming,
                                         'RUN': Running,
                                         'WLK': SportsWalking}
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
        training = read_package(workout_type, data)
        main(training)
