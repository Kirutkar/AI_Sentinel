# 🛡️ AI Sentinel – Intelligent Log Anomaly Detector

AI Sentinel is an intelligent **cybersecurity monitoring system** that detects anomalies in system log data using **Deep Learning (Autoencoder)** and explains the root cause with **AI Agents (CrewAI + GPT)**.

---

## 🚀 Overview

Most large-scale systems (like data servers or distributed file systems) generate millions of log entries daily.  
Identifying abnormal patterns manually is nearly impossible — that’s where **AI Sentinel** comes in.

1. It learns normal log patterns using a **Deep Learning Autoencoder model**.
2. Detects unusual behavior (anomalies) in new logs.
3. Uses **AI agents** to explain *why* it happened and *what action* to take.
4. Ensures safe AI responses using a **lightweight Guardrail** filter.

---

## 🧠 Tech Stack

- **Python 3.10 / 3.13**
- **TensorFlow (Autoencoder model)**
- **CrewAI (Multi-Agent Framework)**
- **Streamlit (Frontend + Deployment)**
- **OpenAI GPT Integration**
- **CI/CD:** Automated deployment via **GitHub → Render/Streamlit Cloud**

---

## 🏗️ Architecture

1. **Autoencoder Model (`ai_sentinel_autoencoder.h5`)**
   - Learns normal system log patterns.
   - High reconstruction error = anomaly detected.

2. **Streamlit App**
   - Upload `.csv` log files.
   - Visualizes normal vs anomalous logs.
   - Calls CrewAI pipeline for explanation and actions.

3. **CrewAI Agents**
   - `Detection Agent` → Explains anomaly cause.
   - `Severity Agent` → Classifies as *Critical, Major, Minor*.
   - `Action Agent` → Suggests operations fix.

4. **Guardrail**
   - Filters GPT outputs for irrelevant or technical junk (tracebacks, code, etc.).
   - Keeps responses short, relevant, and clean.

---

## 🧩 Dataset Used

The project uses **HDFS (Hadoop Distributed File System) Logs** —  
a real dataset of server log sequences from large distributed systems.  

It represents how files are read/written/replicated across clusters.  
Each “BlockId” represents a file block operation — like:
Block 14205 starts replication
Block 14205 completed successfully
Block 14205 corrupted

When any unusual pattern occurs, the autoencoder flags it as **Anomaly**.

---

## 📦 Example Workflow

1. Upload a preprocessed HDFS `.csv` file.
2. Model reconstructs the sequence → finds anomaly (based on error).
3. CrewAI agents analyze and generate:
   - **Reason:** Why it happened.
   - **Severity:** Critical/Major/Minor.
   - **Suggested Action:** What to do next.

---

## 🧩 Lightweight Guardrail Explanation

- Guardrail runs after GPT gives a response.
- It removes unwanted text like:
  - “Traceback”, “Error”, “Exception”, or “line …”
- If a non-log file (wrong CSV) is uploaded:
  - The model tries to read it.
  - Since data pattern doesn’t match trained format, reconstruction error spikes.
  - The system automatically classifies all rows as **Anomaly**.
  - CrewAI still runs but responses will be *cleanly filtered* via Guardrail.

This shows robustness and safe output handling.

---

## 🔁 CI/CD Implementation

- The project is **auto-deployed** through GitHub → Render.
- Every code commit triggers a build pipeline.
- If the build succeeds, the app updates automatically.
- You can verify builds under the **Render dashboard (Logs tab)**.

---

## 💡 Future Improvements

- Add live log streaming.
- Connect to real server monitoring dashboards.
- Include GPT response validation using advanced Guardrails or LlamaGuard.

---

## 🙌 Achievements

✅ Deep Learning-based anomaly detection  
✅ Multi-agent reasoning pipeline  
✅ Lightweight guardrail for safe AI responses  
✅ First-ever CI/CD deployment via GitHub  
✅ Successful live demo using Streamlit Cloud

---

## 🧑‍💻 Author

**Kiruthika Ramalingam**  
AI & Automation Enthusiast | DDS Challenge 2025 Participant  
📍 UAE | 🔗 [LinkedIn](https://linkedin.com/in/kiruthikaramalingam)