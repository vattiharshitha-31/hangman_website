# 🎯 Hangman Game

A web-based Hangman Game built using Python and Flask.

This project allows players to guess hidden words from different categories while tracking their score, hints, and game statistics.

## 🚀 Features

- 🎯 Classic Hangman gameplay
- 🍔 Multiple categories:
  - Food
  - Animals
  - Programming
  - Countries
- 💡 Hint system with limited hints
- ⭐ Score system
  - Correct letter: +10 points
  - Wrong letter: -5 points
  - Hint: -10 points
- 📊 Game statistics
  - Games Played
  - Games Won
  - Games Lost
  - Highest Score
  - Win Rate
- 🔄 New Game option
- 🔀 Change Category option
- 📱 Responsive design for different screen sizes

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- Jinja2 Templates
- Flask Session

## 🎮 How to Play

1. Select a category.
2. A random word will be selected.
3. Guess the hidden word one letter at a time.
4. Correct guesses reveal the letter.
5. Wrong guesses reduce the remaining chances.
6. You can use hints when needed.
7. Try to complete the word before all chances are used.

## 📊 Scoring System

| Action | Points |
|--------|--------|
| Correct Letter | +10 |
| Wrong Letter | -5 |
| Use Hint | -10 |

## 💡 Hint System

Players can use up to 2 hints during a game.

Each hint reveals one unrevealed letter and deducts 10 points from the score.

## 📈 Statistics

The game tracks statistics during the current session:

- Games Played
- Games Won
- Games Lost
- Highest Score
- Win Rate

## 💻 Run the Project Locally

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL