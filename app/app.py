import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
import openai
from kubernetes import client, config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "xxxx")

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

# Load Kubernetes configuration
config.load_kube_config()

# Create a Flask app
app = Flask(__name__)

# Function to get pod events based on pod name
def get_pod_events(pod_name):
    v1 = client.CoreV1Api()
    events = v1.list_event_for_all_namespaces()
    event_list = []
    for event in events.items:
        # Check if the event is related to the specified pod name
        if event.involved_object.name == pod_name:
            message = f"Timestamp: {event.first_timestamp}, Event: {event.message}"
            event_list.append(message)
    return event_list

# Function to summarize multiple events using OpenAI
def summarize_events_combined(events):
    # Combine all event messages into a single input for summarization
    combined_events_message = "\n\n".join(events)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {
                "role": "user",
                "content": f"Summarize these Kubernetes events:\n\n{combined_events_message}",
            }
        ],
        max_tokens=300,  # Adjust max tokens as needed
        stream=False,
    )
    # Extract and return the content of the response
    return response.choices[0].message.content

# API endpoint to get a combined summary of events
@app.route("/summarize/<pod_name>", methods=["GET"])
def summarize_logs(pod_name):
    events = get_pod_events(pod_name)
    if not events:
        return jsonify({"message": f"No events found for pod {pod_name}"}), 404

    # Get a single summary for all events
    summary = summarize_events_combined(events)
    return jsonify({"pod_name": pod_name, "summary": summary})

def main():
    app.run(host="0.0.0.0", port=8000, debug=True)

if __name__ == "__main__":
    main()
