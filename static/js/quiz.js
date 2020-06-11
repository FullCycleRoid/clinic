function buildQuiz() {
  const output = [];

  psyQuestions.forEach(
    (currentQuestion, questionNumber) => {

      const answers = [];

      for (item in currentQuestion.answers) {
        answers.push(
          `<label>
            <input type='radio' name='question${questionNumber}' value='${item}'>
            ${item}:
            ${currentQuestion.answers[item]}
          </label>`
        );
      }
      output.push(
        `<div class="question">${currentQuestion.question}</div>
         <div class="answers">${answers.join('')}</div>`
      )
    }
  )
  quizContainer.innerHTML = output.join('');
}

function showResults() {
  let numCorrectAnswers = 0;

  const answersContainer = quizContainer.querySelectorAll('.answers');

  psyQuestions.forEach((currentQuestion, questionNumber) => {

    const answers = answersContainer[questionNumber];
    const selector = `input[name=question${questionNumber}]:checked`;
    const userAnswer = (answers.querySelector(selector) || {}).value;

    if (userAnswer === currentQuestion.correctAnswer) {
      numCorrectAnswers++;
      answersContainer[questionNumber].style.color = 'white'
    } else {
      answersContainer[questionNumber].style.color = 'red'
    }
  })

  let html = `<h1>${numCorrectAnswers} in out of ${psyQuestions.length} questions</h1>`
  resultContainer.innerHTML = html
}

const psyQuestions = [
  {
    question: "Вы испытываете тревожность?",
    answers: {
      a: "Да",
      b: "Нет",
      c: "Иногда"
    },
    correctAnswer: "c"
  },
  {
    question: "Вы думаете о суициде?",
    answers: {
      a: "Да",
      b: "Нет",
      c: "Иногда"
    },
    correctAnswer: "c"
  },
  {
    question: "Вы слышите голоса?",
    answers: {
      a: "Да",
      b: "Нет",
      c: "Иногда",
      d: "По воскресениям"
    },
    correctAnswer: "d"
  }
];


const quizContainer = document.getElementById('quiz');
const submitButton = document.getElementById('submit');
const resultContainer = document.getElementById('result');


buildQuiz();

submitButton.addEventListener('click', showResults);