let testAnswers = {}
let testInfo = document.getElementById('test-info')
let questionList = document.getElementById('question_list').innerHTML;
let questionsArray = JSON.parse("[" + questionList + "]");
let questionContainer = document.getElementById('test');

function startTest(e) {
  console.log('test begun')
  startBtn.style.display = 'none';
  testInfo.style.display = 'none';
  e.preventDefault();
  builtTest();
}


function AnswerVal(question, answer) {
    testAnswers[question] = answer
}

function builtTest() {
    const output = []

    questionsArray[0].forEach((currentQuestion, questionId) => {
        let answers = []


        for (let answer in currentQuestion.answers) {
          answers.push(
            `<input type="submit" class='btn btn-test btn-danger btn-small-text'
              value='${answer}' onclick="AnswerVal(${questionId}, ${answer})">`
          )
        }

        output.push(
            `<div class="question">${currentQuestion.question}</div>
             <div class="answers">
                <div class="btn-group">
                    ${answers.join('')}
                </div>
            </div>`
        )
    })
    questionContainer.innerHTML = output.join('')
}

function results() {

}

let startBtn = document.getElementById('start-test-btn')
startBtn.addEventListener('click', startTest)