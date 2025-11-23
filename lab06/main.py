import random
import math
import matplotlib.pyplot as plt

# ----- параметры -----
L = 4                  
MAX_INT = 2**L - 1

# Целевая функция (сюда вписать ваш вариант) — пример
# f(x) = x * sin(10*pi*x) + 1
import math
def f(x):
    return x * math.sin(10 * math.pi * x) + 1

# Кодирование и декодирование (4 бита → число 0..15 → x=[0,1])
def decode(ch):
    return int(ch, 2) / MAX_INT

# Генерация начальной популяции
def init_pop(N):
    return [format(random.randint(0, MAX_INT), '04b') for _ in range(N)]

# Оценка приспособленности
def evaluate(pop):
    return [f(decode(ch)) for ch in pop]

# Селекция рулеткой
def select_roulette(pop, fit):
    total = sum(fit)
    if total == 0:
        return random.choice(pop)
    r = random.uniform(0, total)
    s = 0
    for ch, fv in zip(pop, fit):
        s += fv
        if s >= r:
            return ch
    return pop[-1]

# Кроссовер одноточечный
def crossover(p1, p2, pc):
    if random.random() < pc:
        point = random.randint(1, L - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:], point
    return p1, p2, None

# Мутация
def mutate(ch, pm):
    ch_list = list(ch)
    mutated = []
    for i in range(len(ch_list)):
        if random.random() < pm:
            ch_list[i] = '1' if ch_list[i] == '0' else '0'
            mutated.append(i+1)
    return ''.join(ch_list), mutated

# ---- основной ГА ----
def GA(N=6, pc=0.8, pm=0.05, G=30):
    pop = init_pop(N)
    best_hist = []

    for g in range(1, G+1):
        print(f"\n=== Поколение {g} ===")

        fit = evaluate(pop)
        best = max(fit)
        avg = sum(fit)/len(fit)
        print(f"Популяция:")
        for i, (ch, fv) in enumerate(zip(pop, fit), 1):
            print(f"  {i}. {ch}  x={decode(ch):.3f}  f={fv:.6f}")

        print(f"max={best:.6f}, avg={avg:.6f}")
        best_hist.append(best)

        # --- селекция ---
        parents = [select_roulette(pop, fit) for _ in range(N)]
        print("Родители:", parents)

        # --- кроссовер ---
        new_pop = []
        print("Кроссовер:")
        for i in range(0, N, 2):
            p1 = parents[i]
            p2 = parents[i+1 if i+1 < N else 0]
            c1, c2, point = crossover(p1, p2, pc)
            if point:
                print(f"  {p1} × {p2} -> точка {point}")
            else:
                print(f"  {p1} × {p2} -> без кроссовера")
            new_pop += [c1, c2]

        # --- мутация ---
        print("Мутации:")
        for i in range(N):
            new, muts = mutate(new_pop[i], pm)
            if muts:
                print(f"  особь {i+1}, биты {muts}: {new_pop[i]} → {new}")
            new_pop[i] = new

        pop = new_pop

    # график
    plt.plot(best_hist)
    plt.title("Изменение максимального fitness")
    plt.xlabel("Поколение")
    plt.ylabel("max fitness")
    plt.grid(True)
    plt.show()

    print("\nИТОГ")
    final_fit = evaluate(pop)
    best_f = max(final_fit)
    ix = final_fit.index(best_f)
    ch = pop[ix]
    print(f"Лучшее решение: {ch} → x={decode(ch):.4f}, f={best_f:.6f}")

# ---- Пример запуска ----
GA(N=12, pc=0.8, pm=0.05, G=50)
