import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ====== 1. ТРЕУГОЛЬНЫЕ ФУНКЦИИ ПРИНАДЛЕЖНОСТИ ======
def trimf(x, a, b, c):
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0)

# --- Температура (°C)
def temp_low(x): return trimf(x, -10, 0, 10)
def temp_med(x): return trimf(x, 5, 15, 25)
def temp_high(x): return trimf(x, 20, 30, 40)

# --- UV (индекс 0–11)
def uv_low(x): return trimf(x, 0, 1, 3)
def uv_mod(x): return trimf(x, 2, 5, 7)
def uv_high(x): return trimf(x, 6, 8, 10)
def uv_ext(x): return trimf(x, 9, 11, 12)

# --- Влажность (%)
def hum_low(x): return trimf(x, 0, 30, 60)
def hum_high(x): return trimf(x, 40, 70, 100)

# ====== 2. БАЗА ПРАВИЛ ======
rules = [
    ("низкая","низкий","низкая","низкий"),
    ("низкая","низкий","высокая","низкий"),
    ("низкая","умеренный","низкая","средний"),
    ("низкая","умеренный","высокая","низкий"),
    ("низкая","высокий","низкая","высокий"),
    ("низкая","высокий","высокая","средний"),
    ("низкая","экстремальный","низкая","высокий"),
    ("низкая","экстремальный","высокая","высокий"),
    ("средняя","низкий","низкая","низкий"),
    ("средняя","низкий","высокая","низкий"),
    ("средняя","умеренный","низкая","средний"),
    ("средняя","умеренный","высокая","средний"),
    ("средняя","высокий","низкая","высокий"),
    ("средняя","высокий","высокая","высокий"),
    ("средняя","экстремальный","низкая","высокий"),
    ("средняя","экстремальный","высокая","высокий"),
    ("высокая","низкий","низкая","низкий"),
    ("высокая","низкий","высокая","низкий"),
    ("высокая","умеренный","низкая","средний"),
    ("высокая","умеренный","высокая","средний"),
    ("высокая","высокий","низкая","высокий"),
    ("высокая","высокий","высокая","высокий"),
    ("высокая","экстремальный","низкая","высокий"),
    ("высокая","экстремальный","высокая","высокий"),
]

risk_levels = {"низкий": 20, "средний": 50, "высокий": 80}

# ====== 3. ФАЗЗИФИКАЦИЯ ======
def fuzzify(temp, uv, hum):
    μ_temp = {"низкая": temp_low(temp), "средняя": temp_med(temp), "высокая": temp_high(temp)}
    μ_uv = {"низкий": uv_low(uv), "умеренный": uv_mod(uv), "высокий": uv_high(uv), "экстремальный": uv_ext(uv)}
    μ_hum = {"низкая": hum_low(hum), "высокая": hum_high(hum)}
    return μ_temp, μ_uv, μ_hum

# ====== 4. ПРИМЕНЕНИЕ ПРАВИЛ ======
def apply_rules(μ_temp, μ_uv, μ_hum):
    result = {"низкий": 0, "средний": 0, "высокий": 0}
    for t, u, h, r in rules:
        α = min(μ_temp[t], μ_uv[u], μ_hum[h])
        result[r] = max(result[r], α)
    return result

# ====== 5. ДЕФАЗЗИФИКАЦИЯ ======
def defuzzify(risks):
    num = sum(risks[k] * risk_levels[k] for k in risks)
    den = sum(risks.values())
    return num / den if den != 0 else 0

# ====== 6. ЛОГИКА ПРОГРАММЫ ======
st.title("Прогноз риска солнечного ожога")
st.write("Введите значения для температуры, UV-индекса и влажности:")

temp = st.slider("Температура (°C)", -10, 40, 15)
uv = st.slider("UV-индекс", 0, 11, 5)
hum = st.slider("Влажность (%)", 0, 100, 50)

if st.button("Рассчитать риск"):
    μ_temp, μ_uv, μ_hum = fuzzify(temp, uv, hum)
    fuzzy_out = apply_rules(μ_temp, μ_uv, μ_hum)
    crisp = defuzzify(fuzzy_out)

    # Интерпретация
    if crisp < 30:
        msg = "Риск низкий — ожог маловероятен."
    elif crisp < 65:
        msg = "Риск средний — рекомендуется солнцезащитный крем."
    else:
        msg = "Риск высокий — избегайте прямого солнца!"

    st.subheader("Результат:")
    st.write(f"**Числовое значение риска:** {crisp}%")
    st.write(msg)

    st.write("Степени принадлежности:")
    st.json({
        "Температура": μ_temp,
        "UV": μ_uv,
        "Влажность": μ_hum,
    })

    # ====== ГРАФИКИ ======
    st.subheader("Функции принадлежности")

    fig, axs = plt.subplots(1, 3, figsize=(15, 4))

    # Температура
    x = np.linspace(-10, 40, 200)
    axs[0].plot(x, [temp_low(i) for i in x], label="низкая")
    axs[0].plot(x, [temp_med(i) for i in x], label="средняя")
    axs[0].plot(x, [temp_high(i) for i in x], label="высокая")
    axs[0].axvline(temp, color='r', linestyle='--')
    axs[0].set_title("Температура (°C)")
    axs[0].legend()

    # UV
    x = np.linspace(0, 11, 200)
    axs[1].plot(x, [uv_low(i) for i in x], label="низкий")
    axs[1].plot(x, [uv_mod(i) for i in x], label="умеренный")
    axs[1].plot(x, [uv_high(i) for i in x], label="высокий")
    axs[1].plot(x, [uv_ext(i) for i in x], label="экстремальный")
    axs[1].axvline(uv, color='r', linestyle='--')
    axs[1].set_title("UV-индекс")
    axs[1].legend()

    # Влажность
    x = np.linspace(0, 100, 200)
    axs[2].plot(x, [hum_low(i) for i in x], label="низкая")
    axs[2].plot(x, [hum_high(i) for i in x], label="высокая")
    axs[2].axvline(hum, color='r', linestyle='--')
    axs[2].set_title("Влажность (%)")
    axs[2].legend()

    st.pyplot(fig)