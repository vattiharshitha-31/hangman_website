from flask import Flask, render_template, request
import random

app = Flask(__name__)

words = [
    "venkateswarlu",
    "dhanalakshmi",
    "harshitha",
    "dhanush",
    "subbareddy",
    "narasa",
    "vatti",
    "biryani",
    "chicken",
    "pakodi"
]

word = random.choice(words)
guessed_letters = set()
wrong_guesses = 0
max_wrong = 6


@app.route("/", methods=["GET", "POST"])
def home():
    global word, guessed_letters, wrong_guesses

    # New Game
    if request.method == "GET":
        word = random.choice(words)
        guessed_letters = set()
        wrong_guesses = 0

    # Letter guess
    if request.method == "POST":
        letter = request.form.get("letter", "").lower()

        if letter and letter not in guessed_letters:
            guessed_letters.add(letter)

            if letter not in word:
                wrong_guesses += 1

    display_word = ""

    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    message = ""

    if all(letter in guessed_letters for letter in word):
        message = "🎉 You Won! The word was " + word

    elif wrong_guesses >= max_wrong:
        message = "😮 Game Over! The word was " + word

    return render_template(
        "index.html",
        display_word=display_word,
        guessed_letters=guessed_letters,
        wrong_guesses=wrong_guesses,
        max_wrong=max_wrong,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
