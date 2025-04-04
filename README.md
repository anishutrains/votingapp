# Voting App

A web-based voting application for US Presidential candidates that allows voters to cast their votes once and view real-time statistics.

## Features

- Simple one-page interface
- Voter registration with name
- Display of presidential candidates
- One vote per voter
- Real-time vote statistics with pie charts
- Mobile-responsive design

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Deployment**: Docker (optional)

## Project Structure

```
votingApp/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   ├── schema.sql
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   │       ├── candidate1.jpg
│   │       └── candidate2.jpg
│   └── templates/
│       └── index.html
├── config.py
├── init_db.py
├── requirements.txt
└── README.md
```

## Database Schema

- Voters (id, name, has_voted)
- Candidates (id, name, party, image_url)
- Votes (id, voter_id, candidate_id, timestamp)

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/votingApp.git
   cd votingApp
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python init_db.py
   ```

5. Run the application:
   ```
   flask run
   ```

6. Access the application at http://localhost:5000

## Usage

1. Enter your name to register as a voter
2. View the list of candidates
3. Select a candidate and cast your vote
4. View the real-time vote statistics

## Deployment Instructions

### Simple Deployment on Ubuntu Server (AWS Lightsail)

#### Prerequisites
- AWS account
- AWS Lightsail instance (Ubuntu 20.04 LTS or newer)

#### Step 1: Create a Lightsail Instance
1. Log in to the AWS Management Console
2. Navigate to Lightsail
3. Click "Create instance"
4. Choose Ubuntu 20.04 LTS as the blueprint
5. Select your preferred instance plan (at least 1GB RAM recommended)
6. Choose your preferred availability zone
7. Give your instance a name (e.g., "voting-app")
8. Click "Create instance"

#### Step 2: Connect to Your Instance
1. Once your instance is running, click on it in the Lightsail console
2. Click on the "Connect using SSH" button
3. This will open a browser-based SSH client

#### Step 3: Update the System
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 4: Install Required Software
```bash
# Install Python and pip
sudo apt install -y python3 python3-pip python3-venv

# Install PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Install Git
sudo apt install -y git
```

#### Step 5: Configure PostgreSQL
```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -i -u postgres

# Create a database and user
psql

#CREATE DATABASE postgres;
#CREATE USER postgres WITH PASSWORD 'admin';

# Change the password for the postgres user
ALTER USER postgres WITH PASSWORD 'admin';
GRANT ALL PRIVILEGES ON DATABASE postgres TO postgres;

\q

# Exit postgres user
exit
```

#### Step 6: Clone the Repository
```bash
# Navigate to the home directory
cd ~

# Clone the repository
git clone https://github.com/anishutrains/votingapp.git
cd votingApp
```

#### Step 7: Set Up the Application
```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# # Update the config.py file with your database credentials
# nano config.py
# ```

# Edit the config.py file to include your PostgreSQL credentials:
# ```python
# DB_TYPE = 'postgres'
# DB_HOST = 'localhost'
# DB_PORT = '5432'
# DB_NAME = 'postgres'
# DB_USER = 'postgres'
# DB_PASSWORD = 'admin'
# ```

#### Step 8: Initialize the Database

# Make sure you're in the virtual environment
source venv/bin/activate
# Run the database initialization script
python init_db.py
```

#### Step 9: Run the Application
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Run the application
python run.py
```
####step 10

1. Go to your Lightsail console
2. Click on your instance
3. Go to the "Networking" tab
4. Under "Firewall", add a new rule:
5. Application: Custom
6. Protocol: TCP
7. Port: 5000
8. Source: Anywhere (0.0.0.0/0)
9. Click "Save"

#### Step 11: Access Your Application
1. In the Lightsail console, go to your instance
2. Click on the "Networking" tab
3. Find your instance's public IP address
4. Open a web browser and navigate to `http://YOUR_IP_ADDRESS:5000`



### Deploying with Docker

#### Prerequisites
- Docker installed on your system
- Docker Compose installed on your system

#### Step 1: Create a Dockerfile
Create a file named `Dockerfile` in the root directory of your project:

```bash
nano Dockerfile
```

Add the following content:
```
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
```

#### Step 2: Create a Docker Compose File
Create a file named `docker-compose.yml` in the root directory:

```bash
nano docker-compose.yml
```

Add the following content:
```
version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - db
    environment:
      - DB_TYPE=postgres
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=postgres
      - DB_USER=postgres
      - DB_PASSWORD=admin
    volumes:
      - ./app/static:/app/app/static

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=admin

volumes:
  postgres_data:
```

#### Step 3: Build and Run the Docker Containers
```bash
# Build the containers
docker-compose build

# Start the containers
docker-compose up -d
```

#### Step 4: Initialize the Database
```bash
# Access the web container
docker-compose exec web bash

# Run the database initialization script
python init_db.py

# Exit the container
exit
```

#### Step 5: Access the Application
Open your web browser and navigate to `http://localhost:5000` to access the application.

#### Step 6: Stop the Containers
When you're done, you can stop the containers with:
```bash
docker-compose down
```

## Development Process

This project was developed as a teaching tool to demonstrate the software development process:

1. **Requirements Gathering**: Understanding the needs of a voting application
2. **Design**: Planning the database schema and user interface
3. **Implementation**: Building the application with Flask and PostgreSQL
4. **Testing**: Ensuring the application works correctly
5. **Deployment**: Making the application available for use

## License

MIT 