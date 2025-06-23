// 🌗 DARK MODE TOGGLE
const themeToggle = document.getElementById("themeSwitch");

if (themeToggle) {
  const isDark = localStorage.getItem("darkMode") === "true";
  document.body.classList.toggle("dark", isDark);
  themeToggle.checked = isDark;

  themeToggle.addEventListener("change", () => {
    const darkModeEnabled = themeToggle.checked;
    document.body.classList.toggle("dark", darkModeEnabled);
    localStorage.setItem("darkMode", darkModeEnabled);
  });
}

// 🧠 FLASHCARD LEARN MODE
let currentIndex = 0;
let correctCount = 0;
let incorrectCount = 0;

const flashcards = window.learnCards || [];  // Expect cards to be passed from Jinja
const learnCard = document.getElementById("learnCard");
const questionText = document.getElementById("questionText");
const answerText = document.getElementById("answerText");
const progress = document.getElementById("progress");

function flipCard() {
  if (learnCard) {
    learnCard.classList.toggle("flipped");
  }
}

function updateCard() {
  if (!flashcards.length) return;
  const card = flashcards[currentIndex];
  questionText.textContent = card.question;
  answerText.textContent = card.answer;
  progress.textContent = `Card ${currentIndex + 1} of ${flashcards.length}`;
  learnCard.classList.remove("flipped");
}

function markCorrect() {
  correctCount++;
  nextCard();
}

function markWrong() {
  incorrectCount++;
  nextCard();
}

function nextCard() {
  currentIndex++;
  if (currentIndex >= flashcards.length) {
    alert(`Session Complete!\n✔️ Correct: ${correctCount}\n❌ Incorrect: ${incorrectCount}`);
    currentIndex = 0;
    correctCount = 0;
    incorrectCount = 0;
  }
  updateCard();
}

document.addEventListener("DOMContentLoaded", () => {
  if (flashcards.length) {
    updateCard();
  }
});
