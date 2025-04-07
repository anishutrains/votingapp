# Voting App

A web-based voting application for US Presidential candidates that allows voters to cast their votes once and view real-time statistics.

## Features

- Simple one-page interface with vibrant democracy theme
- Voter registration with name
- Display of presidential candidates with party information
- One vote per voter
- Real-time vote statistics with pie charts
- Mobile-responsive design

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Backend**: Python Flask
- **Database**: PostgreSQL
- **Deployment**: AWS Lightsail or Docker

## Project Structure

```
votingApp/
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── images/
│   │       ├── candidate1.jpg
│   │       ├── candidate2.jpg
│   │       ├── home_main.jpg
│   │       └── usa_flag.png
│   └── templates/
│       └── index.html
├── backend/
│   ├── __init__.py
│   ├── routes/
│   │   └── main.py
│   └── run.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── models.py
│   ├── init_db.py
│   └── schema.sql
├── config/
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Database Schema

- Voters (id, name, has_voted)
- Candidates (id, name, party, image_url)
- Votes (id, voter_id, candidate_id, timestamp)

## Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/anishutrains/votingapp.git
   cd votingApp
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```



4. Run the application:
   ```
   python -m backend.run
   ```

6. Access the application at http://localhost:5000

## Deployment Instructions

### Option 1: Deploy on AWS Lightsail (Ubuntu)

#### Prerequisites
- AWS account
- AWS Lightsail instance (Ubuntu 20.04 LTS or newer)

#### Step 1: Create a Lightsail Instance
1. Log in to the AWS Management Console
2. Navigate to Lightsail
3. Click "Create instance"
4. Choose Pick your instance image(Linux/Unix)->Ubuntu 24.04 LTS as the blueprint(from Operating System (OS) only)
5. Select your preferred instance plan (at least 1GB RAM recommended)
6. Give your instance a name (e.g., "voting-app")
7. Click "Create instance"

#### Step 2: Connect to Your Instance
1. Once your instance is running, click on it in the Lightsail console
2. Click on the "Connect using SSH" button

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

# Set password for postgres user
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'admin';"
```

#### Step 6: Clone the Repository
```bash
# Navigate to the home directory
cd ~

# Clone the repository
git clone https://github.com/anishutrains/votingapp.git
cd votingapp
```

#### Step 7: Set Up the Application
```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

#### Step 8: Run the Application
```bash
# Run the application
python -m backend.run
```

#### Step 9: Configure Firewall
1. Go to your Lightsail console
2. Click on your instance
3. Go to the "Networking" tab
4. Under "Firewall", add a new rule:
   - Application: Custom
   - Protocol: TCP
   - Port: 5000
   - Source: Anywhere (0.0.0.0/0)
5. Click "Save"

#### Step 11: Access Your Application
1. In the Lightsail console, go to your instance
2. Click on the "Networking" tab
3. Find your instance's public IP address
4. Open a web browser and navigate to `http://YOUR_IP_ADDRESS:5000`

### Option 2: Deploy with Docker

#### Prerequisites
- Docker installed on your system

#### Installing Docker

##### For Ubuntu (AWS Lightsail):
```bash
# Update package index
sudo apt update

# Install Docker using the convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the docker group (to run docker without sudo)
sudo usermod -aG docker $USER

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

##### For Windows:
1. Download Docker Desktop from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the installation wizard
4. Restart your computer
5. Open PowerShell and verify installation:
```powershell
docker --version
```

#### Step 1: clone application , Build and Run the Application

```bash
# Clone the repository
git clone https://github.com/anishutrains/votingapp.git
cd votingapp

# Build the Docker image
sudo docker build -t voting-app .

# Create a Docker network
sudo docker network create voting-network

# Run PostgreSQL container
sudo docker run -d --name postgres-db --network voting-network -e POSTGRES_PASSWORD=admin postgres:13

# Run the application container
sudo docker run -d --name voting-app --network voting-network -p 5000:5000 voting-app
```

#### Step 2: Access the Application
Open your web browser and navigate to `http://localhost:5000` to access the application.

#### Step 3: Stop the Containers
When you're done, you can stop the containers with:
```bash
docker stop voting-app postgres-db
docker rm voting-app postgres-db
docker network rm voting-network
```

## Usage

1. Enter your name to register as a voter
2. View the list of candidates
3. Select a candidate and cast your vote
4. View the real-time vote statistics

## Development Process

This project was developed as a teaching tool to demonstrate the software development process:

1. **Requirements Gathering**: Understanding the needs of a voting application
2. **Design**: Planning the database schema and user interface
3. **Implementation**: Building the application with Flask and PostgreSQL
4. **Testing**: Ensuring the application works correctly
5. **Deployment**: Making the application available for use

