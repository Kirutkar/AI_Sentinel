from crewai import Agent, LLM
from dotenv import load_dotenv
from crewai import Crew

# Load .env for API key
load_dotenv()

# Define the model properly
openai_llm = LLM(model="gpt-4o-mini")  # ✅ creates LLM object

# 1. Detection Explainer Agent
detection_agent = Agent(
    role="Detection Explainer",
    goal="Explain anomalies briefly in logs.",
    backstory="Expert in log analysis. Explains root causes in 1–2 lines.",
    llm=openai_llm,
    verbose=True
)

# 2. Severity Classifier Agent
severity_agent = Agent(
    role="Severity Classifier",
    goal="Label severity as Critical / Major / Minor.",
    backstory="Cyber defense specialist. Uses error thresholds for severity.",
    llm=openai_llm,
    verbose=True
)

# 3. Action Advisor Agent
action_agent = Agent(
    role="Action Advisor",
    goal="Suggest 1–2 short practical actions for anomalies.",
    backstory="System reliability engineer. Suggests clear next steps.",
    llm=openai_llm,
    verbose=True
)
# Define tasks
detection_task = Task(
    agent=detection_agent,
    description="Explain why the log entry was flagged as an anomaly.",
    inputs={"block_id": "block_id", "error": "error", "sequence": "sequence"}
)
severity_task = Task(
    agent=severity_agent,
    description="Classify the severity for the anomaly.",
    inputs={"error": "error"}
)
action_task = Task(
    agent=action_agent,
    description="Suggest actions the ops team should take for this anomaly.",
    inputs={"block_id": "block_id", "error": "error", "sequence": "sequence"}
)

tasks = [detection_task, severity_task, action_task]

crew = Crew(
    agents=[detection_agent, severity_agent, action_agent],
    tasks=tasks,
)
