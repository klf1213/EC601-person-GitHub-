from flask import Flask, request, jsonify
import openai
import json

# Set your OpenAI API key here
openai.api_key = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)


@app.route('/harmonize', methods=['POST'])
def harmonize():
    """
    Endpoint: /harmonize (POST)
    Expected JSON input:
    {
        "melody": "C4 D4 E4 G4 ...",  # melody notes or MIDI sequence
        "style": "classical"          # desired harmony style, e.g., 'classical', 'jazz', 'pop'
    }

    Example JSON response:
    {
        "chords": [
            {"beat": 1, "chord": "Cmaj7"},
            {"beat": 2, "chord": "Fmaj7"}
        ],
        "explanation": "Reasoning behind these chord choices..."
    }
    """
    data = request.get_json()
    melody = data.get('melody', '')
    style = data.get('style', 'classical')

    # Prompt for Chat GPT
    prompt = f"""
You are a professional harmony assistant. Given the melody and desired style below, generate suitable chord progressions and explain your choices.
Please return the result as JSON:
- "chords": a list of chords with their beat positions
- "explanation": a short reasoning

Melody: {melody}
Style: {style}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a harmony assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        # GPT should return a JSON string. Parse it directly.
        gpt_output = response.choices[0].message['content'].strip()
        result = json.loads(gpt_output)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)