# Local Node Sentinel: E2E System Telemetry Monitor

This repository contains an End-to-End observability pipeline designed to monitor local hardware health (CPU and RAM usage) in real-time. It recives raw hardware metrics, structures the data, and applies unsupervised Machine Learning to automatically detect anomalies and potential system overloads.

## Key Features

*   **Real-Time Data Ingestion:** Continuous extraction of system metrics using Python (`psutil`) and lightweight local storage (SQLite).
*   **Machine Learning Anomaly Detection:** Implementation of `scikit-learn`'s Isolation Forest algorithm to identify unusual hardware behavior without predefined thresholds.
*   **Interactive Dashboard:** A `Streamlit` web interface for near real-time monitoring and anomaly visualization.
*   **Containerized Architecture:** Fully deployable using `Docker`, ensuring a reproducible and scalable environment.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Git](https://git-scm.com/)

## Installation & Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/PedroGLorenzo/local-node-sentinel.git](https://github.com/PedroGLorenzo/local-node-sentinel.git)
   cd local-node-sentinel

2. **Build and spin up the containers:**
   ```bash
   docker-compose up --build -d

3. **Access the Dashboard:**
   Once the containers are running and collecting data, open your web browser and navigate to:
   `http://localhost:8501`

4. **Stop the monitor:**
   To stop the data collection and spin down the containers, run:
   ```bash
   docker-compose down
   ```

## Project Structure

* `src/collector.py`: Extracts CPU and RAM metrics using `psutil` and stores them in a lightweight SQLite database.
* `src/detector.py`: Applies an unsupervised Machine Learning model (Isolation Forest) to detect system overloads or anomalies.
* `src/dashboard.py`: Streamlit-based web interface for real-time visualization of metrics and alerts.
* `docker-compose.yml`: Multi-container orchestration to ensure a reproducible environment.

## Author

**Pedro García Lorenzo**[cite: 1]
* GitHub: [@PedroGLorenzo](https://github.com/PedroGLorenzo)[cite: 1]
* Email: pedro.glorenzo@udc.es[cite: 1]