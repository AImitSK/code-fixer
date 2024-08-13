from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("openai_key"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form["code"]
        error = request.form["error"]

        # Korrigierten Code ohne Erklärungen anfordern
        fix_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Fix this code without any explanation or additional text:\n\n{code}\n\nError:\n\n{error}"}
            ]
        )
        fixed_code = fix_response.choices[0].message.content.strip()

        # Fehlererklärung auf Deutsch anfordern
        explanation_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
                {"role": "user", "content": f"Erkläre den Fehler in diesem Code auf Deutsch, ohne ihn zu beheben:\n\n{code}\n\nFehler:\n\n{error}"}
            ]
        )
        explanation = explanation_response.choices[0].message.content.strip()

        return render_template("index.html", explanation=explanation, fixed_code=fixed_code)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
