from flask import Flask, render_template, request
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import json
import re
import requests

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def index():
    return render_template("v2/index.html")


@app.route("/questionnaire/<device>")
def questionnaire(device):
    return render_template("questionnaire.html", device=device)


@app.route("/analyze", methods=["POST"])
def analyze():

    data=request.form.to_dict()

    return render_template("v2/ai_loading.html",data=data)

@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.form.to_dict()

    device_type = data.get("device")

    # ---------------- PHONE PROMPT ----------------

    if device_type == "phone":

        prompt = f"""
        A user in India wants to buy a smartphone.

        User profile:

        Budget: {data.get("budget")}
        Operating System: {data.get("os")}
        Primary usage: {data.get("usage")}
        Performance priority: {data.get("performance")}
        Display preference: {data.get("display")}
        Charging preference: {data.get("charging")}
        Battery importance: {data.get("battery")}
        Camera importance: {data.get("camera")}
        Preferred brands: {data.get("brand")}

        Important rules:

        - Only recommend phones that match the OS preference.
        - Respect preferred brands if provided.
        - Stay within the budget.
        - Focus on the user's priorities.

        Recommend the TOP 3 smartphones currently available in India.

        Return ONLY JSON:

        [
        {{
        "name": "",
        "price": "",
        "reason": "",
        "specs": {{
        "processor": "",
        "display": "",
        "battery": "",
        "ram": "",
        "storage": ""
        }}
        }}
        ]
        """

    # ---------------- LAPTOP PROMPT ----------------

    elif device_type == "laptop":

        prompt = f"""
        A user in India wants to buy a laptop.

        User profile:

        Budget: {data.get("budget")}
        Primary usage: {data.get("usage")}
        Performance priority: {data.get("performance")}
        GPU requirement: {data.get("gpu")}
        RAM requirement: {data.get("ram")}
        Storage requirement: {data.get("storage")}
        Display preference: {data.get("display")}
        Screen size: {data.get("screen")}
        Battery importance: {data.get("battery")}
        Build quality preference: {data.get("build")}
        Operating system: {data.get("os")}

        Recommend the TOP 3 laptops available in India.

        Return ONLY JSON:

        [
        {{
        "name": "",
        "price": "",
        "reason": "",
        "specs": {{
        "processor": "",
        "display": "",
        "battery": "",
        "ram": "",
        "storage": ""
        }}
        }}
        ]
        """

    # ---------------- PC BUILD PROMPT ----------------

    elif device_type == "pc":

        budget_range = data.get("budget")

        if "+" in budget_range:
            max_budget = int(budget_range.replace("+",""))
        else:
            max_budget = int(budget_range.split("-")[1])

        prompt = f"""
        A user wants to build a custom PC in India.

        User Requirements:

        Maximum Budget: ₹{max_budget}

        Usage: {data.get("usage")}
        Gaming Resolution: {data.get("resolution")}
        CPU Priority: {data.get("cpu_priority")}
        GPU Priority: {data.get("gpu_priority")}
        RAM Requirement: {data.get("ram")}
        Storage Requirement: {data.get("storage")}
        Cooling Preference: {data.get("cooling")}
        Case Size: {data.get("case")}
        Upgrade Preference: {data.get("upgrade")}

        STRICT RULES:

        1. The TOTAL cost of each build MUST be LESS THAN OR EQUAL to ₹{max_budget}
        2. Do NOT exceed the budget under any circumstances
        3. Use realistic Indian market prices
        4. Balance CPU and GPU to avoid bottlenecks
        5. Both builds must have similar performance

        Return ONLY valid JSON.

        Format:

        {{
        "builds":[
        {{
        "name":"Primary Build",
        "cpu":{{"name":"","price":""}},
        "gpu":{{"name":"","price":""}},
        "motherboard":{{"name":"","price":""}},
        "ram":{{"name":"","price":""}},
        "storage":{{"name":"","price":""}},
        "psu":{{"name":"","price":""}},
        "case":{{"name":"","price":""}},
        "cooler":{{"name":"","price":""}}
        }},
        {{
        "name":"Alternate Build",
        "cpu":{{"name":"","price":""}},
        "gpu":{{"name":"","price":""}},
        "motherboard":{{"name":"","price":""}},
        "ram":{{"name":"","price":""}},
        "storage":{{"name":"","price":""}},
        "psu":{{"name":"","price":""}},
        "case":{{"name":"","price":""}},
        "cooler":{{"name":"","price":""}}
        }}
        ]
        }}
        """

    elif device_type == "tablet":

        prompt = f"""
        A user in India wants to buy a tablet.

        User profile:

        Budget: {data.get("budget")}
        Primary usage: {data.get("usage")}
        Screen size: {data.get("screen")}
        Performance requirement: {data.get("performance")}
        Battery importance: {data.get("battery")}
        Operating system: {data.get("os")}

        Recommend the TOP 3 tablets available in India.

        Return ONLY JSON:

        [
        {{
        "name": "",
        "price": "",
        "reason": "",
        "specs": {{
        "processor": "",
        "display": "",
        "battery": "",
        "ram": "",
        "storage": ""
        }}
        }}
        ]
        """

    else:
        return "Invalid device type", 400

    try:

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )


        ai_text = response.output_text

        print("AI RAW RESPONSE:")
        print(ai_text)

        # Extract JSON
        json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)

        if device_type == "pc":

            pc_data = json.loads(json_match.group())
            builds = pc_data.get("builds", [])

            return render_template("v2/pc_result.html", builds=builds)

        else:

            json_match = re.search(r'\[.*\]', ai_text, re.DOTALL)

            if json_match:
                devices = json.loads(json_match.group())
                for device in devices:

                    device["image"] = fetch_device_image(device_type)

            else:
                devices = []

            return render_template("result.html", devices=devices)

    except Exception as e:

        print("AI ERROR:", e)

        if device_type == "pc":
            return render_template("v2/pc_result.html", build={})

        return render_template("result.html", devices=[])

@app.route("/phone")
def phone():
    return render_template("v2/phone.html")

@app.route("/laptop")
def laptop_entry():
    return render_template("v2/laptop_entry.html")

@app.route("/tablet")
def tablet():
    return render_template("v2/tablet.html")

@app.route("/laptop-buy")
def laptop_buy():
    return render_template("v2/laptop_buy.html")


@app.route("/pc-build")
def pc_build():
    return render_template("v2/pc_build.html")

def fetch_device_image(device_type):

    images = {
        "phone": "/static/v2/images/phone.png",
        "laptop": "/static/v2/images/laptop.png",
        "tablet": "/static/v2/images/tablet.png",
        "pc": "/static/v2/images/pc.png"
    }

    return images.get(device_type, "/static/v2/images/phone.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


