from collections import deque
import time
import heapq

# ОПИСАНИЕ СРЕДЫ (МИНИМАЛЬНОЕ)

WIDTH = 2
HEIGHT = 2

BASE = (0, 0)           # начальная позиция
ITEM_POS = (1, 1)       # место, где лежит предмет

def make_state(x, y, has_item):
    """Создаёт состояние (клетка + взят ли предмет)."""
    return (x, y, has_item)

START_STATE = make_state(BASE[0], BASE[1], False)
GOAL_STATE = make_state(BASE[0], BASE[1], True)

def is_inside(x, y):
    return 0 <= x < WIDTH and 0 <= y < HEIGHT

def is_goal(state):
    return state == GOAL_STATE

def successors_forward(state):
    x, y, has_item = state
    result = []
    moves = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
    for name, (dx, dy) in moves:
        nx, ny = x + dx, y + dy
        if is_inside(nx, ny):
            result.append((make_state(nx, ny, has_item), f"move_{name}"))
    if (x, y) == ITEM_POS and not has_item:
        result.append((make_state(x, y, True), "pickup"))
    return result

def predecessors_backward(state):
    x, y, has_item = state
    result = []
    moves = [("up", (0, -1)), ("down", (0, 1)), ("left", (-1, 0)), ("right", (1, 0))]
    for name, (dx, dy) in moves:
        px, py = x - dx, y - dy
        if is_inside(px, py):
            result.append((make_state(px, py, has_item), f"move_{name}_back"))
    if (x, y) == ITEM_POS and has_item:
        result.append((make_state(x, y, False), "unpickup"))
    return result

def heuristic(state):
    x, y, has_item = state
    dist_to_base = abs(x - BASE[0]) + abs(y - BASE[1])
    dist_to_item = abs(x - ITEM_POS[0]) + abs(y - ITEM_POS[1])
    item_to_base = abs(ITEM_POS[0] - BASE[0]) + abs(ITEM_POS[1] - BASE[1])
    if not has_item:
        return dist_to_item + item_to_base
    else:
        return dist_to_base

def reconstruct_path(parents, end_state):
    path = []
    s = end_state
    while s is not None:
        path.append(s)
        s = parents.get(s)
    path.reverse()
    return path

# ==========================
# Прямой BFS
# ==========================
def bfs_forward():
    start_time = time.perf_counter()
    queue = deque([START_STATE])
    parents = {START_STATE: None}
    visited_count = 0
    generated_count = 0
    found_state = None
    while queue:
        state = queue.popleft()
        visited_count += 1
        if is_goal(state):
            found_state = state
            break
        for new_state, _ in successors_forward(state):
            generated_count += 1
            if new_state not in parents:
                parents[new_state] = state
                queue.append(new_state)
    elapsed = time.perf_counter() - start_time
    if found_state is None:
        return None, visited_count, generated_count, 0.0, elapsed
    path = reconstruct_path(parents, found_state)
    b = generated_count / visited_count if visited_count else 0.0
    return path, visited_count, generated_count, b, elapsed

# ==========================
# A* поиск
# ==========================
def astar_forward():
    start_time = time.perf_counter()
    heap = []
    counter = 0

    g_scores = {START_STATE: 0}
    parents = {START_STATE: None}
    in_open = {START_STATE}
    visited_count = 0
    generated_count = 0
    found_state = None

    heapq.heappush(heap, (heuristic(START_STATE), counter, START_STATE))

    while heap:
        f, _, state = heapq.heappop(heap)
        if state not in in_open:
            continue
        in_open.remove(state)
        visited_count += 1

        if is_goal(state):
            found_state = state
            break

        g_current = g_scores[state]

        for new_state, _ in successors_forward(state):
            generated_count += 1
            tentative_g = g_current + 1
            if new_state not in g_scores or tentative_g < g_scores[new_state]:
                g_scores[new_state] = tentative_g
                parents[new_state] = state
                counter += 1
                heapq.heappush(heap, (tentative_g + heuristic(new_state), counter, new_state))
                in_open.add(new_state)

    elapsed = time.perf_counter() - start_time
    if found_state is None:
        return None, visited_count, generated_count, 0.0, elapsed

    path = reconstruct_path(parents, found_state)
    b = generated_count / visited_count if visited_count else 0.0
    return path, visited_count, generated_count, b, elapsed

# ==========================
# Обратный жадный поиск (оставляем)
# ==========================
def greedy_backward():
    start_time = time.perf_counter()
    heap = []
    counter = 0
    heapq.heappush(heap, (heuristic(GOAL_STATE), counter, GOAL_STATE))
    parents = {GOAL_STATE: None}
    in_open = {GOAL_STATE}
    visited_count = 0
    generated_count = 0
    found_state = None
    while heap:
        h, _, state = heapq.heappop(heap)
        if state not in in_open:
            continue
        in_open.remove(state)
        visited_count += 1
        if state == START_STATE:
            found_state = state
            break
        for prev_state, _ in predecessors_backward(state):
            generated_count += 1
            if prev_state not in parents:
                parents[prev_state] = state
                counter += 1
                heapq.heappush(heap, (heuristic(prev_state), counter, prev_state))
                in_open.add(prev_state)
    elapsed = time.perf_counter() - start_time
    if found_state is None:
        return None, visited_count, generated_count, 0.0, elapsed
    path = reconstruct_path(parents, START_STATE)
    b = generated_count / visited_count if visited_count else 0.0
    return path, visited_count, generated_count, b, elapsed

# ==========================
# Двунаправленный BFS
# ==========================
def bidirectional_bfs():
    start_time = time.perf_counter()
    if START_STATE == GOAL_STATE:
        return [START_STATE], 0, 0, 0.0, 0.0

    q_start = deque([START_STATE])
    q_goal = deque([GOAL_STATE])
    parents_start = {START_STATE: None}
    parents_goal = {GOAL_STATE: None}
    visited_from_start = {START_STATE}
    visited_from_goal = {GOAL_STATE}
    visited_count = 0
    generated_count = 0
    meeting_state = None

    while q_start and q_goal and meeting_state is None:
        for _ in range(len(q_start)):
            state = q_start.popleft()
            visited_count += 1
            for new_state, _ in successors_forward(state):
                generated_count += 1
                if new_state not in visited_from_start:
                    visited_from_start.add(new_state)
                    parents_start[new_state] = state
                    q_start.append(new_state)
                    if new_state in visited_from_goal:
                        meeting_state = new_state
                        break
            if meeting_state:
                break
        if meeting_state:
            break
        for _ in range(len(q_goal)):
            state = q_goal.popleft()
            visited_count += 1
            for prev_state, _ in predecessors_backward(state):
                generated_count += 1
                if prev_state not in visited_from_goal:
                    visited_from_goal.add(prev_state)
                    parents_goal[prev_state] = state
                    q_goal.append(prev_state)
                    if prev_state in visited_from_start:
                        meeting_state = prev_state
                        break
            if meeting_state:
                break

    elapsed = time.perf_counter() - start_time
    if meeting_state is None:
        return None, visited_count, generated_count, 0.0, elapsed

    path1 = []
    s = meeting_state
    while s is not None:
        path1.append(s)
        s = parents_start.get(s)
    path1.reverse()

    path2 = []
    s = parents_goal.get(meeting_state)
    while s is not None:
        path2.append(s)
        s = parents_goal.get(s)

    full_path = path1 + path2
    b = generated_count / visited_count if visited_count else 0.0
    return full_path, visited_count, generated_count, b, elapsed

# ==========================
# Запуск всех алгоритмов
# ==========================
def run_all():
    print("Стартовое состояние:", START_STATE)
    print("Целевое состояние:", GOAL_STATE)
    print()

    print("Прямой поиск (BFS)")
    path, visited, generated, b, t = bfs_forward()
    print("Путь:", path)
    print("Длина решения:", len(path) - 1 if path else None)
    print("Посещённых вершин:", visited)
    print("Сгенерировано состояний:", generated)
    print("Коэффициент разветвления:", round(b, 2))
    print("Время:", f"{t:.6f} c")
    print()

    print("A* поиск")
    path, visited, generated, b, t = astar_forward()
    print("Путь:", path)
    print("Длина решения:", len(path) - 1 if path else None)
    print("Посещённых вершин:", visited)
    print("Сгенерировано состояний:", generated)
    print("Коэффициент разветвления:", round(b, 2))
    print("Время:", f"{t:.6f} c")
    print()

    print("Обратный жадный поиск с эвристикой")
    path, visited, generated, b, t = greedy_backward()
    print("Путь:", path)
    print("Длина решения:", len(path) - 1 if path else None)
    print("Посещённых вершин:", visited)
    print("Сгенерировано состояний:", generated)
    print("Коэффициент разветвления:", round(b, 2))
    print("Время:", f"{t:.6f} c")
    print()

    print("Двунаправленный поиск (BFS)")
    path, visited, generated, b, t = bidirectional_bfs()
    print("Путь:", path)
    print("Длина решения:", len(path) - 1 if path else None)
    print("Посещённых вершин:", visited)
    print("Сгенерировано состояний:", generated)
    print("Коэффициент разветвления:", round(b, 2))
    print("Время:", f"{t:.6f} c")

if __name__ == "__main__":
    run_all()
