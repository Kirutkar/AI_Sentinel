# crew_tasks.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found. Please set it in your .env file.")

client = OpenAI(api_key=api_key)


def explain_detection(block_id, sequence, error):
    prompt = f"""
    BlockId: {block_id}
    Error: {error}

    In 2 short lines, explain why this was flagged as an anomaly.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def suggest_action(block_id, sequence, error):
    prompt = f"""
    BlockId: {block_id}
    Error: {error}

    Suggest 1–2 short actions the ops team should take.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def classify_severity(block_id, error):
    """Classify severity based on reconstruction error"""
    if error > 50:
        return "Critical"
    elif error > 30:
        return "Major"
    else:
        return "Minor"

