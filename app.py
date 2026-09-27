from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)

app.secret_key = "my-hangman-secret-key"


# ================= CATEGORIES =================

categories = {
    "food": [
        "biryani", "chicken", "pakodi", "pizza",
        "burger", "dosa", "idli", "noodles"
    ],

    "animals": [
        "elephant", "tiger", "lion", "rabbit",
        "monkey", "giraffe", "zebra", "kangaroo"
    ],

    "programming": [
        "python", "javascript", "flask", "developer",
        "programming", "variable", "function", "database"
    ],

    "countries": [
        "india", "japan", "canada", "brazil",
        "australia", "germany", "france", "italy"
    ]
}


# ================= CATEGORY NAMES =================

category_names = {
    "food": "🍔 Food",
    "animals": "🐱 Animals",
    "programming": "💻 Programming",
    "countries": "🌍 Countries"
}


# ================= HINTS =================

hints = {
    "biryani": "A popular rice dish with spices and meat.",
    "chicken": "A common type of poultry.",
    "pakodi": "A crispy Indian snack made by deep frying.",
    "pizza": "An Italian dish with a flat base and toppings.",
    "burger": "A popular fast food with a bun and filling.",
    "dosa": "A thin South Indian dish made from fermented batter.",
    "idli": "A soft steamed South Indian breakfast.",
    "noodles": "Long thin strands of food usually boiled or stir-fried.",

    "elephant": "The largest land animal.",
    "tiger": "A large striped wild cat.",
    "lion": "Known as the king of the jungle.",
    "rabbit": "A small animal with long ears.",
    "monkey": "An animal that can climb trees easily.",
    "giraffe": "The tallest land animal.",
    "zebra": "An animal known for its black and white stripes.",
    "kangaroo": "An Australian animal that moves by jumping.",

    "python": "A popular programming language named after a comedy group.",
    "javascript": "A programming language commonly used for web development.",
    "flask": "A lightweight Python web framework.",
    "developer": "A person who creates software.",
    "programming": "The process of writing instructions for computers.",
    "variable": "A named place used to store data.",
    "function": "A reusable block of code.",
    "database": "A structured collection of data.",

    "india": "A country in South Asia.",
    "japan": "An island country in East Asia.",
    "canada": "A country located north of the United States.",
    "brazil": "The largest country in South America.",
    "australia": "A country and continent known for kangaroos.",
    "germany": "A country in Central Europe.",
    "france": "A European country famous for the Eiffel Tower.",
    "italy": "A European country shaped like a boot."
}


# ================= GAME SETTINGS =================

MAX_WRONG = 6
MAX_HINTS = 2

CORRECT_POINTS = 10
WRONG_PENALTY = 5
HINT_PENALTY = 10


# ================= START NEW GAME =================

def start_new_game(category):

    word = random.choice(categories[category])

    session["category"] = category
    session["word"] = word

    session["guessed_letters"] = []
    session["wrong_guesses"] = 0
    session["hints_used"] = 0
    session["score"] = 0


# ================= HOME ROUTE =================

@app.route("/", methods=["GET", "POST"])
def home():

    # ================= POST REQUEST =================

    if request.method == "POST":

        # ---------------- CATEGORY SELECTION ----------------

        category = request.form.get("category")

        if category in categories:

            start_new_game(category)

            return redirect(url_for("home"))


        # ---------------- HINT SYSTEM ----------------

        hint_request = request.form.get("hint")

        if hint_request == "use":

            if "word" in session:

                word = session["word"]

                guessed_letters = session.get(
                    "guessed_letters", []
                )

                hints_used = session.get(
                    "hints_used", 0
                )


                if hints_used < MAX_HINTS:

                    available_letters = [
                        letter
                        for letter in set(word)
                        if letter not in guessed_letters
                    ]


                    if available_letters:

                        hint_letter = random.choice(
                            available_letters
                        )

                        guessed_letters.append(
                            hint_letter
                        )

                        session["guessed_letters"] = (
                            guessed_letters
                        )

                        session["hints_used"] = (
                            hints_used + 1
                        )

                        session["score"] = (
                            session.get("score", 0)
                            - HINT_PENALTY
                        )


        # ---------------- LETTER GUESS ----------------

        letter = request.form.get(
            "letter", ""
        ).lower()


        if "word" in session and letter:

            guessed_letters = session.get(
                "guessed_letters", []
            )

            word = session["word"]


            if letter not in guessed_letters:

                guessed_letters.append(letter)

                session["guessed_letters"] = (
                    guessed_letters
                )


                # Correct guess

                if letter in word:

                    session["score"] = (
                        session.get("score", 0)
                        + CORRECT_POINTS
                    )


                # Wrong guess

                else:

                    session["wrong_guesses"] = (
                        session.get("wrong_guesses", 0)
                        + 1
                    )

                    session["score"] = (
                        session.get("score", 0)
                        - WRONG_PENALTY
                    )


    # ================= NO GAME STARTED =================

    if "word" not in session:

        return render_template(
            "index.html",

            categories=category_names,

            game_started=False,

            wrong_guesses=0,

            max_wrong=MAX_WRONG,

            guessed_letters=[],

            display_word="",

            message="",

            category="",

            game_over=False,

            won=False,

            hint="",

            hints_used=0,

            max_hints=MAX_HINTS,

            score=0,

            # Statistics

            games_played=session.get(
                "games_played", 0
            ),

            games_won=session.get(
                "games_won", 0
            ),

            games_lost=session.get(
                "games_lost", 0
            ),

            highest_score=session.get(
                "highest_score", 0
            )
        )


    # ================= GAME DATA =================

    word = session["word"]

    guessed_letters = session.get(
        "guessed_letters", []
    )

    wrong_guesses = session.get(
        "wrong_guesses", 0
    )

    category = session.get(
        "category", ""
    )

    hints_used = session.get(
        "hints_used", 0
    )

    score = session.get(
        "score", 0
    )


    # ================= DISPLAY WORD =================

    display_word = ""

    for letter in word:

        if letter in guessed_letters:

            display_word += letter + " "

        else:

            display_word += "_ "


    # ================= GAME STATUS =================

    message = ""

    game_over = False

    won = False


    # ================= WIN =================

    if all(
        letter in guessed_letters
        for letter in word
    ):

        message = (
            "🎉 You Won! The word was "
            + word
        )

        game_over = True

        won = True


        # Update statistics only once

        if not session.get(
            "current_game_recorded", False
        ):

            session["games_played"] = (
                session.get("games_played", 0)
                + 1
            )

            session["games_won"] = (
                session.get("games_won", 0)
                + 1
            )

            session["highest_score"] = max(
                session.get("highest_score", 0),
                score
            )

            session["current_game_recorded"] = True


    # ================= LOSS =================

    elif wrong_guesses >= MAX_WRONG:

        message = (
            "😮 Game Over! The word was "
            + word
        )

        game_over = True


        # Update statistics only once

        if not session.get(
            "current_game_recorded", False
        ):

            session["games_played"] = (
                session.get("games_played", 0)
                + 1
            )

            session["games_lost"] = (
                session.get("games_lost", 0)
                + 1
            )

            session["highest_score"] = max(
                session.get("highest_score", 0),
                score
            )

            session["current_game_recorded"] = True


    # ================= HINT =================

    current_hint = hints.get(
        word,
        "Try to guess the hidden word."
    )


    # ================= WIN RATE =================

    games_played = session.get(
        "games_played", 0
    )

    games_won = session.get(
        "games_won", 0
    )


    if games_played > 0:

        win_rate = round(
            (games_won / games_played) * 100,
            1
        )

    else:

        win_rate = 0


    # ================= RENDER =================

    return render_template(

        "index.html",

        display_word=display_word,

        guessed_letters=guessed_letters,

        wrong_guesses=wrong_guesses,

        max_wrong=MAX_WRONG,

        message=message,

        category=category_names.get(
            category, ""
        ),

        game_started=True,

        game_over=game_over,

        won=won,

        categories=category_names,

        hint=current_hint,

        hints_used=hints_used,

        max_hints=MAX_HINTS,

        score=score,

        # Statistics

        games_played=session.get(
            "games_played", 0
        ),

        games_won=session.get(
            "games_won", 0
        ),

        games_lost=session.get(
            "games_lost", 0
        ),

        highest_score=session.get(
            "highest_score", 0
        ),

        win_rate=win_rate
    )


# ================= NEW GAME =================

@app.route("/new-game")
def new_game():

    category = session.get("category")

    if category in categories:

        start_new_game(category)

        # Allow the new game to be recorded

        session["current_game_recorded"] = False

    else:

        session.clear()

    return redirect(url_for("home"))


# ================= CHANGE CATEGORY =================

@app.route("/change-category")
def change_category():

    # Keep statistics when changing category

    games_played = session.get(
        "games_played", 0
    )

    games_won = session.get(
        "games_won", 0
    )

    games_lost = session.get(
        "games_lost", 0
    )

    highest_score = session.get(
        "highest_score", 0
    )


    session.clear()


    # Restore statistics

    session["games_played"] = games_played
    session["games_won"] = games_won
    session["games_lost"] = games_lost
    session["highest_score"] = highest_score


    return redirect(url_for("home"))


# ================= RUN APP =================

if __name__ == "__main__":

    app.run(debug=True)