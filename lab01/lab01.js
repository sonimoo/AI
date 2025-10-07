// СОСТОЯНИЯ АВТОМАТА 
const State = {
  Q0: 'Q0', // старт, ждем 'a' первой пары
  Q1: 'Q1', // после 'a', ждем 'b'
  Q2: 'Q2', // после хотя бы одного "ab", принимающее состояние
  Q3: 'Q3', // после 'c' в части cd
  Q4: 'Q4', // после хотя бы одного "cd", принимающее состояние
  REJECT: 'REJECT'
};

// ФУНКЦИЯ ПРОВЕРКИ СЛОВА 
function checkWord(word) {
  let state = State.Q0;

  for (const ch of word) {
    switch (state) {
      case State.Q0:
        if (ch === 'a') state = State.Q1;
        else state = State.REJECT;
        break;

      case State.Q1:
        if (ch === 'b') state = State.Q2;
        else state = State.REJECT;
        break;

      case State.Q2: // после хотя бы одного "ab"
        if (ch === 'a') state = State.Q1;     // начинаем ещё один "ab"
        else if (ch === 'c') state = State.Q3; // переходим в часть (cd)*
        else state = State.REJECT;
        break;

      case State.Q3: 
        if (ch === 'd') state = State.Q4;
        else state = State.REJECT;
        break;

      case State.Q4: // после хотя бы одного "cd"
        if (ch === 'c') state = State.Q3; // продолжаем (cd)*
        else state = State.REJECT;
        break;

      default:
        state = State.REJECT;
        break;
    }

    if (state === State.REJECT) return false;
  }

  // Принимающие состояния: Q2 или Q4
  return state === State.Q2 || state === State.Q4;
}

// ТЕСТЫ 
const tests = [
  "ab", "abab", "abcd", "ababcdcd", "abcdcd", "ababcd",
  "cd", "a", "abb", "abcdab", "", "ababc", 
];

for (const t of tests) {
  console.log(`"${t}" -> ${checkWord(t)}`);
}
