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
bash
sudo apt update
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx
sudo systemctl enable docker
sudo usermod -aG docker $USER

3. Deploy App
git clone https://github.com/<usuario>/bookstore-monolitica.git
cd Transformation-Monolitih-To-Distributed
docker-compose up -d

4. Configure Domain and NGINX
(see /etc/nginx/sites-available/bookstore for full config)
5. Enable HTTPS
sudo certbot --nginx -d proyecto2telematica.online

🔁 Objective 2 - Scaled Deployment
<details> <summary>Click to expand</summary>
🔄 Backend Changes
Removed internal MySQL from docker-compose.yml

Modified app.py and config.py:

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@18.235.143.239:3306/bookstore'

🗄 MySQL EC2 Configuration

1.Create EC2 Instance

2.Install MySQL

sudo apt update
sudo apt install -y mysql-server

3. Allow Remote Connections

sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Change bind-address to 0.0.0.0
sudo systemctl restart mysql

4. Create DB and User

CREATE DATABASE bookstore;
CREATE USER 'admin'@'%' IDENTIFIED BY 'TuClaveSegura';
GRANT ALL PRIVILEGES ON bookstore.* TO 'admin'@'%';
FLUSH PRIVILEGES;

☁️ Auto Scaling Group (ASG)
Launch Template: Created from the base EC2 instance image

Custom AMI: Built from EC2 base for autoscaling

Load Balancer: Configured with HTTP/HTTPS listener and target groups

ASG Configuration:

Min: 1 instance

Max: 3 instances

Trigger: CPU usage > 80%

Health check & replacement enabled

Spread across multiple availability zones

🌐 Subdomain Configuration
Subdomain: www.proyecto2telematica.online

Configured A record pointing to the Load Balancer

NGINX updated to handle subdomain traffic

SSL certificate:
sudo certbot --nginx -d www.proyecto2telematica.online

