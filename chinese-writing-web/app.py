from flask import Flask, render_template, request

app = Flask(__name__)

dictionary = {}


# Convert numbered pinyin (ni3 hao3) → tone marks (nǐ hǎo)
def convert_pinyin(pinyin):

    tone_map = {
        'a': ['ā','á','ǎ','à'],
        'e': ['ē','é','ě','è'],
        'i': ['ī','í','ǐ','ì'],
        'o': ['ō','ó','ǒ','ò'],
        'u': ['ū','ú','ǔ','ù'],
        'v': ['ǖ','ǘ','ǚ','ǜ']
    }

    for i in range(1,5):

        if str(i) in pinyin:

            tone = i - 1
            pinyin = pinyin.replace(str(i), '')

            for v in "aeiouv":

                if v in pinyin:
                    pinyin = pinyin.replace(v, tone_map[v][tone], 1)
                    return pinyin

    return pinyin


# Load CEDICT dictionary
with open("data/cedict.txt", encoding="utf-8") as f:

    for line in f:

        if line.startswith("#"):
            continue

        parts = line.split(" ")

        if len(parts) > 2:

            char = parts[1]

            try:

                pinyin = line.split("[")[1].split("]")[0]

                meanings = line.split("/")[1:-1]
                meaning = ", ".join(meanings)

                dictionary[char] = {
                    "pinyin": convert_pinyin(pinyin),
                    "meaning": meaning
                }

            except:
                continue


@app.route("/", methods=["GET", "POST"])
def index():

    character = ""
    pinyin = ""
    meaning = ""

    if request.method == "POST":

        character = request.form["character"]

        if character in dictionary:

            pinyin = dictionary[character]["pinyin"]
            meaning = dictionary[character]["meaning"]

    return render_template(
        "index.html",
        character=character,
        pinyin=pinyin,
        meaning=meaning
    )


# Only run locally (Render uses gunicorn)
if __name__ == "__main__":
    app.run(debug=True)