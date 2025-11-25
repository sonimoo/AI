from collections import deque

# -------------------------------------------------------------
# Кодирование состояния:
# ('L' или 'R' для положения лодки, Волка, Козы и Капусты)
# Пример: ('L','L','R','L')
# -------------------------------------------------------------

def is_valid(state):
    """Проверка допустимости состояния."""
    F, W, G, C = state
    if F != G and W == G:  # Волк и Коза одни на одном берегу
        return False
    if F != G and G == C:  # Коза и Капуста на одном берегу
        return False
    return True

def move(state, item=None):
    """Генерирует новое состояние. item = кого фермер берет с собой (None = фермер один)."""
    F, W, G, C = state
    new_F = 'R' if F == 'L' else 'L'
    new_W, new_G, new_C = W, G, C

    if item == 'W' and W == F:
        new_W = new_F
    elif item == 'G' and G == F:
        new_G = new_F
    elif item == 'C' and C == F:
        new_C = new_F

    new_state = (new_F, new_W, new_G, new_C)
    return new_state if is_valid(new_state) else None

def get_neighbors(state):
    """Все возможные переходы."""
    moves = [None, 'W', 'G', 'C']  # фермер один или с кем-то
    result = []
    for m in moves:
        nxt = move(state, m)
        if nxt is not None:
            result.append(nxt)
    return result

# -------------------------------------------------------------
# BFS — поиск в ширину
# -------------------------------------------------------------
def bfs(start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        state, path = queue.popleft()
        if state == goal:
            return path
        for nxt in get_neighbors(state):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None

# -------------------------------------------------------------
# A* — простая реализация
# Эвристика: количество элементов не на целевой стороне
# -------------------------------------------------------------
def heuristic(state, goal):
    return sum(s != g for s, g in zip(state, goal))

def astar(start, goal):
    open_list = [(start, [start], 0)]  # состояние, путь, g
    visited = set()
    while open_list:
        open_list.sort(key=lambda x: x[2] + heuristic(x[0], goal))
        state, path, g = open_list.pop(0)
        if state == goal:
            return path
        visited.add(state)
        for nxt in get_neighbors(state):
            if nxt not in visited:
                open_list.append((nxt, path + [nxt], g + 1))
    return None

# -------------------------------------------------------------
# Обратный BFS (поиск от цели к старту)
# -------------------------------------------------------------
def reverse_bfs(goal, start):
    queue = deque([(goal, [goal])])
    visited = {goal}
    while queue:
        state, path = queue.popleft()
        if state == start:
            return path[::-1]  # возвращаем в правильном порядке
        for nxt in get_neighbors(state):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None


def print_path(path):
    for i, state in enumerate(path):
        F, W, G, C = state
        print(f"Шаг {i}: Лодка = {F}, Волк = {W}, Коза = {G}, Капуста = {C}")
    print(f"Всего шагов: {len(path)-1}\n")

# -------------------------------------------------------------
start_state = ('L', 'L', 'L', 'L')
goal_state  = ('R', 'R', 'R', 'R')

print("BFS путь:")
bfs_path = bfs(start_state, goal_state)
print_path(bfs_path)

print("A* путь:")
astar_path = astar(start_state, goal_state)
print_path(astar_path)

print("Обратный BFS путь:")
rev_path = reverse_bfs(goal_state, start_state)
print_path(rev_path)
