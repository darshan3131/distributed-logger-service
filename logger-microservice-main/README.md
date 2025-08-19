
# 🔐 Logger Microservice

A lightweight microservice designed to **capture and preserve event logs** across a distributed system.  
It provides an **append-only audit trail** where new events can be recorded, but existing entries remain immutable for integrity and compliance.  

---

## 📝 Problem Context

In systems composed of multiple microservices, tracking “who did what, when, and where” is essential for observability, debugging, and compliance.  
This service acts as a **central log collector**, enabling other microservices to forward structured event data such as:

- A customer account being registered  
- Linking customer details to external identities  
- Billing or payment transactions  
- Account suspension or deactivation  

Because future services may generate **new event types**, the log schema is designed to be flexible while still storing common metadata consistently.

---

## ✨ Core Capabilities

- 🔒 **Immutable Storage** – logs can only be appended, never edited or removed  
- ⚡ **Write-Optimized** – designed for high-frequency inserts, low-frequency reads  
- 📡 **REST API** – simple HTTP endpoints to push and fetch logs  
- 🗄️ **MongoDB Backend** – optimized for sharding and fast writes  
- 🐳 **Dockerized Setup** – ready to run with Docker Compose  
- 📊 **Scalability Notes** – outlines next steps for queues, caching, and batching  

---

## 🛠️ Technology Stack

- **Backend** → Python (Flask for PoC)  
- **Database** → MongoDB (sharded, write-heavy)  
- **Deployment** → Docker + Docker Compose  
- **Planned Improvements** → Redis, NGINX, batching writes  

---

## 📡 API Design

- `POST /logs` → Add a new event  
- `GET /logs` → Retrieve all events  
- `GET /logs/<id>` → Retrieve a specific event  

---

## 🚀 Getting Started

```bash
# Clone repository
git clone https://github.com/darshan3131/distributed-logger-service.git
cd distributed-logger-service/logger-microservice-main

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the service
python logger/Services/app.py
