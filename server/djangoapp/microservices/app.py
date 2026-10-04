"""Small Flask sentiment-analysis microservice."""

from flask import Flask, jsonify


app = Flask("Sentiment Analyzer")


@app.get("/")
def home():
    """Describe the sentiment endpoint."""
    return "Welcome to the Sentiment Analyzer. Use /analyze/text"


@app.get("/analyze/<path:input_txt>")
def analyze_sentiment(input_txt):
    """Classify text with a deterministic automotive-review lexicon."""
    lowered = input_txt.lower()
    positive = ("fantastic", "excellent", "great", "good", "love", "helpful")
    negative = ("bad", "awful", "terrible", "poor", "hate", "worst")
    sentiment = "neutral"
    if any(word in lowered for word in positive):
        sentiment = "positive"
    elif any(word in lowered for word in negative):
        sentiment = "negative"
    return jsonify({"sentiment": sentiment})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
