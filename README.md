para iniciar la base de datos y crear las tablas:

flask shell
>>> from extensions import db
>>> db.create_all()
# 📚 BookStore Monolithic Deployment

This repository contains the deployment strategy of the **BookStore Monolithic Application** using Docker, Flask, NGINX, and AWS infrastructure. It documents two major deployment phases: the initial single-instance setup and the horizontally-scaled deployment using Auto Scaling Groups (ASG) and a dedicated MySQL instance.

---

## 🌐 Live Applications

- ✅ Initial Deployment: [https://proyecto2telematica.online](https://proyecto2telematica.online)  
- 🔁 Scaled Version: [https://www.proyecto2telematica.online](https://www.proyecto2telematica.online)

---

## 📌 Objectives

### ✅ Objective 1: Monolithic Deployment on EC2

- Deployed a monolithic Flask + SQLite app using Docker
- Configured NGINX as a reverse proxy
- Set up an SSL certificate using Let's Encrypt (Certbot)
- Configured a custom domain via GoDaddy

📁 Branch: `main`

### 🔁 Objective 2: Horizontal Scaling with Auto Scaling Group (ASG)

- Introduced horizontal scalability via Auto Scaling Group
- Isolated the database into a separate EC2 instance running MySQL
- Connected multiple instances to a centralized shared MySQL backend
- Configured a Load Balancer and Launch Template for dynamic scaling
- Subdomain integration for scalability layer

📁 Branch: `scalde`

---

## ☁️ Infrastructure Overview

### EC2 Base Instance (Web App)

| Component         | Configuration                         |
|------------------|----------------------------------------|
| **AMI**           | Ubuntu Server 22.04 LTS               |
| **Type**          | `t2.micro`                            |
| **Ports**         | 22 (SSH), 80 (HTTP), 443 (HTTPS)      |
| **Domain**        | www.proyecto2telematica.online        |
| **Technologies**  | Flask, Docker, NGINX, Certbot         |

### EC2 Database Instance (MySQL)

| Component         | Configuration                         |
|------------------|----------------------------------------|
| **AMI**           | Ubuntu Server 22.04 LTS               |
| **Type**          | `t2.micro`                            |
| **Port**          | 3306 (MySQL)                          |
| **Public IP**     | 18.235.143.239                        |
| **Technologies**  | MySQL Server                          |

---

## ⚙️ Deployment Steps

### ✅ Objective 1 - Initial Deployment

<details>
<summary>Click to expand</summary>

1. **Create EC2 Instance**  
2. **Install Dependencies**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx
sudo systemctl enable docker
sudo usermod -aG docker $USER
