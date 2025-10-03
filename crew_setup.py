from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

# Define the model properly
openai_llm = LLM(model="gpt-4o-mini")  # ✅ creates LLM object

# 1. Detection Explainer Agent
detection_agent = Agent(
    role="Detection Explainer",
    goal="Explain anomalies briefly in logs.",
    backstory="Expert in log analysis. Explains root causes in 1–2 lines.",
    llm=openai_llm,   # ✅ pass LLM object, not string
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