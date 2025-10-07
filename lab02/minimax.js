// ПАРАМЕТРЫ ДЕРЕВА 
const depth = 5;
const width = 3;

// ГЕНЕРАЦИЯ ДЕРЕВА 
// Каждый лист (глубина = 0) — это просто случайное число (оценка позиции).
function generateLeaves(depth, width) {
    if (depth === 0) 
        return Math.floor(Math.random() * 200 - 100);

    // если это не лист, создаём массив потомков (детей)
    const children = [];
    for (let i = 0; i < width; i++) 
        children.push(generateLeaves(depth - 1, width));
    return children;
}

// создаём игровое дерево
const gameTree = generateLeaves(depth, width);

// ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ 

// превращает всё дерево в один массив только из чисел-листьев
function flattenLeaves(node) {
    if (typeof node === 'number') return [node];
    return node.flatMap(flattenLeaves); // рекурсивно спускаемся вниз
}

// выбирает несколько случайных листьев, чтобы просто показать в консоли
function sampleLeaves(leaves, n = 10) {
    const sampled = [];
    const len = leaves.length;
    for (let i = 0; i < Math.min(n, len); i++) {
        const index = Math.floor(Math.random() * len);
        sampled.push(leaves[index]);
    }
    return sampled;
}

// ОБЫЧНЫЙ МИНИ-МАКС 
let normalNodes = 0;

// Мини-макс — рекурсивный алгоритм для принятия решений в играх.
// isMax показывает, чей сейчас ход: true → MAX (игрок), false → MIN (противник)
function minimax(node, isMax) {
    normalNodes++; // считаем, сколько раз вызывалась функция т е количество узлов

    // если лист — просто возвращаем его значение (оценка позиции)
    if (typeof node === 'number') return node;

    // если ход игрока (MAX)
    if (isMax) {
        let maxVal = -Infinity;
        for (let child of node) {
            // вычисляем значение для каждого потомка
            const val = minimax(child, false);
            maxVal = Math.max(maxVal, val);
        }
        return maxVal; 
    } 
    // если ход противника (MIN)
    else {
        let minVal = Infinity;
        for (let child of node) {
            const val = minimax(child, true);
            minVal = Math.min(minVal, val);
        }
        return minVal; 
    }
}

// МИНИ-МАКС С АЛЬФА-БЕТА ОТСЕЧЕНИЕМ

let abNodes = 0;

// alpha и beta — "границы отсечения" 
// alpha — лучшее (максимальное) значение для MAX, которое он уже нашёл
// beta  — лучшее (минимальное) значение для MIN
function minimaxAB(node, isMax, alpha = -Infinity, beta = Infinity) {
    abNodes++;

    // базовый случай — лист
    if (typeof node === 'number') return node;

    // если ход MAX
    if (isMax) {
        let maxVal = -Infinity;
        for (let child of node) {
            const val = minimaxAB(child, false, alpha, beta);
            maxVal = Math.max(maxVal, val);
            alpha = Math.max(alpha, maxVal);

            // если beta <= alpha, то дальнейшие узлы бессмысленно проверять
            // (оппонент уже выберет более выгодный вариант)
            if (beta <= alpha) break; // отсечение ветви
        }
        return maxVal;
    } 
    // если ход MIN
    else {
        let minVal = Infinity;
        for (let child of node) {
            const val = minimaxAB(child, true, alpha, beta);
            minVal = Math.min(minVal, val);
            beta = Math.min(beta, minVal);

            if (beta <= alpha) break; // отсечение
        }
        return minVal;
    }
}

// ЗАПУСК И СРАВНЕНИЕ

// функция для точного времени вывода времени в микросекундах
function formatTime(ms) {
    return (ms * 1000).toFixed(2) + ' µs'; 
}

// запускаем обычный минимакс
const t0 = performance.now();
const normalResult = minimax(gameTree, true);
const t1 = performance.now();

// запускаем минимакс с альфа-бета отсечением
const t2 = performance.now();
const abResult = minimaxAB(gameTree, true);
const t3 = performance.now();

// получаем все листья и выбираем несколько для примера
const allLeaves = flattenLeaves(gameTree);
const sample = sampleLeaves(allLeaves, 10);

// ВЫВОД РЕЗУЛЬТАТОВ
console.log("Некоторые из листьев:", sample.join(", "));

console.log("\nОбычный минимакс:");
console.log("  Результат:", normalResult);
console.log("  Узлов проверено:", normalNodes);
console.log("  Время выполнения:", formatTime(t1 - t0));

console.log("\nМини-макс с альфа-бета отсечением:");
console.log("  Результат:", abResult);
console.log("  Узлов проверено:", abNodes);
console.log("  Время выполнения:", formatTime(t3 - t2));
