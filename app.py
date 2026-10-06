from flask import Flask, render_template, request
import language_tool_python

app = Flask(__name__)

tool = language_tool_python.LanguageTool("en-US")


@app.route("/", methods=["GET", "POST"])
def home():
    original_text = ""
    corrected_text = ""
    errors = []

    if request.method == "POST":
        original_text = request.form.get("text", "").strip()

        if original_text:
            matches = tool.check(original_text)

            corrected_text = tool.correct(original_text)

            for match in matches:
                errors.append({
                    "message": match.message,
                    "wrong": original_text[
                        match.offset:match.offset + match.error_length
                    ],
                    "suggestion": (
                        match.replacements[0]
                        if match.replacements
                        else "No suggestion"
                    )
                })

    return render_template(
        "index.html",
        original_text=original_text,
        corrected_text=corrected_text,
        errors=errors
    )


if __name__ == "__main__":
    app.run(debug=True)