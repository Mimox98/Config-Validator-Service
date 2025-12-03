# Config Validator Service

A lightweight Python service that validates JSON and YAML configuration files, packaged in Docker and automated with Jenkins CI/CD.

## 🎯 Purpose

This project demonstrates how to:
- Package a Python tool in Docker for consistent execution across environments
- Automate validation checks with Jenkins pipelines
- Provide a reusable template for internal developer tools
- Improve developer productivity by catching config errors early

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI service:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Run tests:**
   ```bash
   pytest app/tests/ -v
   ```

### Docker

1. **Build the image:**
   ```bash
   docker build -t config-validator:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 config-validator:latest
   ```

3. **Test the API:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/validate-files
   ```

### Jenkins Pipeline

The `Jenkinsfile` defines a complete CI/CD pipeline:
1. **Checkout** - Get source code
2. **Build** - Create Docker image
3. **Test** - Run pytest unit tests
4. **Validate** - Check all config files in `configs/`
5. **Tag & Push** - Publish to Docker registry (optional)

## 📁 Project Structure

```
config-validator/
├── app/
│   ├── main.py              # FastAPI application
│   ├── api/routes.py        # API endpoints
│   ├── core/validator.py    # Validation logic
│   └── tests/test_validator.py
├── configs/
│   ├── example_config.json
│   └── example_config.yaml
├── Dockerfile
├── requirements.txt
├── Jenkinsfile
└── quarto/                  # Documentation
```

## 🔍 API Endpoints

- `GET /health` - Health check
- `POST /validate` - Validate config content
- `GET /validate-files` - Validate all configs in `configs/` directory

## 📋 Configuration Rules

Valid configurations must:
- Be valid JSON or YAML syntax
- Include required keys: `name`, `version`, `environment`
- Have `environment` as one of: `development`, `staging`, `production`
- Have `version` as a non-empty string

## 🎓 Interview Demo Points

1. **Docker containerization** - Show how the Dockerfile creates a consistent environment
2. **Jenkins automation** - Walk through the pipeline stages and their purpose
3. **Python best practices** - Clean structure, type hints, unit tests
4. **Reusability** - Explain how teams can copy this template for other tools
5. **Documentation** - Reference the Quarto site for onboarding new developers

## 📚 Documentation

Full documentation available in the `quarto/` directory:
- Overview and problem statement
- Pipeline architecture and stages
- Docker environment benefits
- How to reuse this template

## 🛠️ Technologies

- **Python 3.11** with FastAPI
- **Docker** for containerization
- **Jenkins** for CI/CD automation
- **pytest** for unit testing
- **Quarto** for documentation

## 📝 License

MIT License - feel free to use this as a template for your own projects.