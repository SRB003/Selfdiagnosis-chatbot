from flask import Flask, request, jsonify
import re

app = Flask(__name__)

symptoms_dict = {
    "fever": "flu",
    "cough": "cold",
    "headache": "migraine",
    "stomach ache": "food poisoning",
    "rash": "allergies",
    "chest pain": "heart attack",
    "shortness of breath": "asthma",
}

remedies_dict = {
    "flu": "Get plenty of rest and fluids. Over-the-counter medications like acetaminophen or ibuprofen can help relieve symptoms.",
    "cold": "Drink plenty of fluids and get lots of rest. Over-the-counter medications like decongestants or pain relievers can help relieve symptoms.",
    "migraine": "Lie down in a dark, quiet room and apply a cold compress to your forehead. Over-the-counter medications like ibuprofen or aspirin can help relieve symptoms.",
    "food poisoning": "Drink plenty of fluids to prevent dehydration. Avoid solid foods until the vomiting and diarrhea have subsided. Contact a doctor if your symptoms are severe or don't improve after a few days.",
    "allergies": "Avoid triggers that cause your allergies. Over-the-counter medications like antihistamines or nasal sprays can help relieve symptoms.",
    "heart attack": "Call 911 or go to the emergency room immediately. Do not attempt to treat a heart attack at home.",
    "asthma": "Use a rescue inhaler as directed. Avoid triggers that cause your asthma. Contact a doctor if your symptoms are severe or don't improve with treatment.",
}


def check_severity(symptoms):
    severity = "mild"
    for symptom in symptoms:
        disease = symptoms_dict.get(symptom.lower())
        if disease and disease != "allergies":
            severity = "severe"
            break
    return severity


@app.route('/', methods=['POST'])
def get_response():

    data = request.json
    user_input = data['user_input']
    tokens = re.findall(r'\w+', user_input.lower())

    symptoms = [token for token in tokens if token in symptoms_dict.keys()]

    severity = check_severity(symptoms)

    if severity == "severe":
        response = "It sounds like your condition is severe. You should seek medical attention as soon as possible."

    elif severity == "mild":
        disease = None
        for token in tokens:
            if token in remedies_dict.keys():
                disease = token
                break

        if disease:
            response = f"Based on your symptoms, it seems like you have {disease}. Here is a home remedy you can try: {remedies_dict[disease]}"
        else:
            response = "I'm sorry, I'm not sure what condition you have. Can you please provide more information?"

    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
