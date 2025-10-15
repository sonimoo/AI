import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button


N, M = 30, 30
prob_live = 0.3          # вероятность того, что клетка изначально живая


# создаём случайную сетку клеток: 1 = живая, 0 = мёртвая
grid = np.random.choice([0, 1], size=(N, M), p=[1 - prob_live, prob_live])

# Функция подсчёта соседей 
def count_neighbors(g, x, y):
    # возвращает количество живых соседей клетки (x, y)
    return np.sum(g[(x-1):(x+2) % N, (y-1):(y+2) % M]) - g[x, y]

# Функция одного шага игры
def step(grid):
    """
    Применяет правила Конвея к каждой клетке сетки:
    - Живые клетки с <2 или >3 соседями умирают
    - Живые с 2-3 соседями продолжают жить
    - Мёртвые клетки с ровно 3 соседями оживают
    """
    new_grid = np.zeros_like(grid)  # создаём новую сетку
    for i in range(N):
        for j in range(M):
            n = 0
            # перебираем все соседние клетки
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue  # пропускаем саму клетку
                    # учитываем границы соединены
                    n += grid[(i + di) % N, (j + dj) % M]
            # применяем правила Конвея
            if grid[i, j] == 1:
                new_grid[i, j] = 1 if n in [2, 3] else 0
            else:
                new_grid[i, j] = 1 if n == 3 else 0
    return new_grid

# Функция для добавления паттерна Blinker
def add_blinker(event=None):
    """
    Добавляет осциллирующий паттерн Blinker в случайное место сетки.
    Blinker — 3 живые клетки в ряд (горизонтально).
    """
    blinker = np.array([[1, 1, 1]])
    r = np.random.randint(0, N - 1)   # случайная строка
    c = np.random.randint(0, M - 3)   # случайный столбец
    grid[r:r+1, c:c+3] = blinker     # вставляем паттерн
    print(f"Blinker добавлен в ({r}, {c})")

# Настройка визуализации
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # оставляем место для кнопки
# создаём изображение сетки
img = ax.imshow(grid, cmap='gray', interpolation='nearest')
ax.set_title("Conway's Game of Life")

# Кнопка для добавления Blinker
ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])  # положение кнопки
btn = Button(ax_button, "Добавить Blinker")
btn.on_clicked(add_blinker)

# Обновление анимации
def update(frame):
    """
    Обновляет сетку для следующего кадра анимации
    """
    global grid
    grid[:] = step(grid)     # вычисляем следующее поколение
    img.set_data(grid)       # обновляем изображение
    return img,

# Запуск анимации 
ani = FuncAnimation(fig, update, interval=500, blit=True)
plt.show()
