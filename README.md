# 💠 Privacy Provisor: Zero-Trust LLM Proxy

**A secure middleware architecture designed to intercept, anonymize, and manage Personally Identifiable Information (PII) within AI-driven workflows.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](YOUR_STREAMLIT_LINK_HERE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Overview
Privacy Provisor acts as a security gateway between users and Large Language Models (LLMs). By utilizing a **Zero-Trust** approach, this system ensures that sensitive data—such as emails, phone numbers, and names—never leaves the local environment. It leverages NLP-based entity recognition to redact PII in real-time, substituting them with dynamic tokens before processing.

## 🛠️ Technical Architecture
The system is built on a decoupled, two-tier cloud architecture:

* **Security Engine (Backend):** Built with **FastAPI** and **Microsoft Presidio**. It utilizes **spaCy (en_core_web_sm)** for high-speed, low-latency entity detection.
* **Dynamic Vault (Storage):** A **SQLite** database handles stateful token-to-PII mapping, ensuring that AI responses can be de-anonymized seamlessly without storing data in RAM.
* **Intelligence:** Integrated with **Google Gemini 1.5 Flash** for high-context, secure reasoning.
* **Interface (Frontend):** A custom-themed **Streamlit** dashboard designed for a "Cyber-Ops" user experience.

## 🛡️ Security Features
* **NLP Redaction:** Automated detection of PII using Microsoft Presidio.
* **Dynamic Tokenization:** Replaces PII with non-sensitive identifiers (e.g., `<EMAIL_ADDRESS_1>`).
* **Context Preservation:** Instructs the LLM to maintain token integrity for accurate de-anonymization.
* **Environment Isolation:** Secure handling of API keys via `.env` and cloud-native secret management.

## 🚀 Getting Started

### Prerequisites
* Python 3.9+
* Google Gemini API Key

### Installation & Setup
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/Amandubey11/Privacy_Provisor.git](https://github.com/Amandubey11/Privacy_Provisor.git)
   cd Privacy_Provisor
