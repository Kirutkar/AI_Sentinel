from crewai import Crew, Task
from crew_agents import detection_agent, severity_agent, action_agent

# Define tasks with explicit names
detection_task = Task(
    description="Explain anomaly in 1–2 lines.",
    agent=detection_agent,
    expected_output="A short explanation (1–2 lines) why the anomaly was detected.",
    name="Reason"
)

severity_task = Task(
    description="Classify anomaly severity into Critical, Major, or Minor.",
    agent=severity_agent,
    expected_output="One of: Critical, Major, Minor.",
    name="Severity"
)

action_task = Task(
    description="Suggest 1–2 practical actions for the ops team.",
    agent=action_agent,
    expected_output="1–2 short recommended actions.",
    name="Suggested Action"
)

# Crew pipeline
crew = Crew(
    agents=[detection_agent, severity_agent, action_agent],
    tasks=[detection_task, severity_task, action_task],
    verbose=True
)
