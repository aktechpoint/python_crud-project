# python_crud-project
# 🛠️ Python CRUD App - DevOps & Cloud Training Project

This is a simple **Python CRUD (Create, Read, Update, Delete)** application designed as part of **DevOps and Cloud training**. It demonstrates essential backend operations and prepares the project for Docker, CI/CD, AWS deployment, and infrastructure automation.

## 🚀 Project Goals

- Build a clean Python-based CRUD backend
- Practice deploying apps to cloud platforms like **AWS EC2**, **Elastic Beanstalk**, or **Docker on ECS**
- Integrate DevOps tools such as:
  - Git & GitHub
  - Docker
  - GitHub Actions / Jenkins
  - Terraform / Ansible
  - Monitoring & Logging tools (Prometheus, Grafana, ELK)

---

## 🧰 Tech Stack

- **Language**: Python 3
- **Framework**: Django / Flask (depending on your actual project)
- **Database**: SQLite / PostgreSQL / MySQL
- **DevOps Tools**: Docker, GitHub Actions, AWS, Terraform, Jenkins (optional)

---
## Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
## Install Requirements
pip install -r requirements.txt

## Run the App
python manage.py runserver
## Docker (Optional)
docker build -t python-crud-app .
docker run -d -p 5000:5000 python-crud-app

