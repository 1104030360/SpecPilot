# SpecPilot

> **AI Specification Accelerator | From Idea to Specification**

[![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

Allows people to quickly transform raw ideas into complete specification documents, enabling development based on the spec when using AI Coding to reduce hallucinations and improve accuracy.

## 💡 Why is this tool needed?

In the era of AI Coding, the biggest challenge is not writing code, but **how to make the AI understand your requirements**. The goals of this project are:

1.  **Accelerate the specification output process** - From a vague idea → a clear specification document, what originally took hours now takes only a few minutes.
2.  **Reduce AI hallucinations** - With a structured specification (DBML + Gherkin), the AI can generate code more accurately.
3.  **Improve development quality** - Specification-first makes the development process more controllable, testable, and maintainable.

### Traditional Workflow vs. AI-Accelerated Workflow

**Traditional Workflow (time-consuming and error-prone):**
```
💭 Idea → 📝 Handwritten documents → 🤔 Multiple revisions → 💻 Development → 🐛 Discover unclear requirements → ♻️ Re-discussion
```

**AI-Accelerated Workflow (fast and precise):**
```
💭 Idea → 🤖 AI derives detailed requirements → 📋 Automatically generate specs → 🔍 AI checks for omissions → ✅ Confirm specs → 💻 AI Coding
```

---

## 🚀 Complete Quickstart Guide

### Prerequisites

- **Python 3.8+**
- **macOS / Linux / Windows** are all supported
- **AI Service** (choose one):
  - OpenAI API Key (recommended, paid)
  - Ollama local LLM (free, requires installation)

### Step 1: Install Python Virtual Environment

```bash
# Check Python version (requires 3.8+)
python3 --version

# Enter the project directory
cd /Users/linjunting/Desktop/Django

# If you don't have a virtual environment, create one first
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Confirm the virtual environment is activated (the terminal will show (venv))
```

### Step 2: Install Dependencies

```bash
# Install Django core
pip install Django==5.2.8
pip install python-dotenv==1.0.0

# Choose your AI service
# Option A: OpenAI API (recommended)
pip install openai==1.3.0

# Option B: Ollama local LLM (free)
pip install ollama==0.1.0

# Full installation (all features)
pip install -r requirements.txt
```

### Step 3: Set Environment Variables

```bash
# Copy the environment variable template
cp .env.example .env

# Edit the .env file
nano .env
# Or use your favorite editor
open .env
```

**Minimum required settings (.env file content):**

```bash
# Django settings
DJANGO_SECRET_KEY=your-random-secret-key-change-this
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API (if using OpenAI)
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Ollama (if using a local LLM)
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

**How to get an OpenAI API Key:**
1.  Visit https://platform.openai.com/api-keys
2.  Log in or create an account
3.  Click "Create new secret key"
4.  Copy the API Key and paste it into `OPENAI_API_KEY` in `.env`

**How to use Ollama (free option):**
```bash
# macOS installation
brew install ollama

# Start the Ollama service
ollama serve

# Download the model in a new terminal window
ollama pull llama2
```

### Step 4: Check Environment Settings

```bash
# Run the environment check script
python check_env.py

# If it shows ✅, the settings are correct
# If it shows ❌, please correct according to the prompts
```

### Step 5: Initialize the Database

```bash
# Enter the Django project directory
cd mysite

# Run database migrations
python manage.py migrate

# Seeing "OK" means success
```

### Step 6: Start the Development Server

```bash
# Start the server (default port 8000)
python manage.py runserver

# Or specify an IP and port (to allow access from other devices)
python manage.py runserver 0.0.0.0:8000
```

### Step 7: Start Using

Open your browser and visit:
- **Main Application**: http://127.0.0.1:8000/polls/
- **Admin Backend**: http://127.0.0.1:8000/admin/ (requires creating an admin account first)

---

## 🐳 Start the Project with Docker (Recommended)

If you have Docker Desktop installed, you can use Docker to quickly start the project without manually setting up a Python environment.

### Why Choose Docker?

✅ **Environment Consistency** - Development, testing, and production environments are identical
✅ **Fast Deployment** - Start the entire application with one command
✅ **Easy Management** - Doesn't affect your local Python environment
✅ **Cross-Platform** - Works on macOS, Linux, and Windows

### Prerequisite: Install Docker Desktop

#### macOS Installation
```bash
# Method 1: Use Homebrew (recommended)
brew install --cask docker

# Method 2: Manual download
# Visit https://www.docker.com/products/docker-desktop
# Download Docker Desktop for Mac and install it
```

#### Windows Installation
1.  Visit https://www.docker.com/products/docker-desktop
2.  Download Docker Desktop for Windows
3.  Run the installer and restart your computer
4.  Ensure WSL 2 (Windows Subsystem for Linux) is enabled

#### Linux Installation
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# CentOS/RHEL
sudo yum install docker docker-compose
```

**Post-installation verification**:
```bash
docker --version
# Should output: Docker version 27.x.x or higher
```

### Docker Startup Steps (Just 3 steps)

#### Step 1: Set Environment Variables
```bash
cd /Users/linjunting/Desktop/Django

# Copy the environment variable template
cp .env.example .env

# Edit the .env file and set the necessary parameters
nano .env
```

**Required environment variables**:
```bash
DJANGO_SECRET_KEY=your-random-secret-key
OPENAI_API_KEY=sk-your-openai-api-key  # Or use Ollama
```

#### Step 2: Add Docker to PATH (macOS only, one-time setup)

If you encounter a `docker: command not found` error, run the following command:

```bash
# Add the following to your shell configuration file
echo 'export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"' >> ~/.zshrc

# Reload the configuration
source ~/.zshrc

# Verify Docker is available
docker --version
```

#### Step 3: Start the Docker Containers
```bash
# Build the Docker image (needed the first time, takes about 1-2 minutes)
docker compose build

# Start the containers (in detached mode)
docker compose up -d

# Check the container status
docker compose ps
```

**Expected output**:
```
NAME              STATUS          PORTS
django-spec-gen   Up 10 seconds   0.0.0.0:8000->8000/tcp
```

#### Step 4: Access the Application
Open your browser and visit:
- **Main Application**: http://localhost:8000/polls/
- **Admin Backend**: http://localhost:8000/admin/

### Common Docker Commands

```bash
# View container logs
docker compose logs -f web

# Stop containers (without deleting them)
docker compose stop

# Start stopped containers
docker compose start

# Stop and delete containers (database will not be lost)
docker compose down

# Rebuild the image (after modifying the Dockerfile)
docker compose up -d --build

# Execute a command inside a container
docker compose exec web bash

# Execute Django management commands
docker compose exec web python mysite/manage.py migrate
docker compose exec web python mysite/manage.py createsuperuser
```

### Advantages of Docker Deployment

| Feature | Traditional Method | Docker Method |
|---|---|---|
| Environment Setup | Manual installation of Python, dependencies | One command to complete |
| Environment Isolation | May affect system Python | Completely isolated |
| Version Management | Difficult to control | Docker image versioning |
| Deployment Speed | Requires step-by-step setup | Fast deployment |
| Cross-Platform | May encounter compatibility issues | Completely consistent |

### Troubleshooting

#### Issue 1: Port 8000 is already in use
```bash
# Find the process using port 8000
lsof -i :8000

# Stop that process or modify docker-compose.yml
# Change "8000:8000" to "8001:8000"
```

#### Issue 2: Container fails to start
```bash
# View detailed logs
docker compose logs web

# Check if the .env file exists
ls -la .env
```

#### Issue 3: Code changes are not updated
```bash
# Docker does not automatically sync code by default
# You need to rebuild the image
docker compose up -d --build
```

#### Issue 4: Database file is missing
```bash
# Check volume mounts
docker compose config

# Ensure docker-compose.yml has:
# volumes:
#   - ./mysite/db.sqlite3:/app/mysite/db.sqlite3
```

---

## 🎯 Core Features and Workflow

### Three-Stage Intelligent Specification Generation System

#### Stage 1: AI Idea Derivation 💡
**Purpose**: Turn a vague idea into three detailed proposals

```
Input: "I want to make a restaurant ordering system"
↓ AI Processing
Output:
  Option A: Traditional table-side ordering system
  Option B: QR code self-service ordering system
  Option C: Intelligent recommendation ordering system
```

**How to use**:
1.  Go to the "AI Idea Derivation" page
2.  Enter your simple idea (one sentence is enough)
3.  The AI will automatically generate three detailed proposals
4.  Choose the most suitable proposal

#### Stage 2: Specification Generator 📋
**Purpose**: Convert the selected proposal into a structured specification

**Automatically generated fields**:
- 📌 Project Goal
- ⚙️ Core Features
- 🔧 Technical Constraints
- 👥 Target Audience

**Features**:
- ✨ One-click parallel generation of all fields (4x efficiency boost)
- 🎨 Deep purple-orange gradient theme for visual clarity
- 💾 Real-time saving, edit anytime

#### Stage 3: Advanced Specification Output (Three Steps) 🚀

**Step 1: Formulation**
- Extract data models (DBML) from the raw specification text
- Automatically generate feature models (Gherkin)
- Follows the "no-assumption principle": only extracts explicit content, does not make assumptions

**Step 2: Discovery**
- AI automatically scans the specification to identify ambiguities and omissions
- Generates a list of clarifying questions
- Checks for: necessary information, consistency, completeness, feasibility

**Step 3: Clarify**
- Answer the clarifying questions one by one
- Instantly update the DBML and Gherkin specifications
- Track progress (Completed X / Total Y)
- Generate a complete specification result page

#### Final Output 📄

**The complete specification result includes**:
1.  **Background Description** - Project overview in Markdown format
2.  **Project Goals** - List-style goal description
3.  **Data Model** - Entity-relationship diagram in DBML format
4.  **Feature Specification** - User stories in Gherkin format
5.  **Flowchart** - Mermaid diagram (auto-rendered)
6.  **API Specification** - RESTful API design document

### Auxiliary Functions

#### ⚖️ Weight Configuration Management
**Purpose**: Set the formula for calculating Ticket priority

**Four weight descriptions**:
- **A Weight**: Importance of impact (how many users or systems are affected)
- **B Weight**: Importance of urgency (how quickly it needs to be handled)
- **C Weight**: Importance of technical complexity (difficulty of implementation)
- **D Weight**: Importance of business value (contribution to the business)

**Constraint**: The sum of the four weights must equal 1.0

**Example**:
```
Option A (Balanced): A=0.25, B=0.25, C=0.25, D=0.25
Option B (Urgency Priority): A=0.2, B=0.5, C=0.1, D=0.2
Option C (Value-Oriented): A=0.2, B=0.1, C=0.2, D=0.5
```

---

## 🛠️ Tech Stack

### Backend
- **Django 5.2.8** - Web framework
- **SQLite3** - Development database
- **Python 3.8+** - Programming language

### AI Services
- **OpenAI GPT-4** - Commercial AI model (recommended)
- **Ollama** - Local LLM (free alternative)
  - Supported models: llama2, mistral, codellama, etc.

### Frontend
- **HTML5 + CSS3** - Responsive interface
- **Vanilla JavaScript** - No framework dependencies
- **Mermaid.js** - Flowchart rendering
- **Marked.js** - Markdown rendering

### Data Models
- 11 Django Models
- Including: User, Order, WeightConfiguration, ChatSession, etc.

---

## 📦 Project Structure

```
Django/
├── README.md                   # 📘 This file (complete guide)
├── ENV_SETUP.md               # 🔑 Environment variable setup tutorial
├── MANUAL.md                  # 📖 User manual and API documentation
├── .env.example               # 📋 Environment variable template
├── requirements.txt           # 📦 Python dependency list
├── check_env.py              # ✅ Environment check script
├── venv/                     # 🐍 Python virtual environment
│
├── docs/                     # 📚 Documentation directory
│   └── schedule-mustupdate/
│       ├── report/          # 📊 Project completion reports (11 files)
│       ├── plan/finish/     # ✅ Completed tasks (12 items)
│       └── todo/            # 📝 To-do items
│
└── mysite/                   # 🎯 Main Django project directory
    ├── manage.py            # Django management script
    ├── db.sqlite3           # SQLite database
    │
    ├── mysite/              # Project settings
    │   ├── settings.py      # Django settings (integrated with .env)
    │   ├── urls.py          # URL routing configuration
    │   └── wsgi.py          # WSGI entry point
    │
    └── polls/               # Main application
        ├── models.py        # 11 data models
        ├── views.py         # 50+ API endpoints
        ├── urls.py          # URL routing configuration
        ├── api_utils.py     # AI API utility functions
        ├── tests*.py        # Test files (111 tests)
        │
        ├── templates/polls/ # HTML templates
        │   └── index.html   # Main interface (2000+ lines)
        │
        └── migrations/      # Database migration files
```

---

## 🧪 Testing Guide

### Run All Tests

```bash
# Enter the Django project directory
cd mysite

# Run the full test suite
python manage.py test polls

# Verbose mode (show each test)
python manage.py test polls -v 2

# Parallel execution (faster)
python manage.py test polls --parallel
```

### Run Specific Test Modules

```bash
# Test user and order functionality
python manage.py test polls.tests_user_order -v 2

# Test AI generation functionality
python manage.py test polls.tests_gpt_generate -v 2

# Test semantic similarity
python manage.py test polls.tests_sentence_similarity -v 2

# Test advanced specification output
python manage.py test polls.tests_advanced_spec -v 2
```

### Test Statistics

- **Total Tests**: 111
- **Pass Rate**: 100%
- **Execution Time**: ~3.8 seconds (single-threaded)
- **Test Coverage**:
  - ✅ User CRUD
  - ✅ Order Management
  - ✅ AI Text Generation
  - ✅ Semantic Similarity Analysis
  - ✅ Weight Configuration Validation
  - ✅ Advanced Specification Output (3 stages)
  - ✅ API Endpoint Responses

---

## 🌐 API Endpoint Overview

### Authentication & User Management
```
POST   /polls/user/              Create user
GET    /polls/user/              List all users
GET    /polls/user/<id>/         Get user details
PUT    /polls/user/<id>/         Update user
DELETE /polls/user/<id>/         Delete user
```

### Order Management
```
POST   /polls/order/             Create order
GET    /polls/order/             List all orders
GET    /polls/order/<id>/        Get order details
PUT    /polls/order/<id>/        Update order
DELETE /polls/order/<id>/        Delete order
```

### AI Specification Generation (Core Functionality)
```
POST   /polls/llm-idea/          AI idea derivation (generates 3 proposals)
POST   /polls/generate-field/    AI field generation (single field)
POST   /polls/formulation/       Formulation stage
POST   /polls/discovery/         Discovery stage
POST   /polls/clarify/           Clarify stage
POST   /polls/generate_complete_result/  Generate complete result page
```

### Configuration Management
```
GET/POST  /polls/weight-config/     Weight configuration
GET/POST  /polls/field-priority/    Field priority
GET/POST  /polls/gpt-prompt/        GPT Prompt configuration
GET/POST  /polls/sync-path/         Path synchronization configuration
```

**For complete API documentation, please see**: [MANUAL.md](MANUAL.md#api-documentation)

---

## 🛠️ Development Tools & Tips

### Django Shell (Interactive Testing)

```bash
# Start Django Shell
python manage.py shell

# Test OpenAI connection
from polls.api_utils import test_openai_connection
success, message = test_openai_connection()
print(message)

# Test Ollama connection
from polls.api_utils import test_ollama_connection
success, message = test_ollama_connection()
print(message)

# Query data
from polls.models import User
users = User.objects.all()
print(users)
```

### Database Management

```bash
# Create new migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Reset the database (⚠️ will delete all data)
rm db.sqlite3
rm -r polls/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Create an Admin Account

```bash
# Create a superuser
python manage.py createsuperuser

# Enter:
# - Username: admin
# - Email: admin@example.com
# - Password: (enter twice)

# Visit http://127.0.0.1:8000/admin/
```

### View Project Settings

```bash
# Check the loading status of environment variables
python check_env.py

# Show Django settings
python manage.py diffsettings
```

---

## 🚨 FAQ & Solutions

### Q1: ModuleNotFoundError when running `python manage.py runserver`?

**Cause**: Virtual environment not activated or dependencies not installed.

**Solution**:
```bash
# Activate the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install Django==5.2.8 python-dotenv==1.0.0

# If problems persist, do a full reinstall
pip install -r requirements.txt
```

### Q2: OpenAI API returns 401 Unauthorized?

**Cause**: API Key is incorrect or not set.

**Solution**:
```bash
# Check the .env file
cat .env | grep OPENAI_API_KEY

# Ensure the format is correct
OPENAI_API_KEY=sk-proj-xxxxxxxxxx  # ✅ Correct
OPENAI_API_KEY='sk-proj-xxx'      # ❌ Incorrect (do not add quotes)

# Restart the server for the environment variables to take effect
python manage.py runserver
```

### Q3: Cannot find .env file?

**Cause**: Not created from the template.

**Solution**:
```bash
# Copy the template
cp .env.example .env

# Edit the file
nano .env

# Or edit with a GUI editor
open .env
```

### Q4: Ollama connection failed?

**Cause**: Ollama service is not running.

**Solution**:
```bash
# Check if Ollama is installed
ollama --version

# If not installed (macOS)
brew install ollama

# Start the Ollama service
ollama serve

# Download a model in a new terminal window
ollama pull llama2

# Test the connection
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello"
}'
```

### Q5: Database migration error?

**Cause**: Migration file conflicts or inconsistencies.

**Solution**:
```bash
# Method 1: Fake migration (if you have manually created the database)
python manage.py migrate --fake

# Method 2: Full reset (⚠️ will delete all data)
rm db.sqlite3
rm -r polls/migrations/0*.py
python manage.py makemigrations polls
python manage.py migrate
```

### Q6: Tests are failing?

**Cause**: Inconsistent database state or missing dependencies.

**Solution**:
```bash
# Re-run migrations
python manage.py migrate

# Clear the test database
python manage.py flush --noinput

# Re-run tests
python manage.py test polls -v 2
```

### Q7: AI generation is very slow?

**Cause**: Using local Ollama or network latency.

**Recommended Solutions**:
1.  **Switch to OpenAI API** (fast but paid).
2.  **Use a smaller Ollama model** (e.g., llama2:7b).
3.  **Enable caching** (to avoid repeated generation).

### Q8: Frontend page is blank or has style errors?

**Cause**: Static files not loaded or browser cache.

**Solution**:
```bash
# Clear browser cache (Cmd+Shift+R or Ctrl+Shift+R)

# Check Django settings
python manage.py collectstatic --noinput

# Confirm template paths
python manage.py check --deploy
```

---

## 📊 Project Statistics

### Code Scale
- **Total Lines**: ~12,000+
- **Python Code**: ~4,000 lines
- **Frontend Code**: ~2,000 lines (HTML + CSS + JS)
- **Test Code**: ~1,500 lines

### Feature Statistics
- **Data Models**: 11 (User, Order, WeightConfiguration, etc.)
- **API Endpoints**: 50+
- **Test Cases**: 111 (100% passing)
- **Frontend Pages**: 5 main sections
- **AI Prompts**: 15+ professional prompts

### Document Statistics
- **README**: This file (complete guide)
- **User Manual**: MANUAL.md (API documentation)
- **Environment Setup**: ENV_SETUP.md (API Key tutorial)
- **Completion Reports**: 11 phase reports
- **To-do List**: 12 completed tasks

---

## 🎯 Example Use Cases

### Scenario 1: Quickly Validate a Product Idea

```
1. Open "AI Idea Derivation"
2. Enter: "I want to build an online course platform"
3. AI generates three proposals:
   - Option A: Traditional pre-recorded course platform
   - Option B: Interactive live teaching platform
   - Option C: AI-personalized learning system
4. Choose the most suitable proposal
5. Generate a complete specification with one click
6. Take it directly to an AI Coding tool
```

**Time**: 5-10 minutes
**Output**: Complete DBML + Gherkin + API specifications

### Scenario 2: Team Collaboration on Specifications

```
1. PM inputs initial requirements into "Advanced Specification Output"
2. Formulation automatically extracts data models and features
3. Discovery finds 15 issues that need clarification
4. The team answers the questions one by one
5. Clarify instantly updates the specification
6. Download the final specification document (DBML + Gherkin)
7. The development team proceeds with development based on the spec
```

**Time**: 30-60 minutes
**Output**: A complete specification confirmed by team discussion

### Scenario 3: Refactor Documentation for an Old Project

```
1. Paste the README or requirements document of the old project
2. Formulation automatically reverse-engineers the data structure
3. Discovery finds contradictions and omissions in the document
4. Supplement the missing information
5. Generate a standardized specification document
6. Use it as a baseline for refactoring
```

**Time**: 20-40 minutes
**Output**: Standardized DBML + Gherkin documents

---

## 🚀 Next Steps Checklist

### Get Started Now (5 minutes)
- [x] ✅ Read this README
- [ ] 🔧 Set up environment variables (see [ENV_SETUP.md](ENV_SETUP.md))
- [ ] ✅ Run tests to confirm the environment
- [ ] 🚀 Start the server
- [ ] 🎨 Visit http://127.0.0.1:8000/polls/

### Dive Deeper (30 minutes)
- [ ] 📖 Read the [MANUAL.md](MANUAL.md) user manual
- [ ] 🧪 Try the "AI Idea Derivation" feature
- [ ] 📋 Try the "Specification Generator" feature
- [ ] 🚀 Try the full "Advanced Specification Output" workflow

### Advanced Usage (1 hour)
- [ ] ⚖️ Set up your own weight configuration scheme
- [ ] 🎯 Customize GPT Prompts for tailored output
- [ ] 🧪 Run the full test suite
- [ ] 📚 Review the project completion reports

---

## 📞 More Resources

### Document Links
- **[ENV_SETUP.md](ENV_SETUP.md)** - Complete guide to environment variable setup
- **[MANUAL.md](MANUAL.md)** - User manual and API documentation
- **[PROJECT_COMPLETION_SUMMARY.md](docs/schedule-mustupdate/report/PROJECT_COMPLETION_SUMMARY.md)** - Project completion summary

### External Resources
- **OpenAI API Documentation**: https://platform.openai.com/docs
- **Ollama Documentation**: https://ollama.ai/
- **Django Documentation**: https://docs.djangoproject.com/
- **DBML Syntax**: https://dbml.dbdiagram.io/docs/
- **Gherkin Syntax**: https://cucumber.io/docs/gherkin/

---

## 📄 License & Contribution

This project is an internal development project. All rights reserved.

---

**Last Updated**: November 7, 2025
**Version**: v2.0.0
**Status**: ✅ Production Ready
**Maintainer**: The Project Team

---

## 💬 Conclusion

The core philosophy of this project is: **Make AI understand your needs better**.

In the age of AI Coding, writing code is no longer the hardest part; the hardest part is clearly expressing your requirements. This tool is designed to solve this problem—by quickly transforming vague ideas into structured specifications, allowing AI to help you realize your needs more accurately.

We hope this tool will accelerate your development process, reduce communication costs, and improve product quality! 🚀

---

### 🔑 Environment Setup (Must Read!)
- **[ENV_SETUP.md](ENV_SETUP.md)** - Complete guide to environment variable setup
  - How to get an OpenAI API Key
  - How to use the free Ollama local LLM
  - API Key security best practices

### 📖 User Manual
- **[MANUAL.md](MANUAL.md)** - Complete user manual
  - Feature usage guide
  - Complete API documentation (50+ endpoints)
  - FAQ
  - Development tools explanation

### 📊 Project Report
- **[PROJECT_COMPLETION_SUMMARY.md](docs/schedule-mustupdate/report/PROJECT_COMPLETION_SUMMARY.md)** - Project completion summary
  - Status of 12 completed phases
  - 111 test cases (100% passing)
  - Tech stack and architecture explanation

---

## 🎯 Main Features

### ✨ Core Features
- 📝 **Automatic Specification Generation** - Automatically generate spec documents based on project requirements
- 🤖 **AI Assistance** - Supports OpenAI GPT-4 or local Ollama
- 🔍 **Semantic Similarity Analysis** - Intelligently detects duplicate requirements
- ⚖️ **Weight Configuration Management** - Visual weight editor
- 🎯 **Field Priority Configuration** - Drag-and-drop priority management
- 📊 **Ticket Scoring System** - Automatically calculates weighted scores

### 🛠️ Admin Features
- 👤 **User Management** - Full CRUD + password encryption
- 📦 **Order Management** - Order status tracking
- 💬 **Chat Session Management** - AI conversation logs
- 📤 **File Upload** - Supports .xlsx files
- 🔗 **Path Sync Configuration** - Cloud sync settings
- 🧠 **FAISS Vector Index** - Fast semantic search

---

## 🔧 Tech Stack

- **Backend**: Django 5.2.8
- **Database**: SQLite3 (Development) / PostgreSQL (Production)
- **AI Service**: OpenAI API / Ollama
- **Semantic Analysis**: Sentence Transformers
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Testing**: Django TestCase (111 tests, 100% passing)

---

## 📦 Project Structure

```
Django/
├── .env                        # Environment variables (needs to be created)
├── .env.example                # Environment variable example
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
├── check_env.py               # Environment check script
├── ENV_SETUP.md               # Environment setup guide ⭐
├── MANUAL.md                  # User manual ⭐
├── venv/                      # Virtual environment
├── docs/                      # Documentation directory
│   └── schedule-mustupdate/
│       ├── report/           # Completion reports (11 files)
│       └── plan/
│           └── finish/       # Completed tasks (12 items)
└── mysite/                    # Django project
    ├── manage.py
    ├── db.sqlite3            # SQLite database
    ├── mysite/               # Project settings
    │   └── settings.py       # Integrated with environment variables
    └── polls/                # Main application
        ├── models.py         # 11 data models
        ├── views.py          # 50+ API endpoints
        ├── urls.py           # URL routing
        ├── api_utils.py      # API utility functions ⭐
        ├── tests*.py         # Test files (111 tests)
        └── templates/        # HTML templates
```

---

## 🧪 Testing

```bash
# Run all tests
cd mysite
python manage.py test polls

# Run specific tests
python manage.py test polls.tests_user_order -v 2
python manage.py test polls.tests_gpt_generate -v 2
python manage.py test polls.tests_sentence_similarity -v 2

# Parallel testing (faster)
python manage.py test polls --parallel
```

**Test Statistics**:
- Total Tests: 111
- Pass Rate: 100%
- Execution Time: ~3.8 seconds

---

## 🌐 API Endpoint Overview

### Authentication & Users
- `POST /polls/user/` - Create user
- `GET /polls/user/` - List all users
- `GET /polls/user/<id>/` - Get user details
- `PUT /polls/user/<id>/` - Update user
- `DELETE /polls/user/<id>/` - Delete user

### AI Services
- `POST /polls/generate-specification/` - Generate specification document
- `POST /polls/retry-ai/` - Retry AI generation
- `POST /polls/sentence-similarity/` - Semantic similarity analysis
- `POST /polls/gpt-generate/` - GPT text generation

### Configuration Management
- `GET/POST /polls/weight-config/` - Weight configuration
- `GET/POST /polls/field-priority/` - Field priority
- `GET/POST /polls/gpt-prompt/` - GPT Prompt configuration

**Complete API Documentation**: See [MANUAL.md](MANUAL.md#api-documentation)

---

## 🔑 API Key Setup

### Option 1: OpenAI API (Recommended)

1. Get API Key: https://platform.openai.com/api-keys
2. Edit `.env` file:
   ```bash
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   OPENAI_MODEL=gpt-4
   ```
3. Install package:
   ```bash
   pip install openai
   ```

### Option 2: Ollama Local LLM (Free)

1. Install Ollama:
   ```bash
   brew install ollama  # macOS
   ```
2. Download model and start service:
   ```bash
   ollama pull llama2
   ollama serve
   ```
3. Edit `.env` file:
   ```bash
   OLLAMA_API_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

**Detailed Setup**: See [ENV_SETUP.md](ENV_SETUP.md)

---

## 📝 Environment Variable Example

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# OpenAI API
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Ollama (optional)
OLLAMA_API_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Sentence Transformers
SENTENCE_TRANSFORMER_MODEL=paraphrase-MiniLM-L6-v2
```

For complete settings, refer to [.env.example](.env.example)

---

## 🎨 Frontend Pages

### Main Page
http://127.0.0.1:8000/polls/
- Specification generation form
- Real-time validation
- Loading animations
- Retry functionality

### Weight Configuration Management
http://127.0.0.1:8000/polls/weight-config-page/
- Visual weight editing
- Sum validation (100%)
- Ticket score calculator

### Field Priority Configuration
http://127.0.0.1:8000/polls/field-priority-page/
- Visual / JSON dual mode
- Drag-and-drop sorting
- Required/optional tags

### Admin Interface
http://127.0.0.1:8000/admin/
- Manage all data models
- Requires superuser account

---

## 🛠️ Development Tools

### Django Shell
```bash
python manage.py shell

# Test API
from polls.api_utils import test_openai_connection
success, message = test_openai_connection()
print(message)
```

### Environment Check
```bash
python check_env.py
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

---

## 🚨 Common Issues

### Q: Error when running tests?
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Test again
python manage.py test polls
```

### Q: OpenAI API returns 401 error?
Check if `OPENAI_API_KEY` in `.env` is set correctly.

### Q: Cannot find .env file?
```bash
cp .env.example .env
open .env  # Edit and fill in your API Key
```

### Q: How to reset the database?
```bash
rm db.sqlite3
rm -r polls/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

**More Questions**: See [MANUAL.md](MANUAL.md#faq)

---

## 📊 Project Statistics

- **Lines of Code**: ~10,000+
- **Data Models**: 11
- **API Endpoints**: 50+
- **Test Cases**: 111 (100% passing)
- **Frontend Pages**: 3
- **Completion Reports**: 11
- **Development Time**: Phase 1 fully executed

---

## 🎯 Next Steps

1. ✅ **Set Environment Variables** - See [ENV_SETUP.md](ENV_SETUP.md)
2. ✅ **Run Tests** - `python manage.py test polls`
3. ✅ **Start Server** - `python manage.py runserver`
4. ✅ **Browse Documentation** - Read [MANUAL.md](MANUAL.md)
5. 🚀 **Start Using** - Visit http://127.0.0.1:8000/polls/

---

## 📄 License

This project is for internal development.

---

## 📞 Contact Information

If you have any questions, please refer to:
- [User Manual](MANUAL.md)
- [Environment Setup Guide](ENV_SETUP.md)
- [Project Completion Summary](docs/schedule-mustupdate/report/PROJECT_COMPLETION_SUMMARY.md)

---

**Last Updated**: November 7, 2025
**Version**: v1.0.0
**Status**: ✅ Production Ready (API Key setup required)