import os
from crewai import Agent
from dotenv import load_dotenv

# Load API key
load_dotenv()

# 1. Detection Explainer Agent
detection_agent = Agent(
    role="Detection Explainer",
    goal="Explain anomalies briefly in logs.",
    backstory="Expert in log analysis. Explains root causes in 1–2 lines.",
    llm="gpt-4o-mini",
    verbose=True
)

# 2. Severity Classifier Agent
severity_agent = Agent(
    role="Severity Classifier",
    goal="Label severity as Critical / Major / Minor.",
    backstory="Cyber defense specialist. Uses error thresholds for severity.",
    llm="gpt-4o-mini",
    verbose=True
)

# 3. Action Advisor Agent
action_agent = Agent(
    role="Action Advisor",
    goal="Suggest 1–2 short practical actions for anomalies.",
    backstory="System reliability engineer. Suggests clear next steps.",
    llm="gpt-4o-mini",
    verbose=True
)
