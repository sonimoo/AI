import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры среды
N = 30
width, height = 100, 100
r_neighbor = 15      # радиус поиска соседей
max_speed = 1.5

# создаём 10 случайных препятствий в пределах среды
# каждое препятствие имеет координаты (x, y)
obstacles = np.random.rand(10, 2) * [width, height]  

# Инициализация агентов
# случайные позиции агентов 
positions = np.random.rand(N, 2) * [width, height]

# случайные начальные векторы скорости каждого агента
# каждый вектор ограничен диапазоном [-max_speed, max_speed]
speeds = (np.random.rand(N, 2) - 0.5) * 2 * max_speed

# Функция обновления анимации
def update(frame):
    global positions, speeds

    # массив новых скоростей для всех агентов
    new_speeds = np.zeros_like(speeds)
    
    # перебираем каждого агента
    for i in range(N):
        pos = positions[i]  # текущая позиция агента
        speed = speeds[i]   # текущий вектор скорости агента

        # Поиск соседей 
        # вычисляем векторы от текущего агента до всех остальных
        diffs = positions - pos
        # вычисляем расстояние до всех остальных агентов
        dist = np.linalg.norm(diffs, axis=1)
        # соседями считаются все агенты внутри радиуса r_neighbor, кроме самого себя
        neighbors = (dist < r_neighbor) & (dist > 0)

        # Правила Boids 
        if np.any(neighbors):
            # 1.тянуться к центру соседей
            center = positions[neighbors].mean(axis=0)
            cohesion = (center - pos) * 0.005
            
            # 2. выравниваться по среднему направлению соседей
            alignment = (speeds[neighbors].mean(axis=0) - speed) * 0.05
            
            # 3. отталкиваться от слишком близких соседей
            separation = -np.sum(diffs[neighbors] / (dist[neighbors][:, None] ** 2 + 1e-6), axis=0) * 0.15
        else:
            cohesion = alignment = separation = 0  # если соседей нет

        # Избегание препятствий 
        avoid = np.zeros(2)
        for o in obstacles:
            diff = o - pos
            d = np.linalg.norm(diff)
            if d < 10:  # если агент слишком близко к препятствию
                avoid -= diff / d * 0.5  # отталкиваемся от препятствия

        # Итоговая скорость агента 
        speed += cohesion + alignment + separation + avoid

        # вычисляем текущую скорость (вектор длины speed)
        speed_magnitude = np.linalg.norm(speed)

        # ограничиваем максимальную скорость
        if speed_magnitude > max_speed:
            speed = speed / speed_magnitude * max_speed
            speed_magnitude = max_speed 

        new_speeds[i] = speed  

    # обновляем позиции агентов
    positions += new_speeds
    # если агент вышел за границы, переносим его на противоположную сторону
    positions %= [width, height]

    # обновляем глобальный массив скоростей
    speeds = new_speeds

    # обновляем позиции на графике
    scat.set_offsets(positions)
    return scat,

# Настройка графика
fig, ax = plt.subplots()
scat = ax.scatter(positions[:, 0], positions[:, 1], c='b')
ax.scatter(obstacles[:, 0], obstacles[:, 1], c='r', marker='v')

# задаём границы графика
ax.set_xlim(0, width)
ax.set_ylim(0, height)

# создаём анимацию
ani = FuncAnimation(fig, update, interval=100)
plt.show()
