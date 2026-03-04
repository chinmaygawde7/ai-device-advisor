from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/phone")
def phone():
    return render_template("phone.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    budget = request.form.get("budget")
    os_pref = request.form.get("os")
    camera = request.form.get("camera")
    gaming = request.form.get("gaming")
    battery = request.form.get("battery")

    prompt = f"""
    A user wants to buy a smartphone in India.

    Budget: {budget}
    Preferred OS: {os_pref}
    Camera Importance: {camera}
    Gaming Importance: {gaming}
    Battery Importance: {battery}

    Recommend the TOP 3 smartphones.

    For each phone include:
    - Name
    - Price
    - Key specs
    - Why it fits the user
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    result = response.output_text

    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)