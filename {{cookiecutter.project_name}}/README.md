# {{cookiecutter.project_name}} <!-- omit in toc -->



{{cookiecutter.app_description}}

A FastAPI application with dual authentication (API Keys + OAuth), role-based access control, and comprehensive testing.

<!-- Pytest Coverage Comment:Begin -->
<!-- Pytest Coverage Comment:End -->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation \& Run](#installation--run)
  - [Access Points](#access-points)
- [Authentication](#authentication)
  - [API Key Authentication](#api-key-authentication)
  - [OAuth 2.0 Authentication](#oauth-20-authentication)
    - [Provider Setup](#provider-setup)
    - [Environment Configuration](#environment-configuration)
    - [Testing OAuth Flow](#testing-oauth-flow)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Math Operations (Requires `admin` or `user` role)](#math-operations-requires-admin-or-user-role)
  - [OAuth Endpoints (No auth required)](#oauth-endpoints-no-auth-required)
- [Development](#development)
  - [Running Tests](#running-tests)
    - [Step 1: Add Business Logic](#step-1-add-business-logic)
    - [Step 2: Create Route](#step-2-create-route)
    - [Step 3: Add Tests](#step-3-add-tests)
  - [Environment Variables](#environment-variables)
- [Installation](#installation)
  - [From GitHub](#from-github)
  - [From Source](#from-source)
  - [In requirements.txt](#in-requirementstxt)
- [CI/CD](#cicd)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [Semantic Versioning](#semantic-versioning)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Features

**Core Capabilities**

- Dual authentication system: API Keys (SHA256 hashed) and OAuth 2.0 (GitHub/Google)
- Role-based access control with granular permissions
- Worker pattern for clean separation between routes and business logic
- Structured JSON logging with request tracking
- Comprehensive unit test suite with coverage reporting
- Built-in authentication test frontend supporting both OAuth and API key flows

**Developer Experience**

- Modern Python development with `pyproject.toml` and Pydantic Settings
- Automated CI/CD using GitHub Actions with semantic versioning
- Code quality enforcement via pre-commit hooks (ruff, isort)
- Automatic HTML coverage reports

## Quick Start

### Prerequisites

- Python 3.12+
- Git

### Installation & Run

```bash
# Clone repository
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run the server
python dev_server.py
```

### Access Points

- **Authentication Frontend**: http://localhost:8000/static/ (test both OAuth and API key methods)
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Authentication

### API Key Authentication

API keys are hashed with SHA256 for security and stored with user metadata.

<details>
<summary><b>Configuration</b></summary>

Base64-encoded JSON format stored in environment variables:

**Using the secrets_b64.py helper script:**

1. Create `src/{{cookiecutter.project_name}}/auth/secrets.json`:
```json
{
  "my_secret_key_123": {
    "username": "John Doe",
    "roles": ["admin", "user"]
  },
  "another_key_456": {
    "username": "Jane Smith",
    "roles": ["user"]
  }
}
```

2. Encode to base64:
```bash
python src/{{cookiecutter.project_name}}/auth/secrets_b64.py encode
```

3. Set in `.env`:
```bash
API_KEYS=<base64_output>
```

</details>

**Usage:**
```bash
curl "http://localhost:8000/math/add?A=10&B=5" \
  -H "Authorization: Bearer your_api_key_here"
```

### OAuth 2.0 Authentication

Supports GitHub (default) and Google OAuth providers.

#### Provider Setup

<details>
<summary><b>GitHub OAuth (Default)</b></summary>

1. Go to [GitHub Settings → Developer Settings](https://github.com/settings/developers)
2. Click **OAuth Apps** → **New OAuth App**
3. Fill in application details:
   - **Application name**: Your app name (e.g., "{{cookiecutter.project_name}}")
   - **Homepage URL**: `http://localhost:8000`
   - **Authorization callback URL**: `http://localhost:8000/static/callback.html`
4. Click **Register application**
5. Copy **Client ID** and generate **Client Secret**

</details>

<details>
<summary><b>Google OAuth</b></summary>

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Navigate to **APIs & Services** → **Credentials**
4. Create **OAuth 2.0 Client ID**
5. Configure OAuth consent screen
6. Set application details:
   - **Application type**: Web application
   - **Authorized JavaScript origins**: `http://localhost:8000`
   - **Authorized redirect URIs**: `http://localhost:8000/static/callback.html`
7. Copy **Client ID** and **Client Secret**

</details>

#### Environment Configuration

```bash
# Required
OAUTH_CLIENT_ID="your_client_id"
OAUTH_CLIENT_SECRET="your_client_secret"
OAUTH_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"

# Optional - defaults to "github"
OAUTH_PROVIDER="github"  # or "google"
```

#### Testing OAuth Flow

**Quick Test:** Visit http://localhost:8000/static/ → Login with provider → test endpoints

<details>
<summary><b>Detailed Testing Instructions</b></summary>

**Web interface (recommended):**
1. Start server: `python dev_server.py`
2. Visit: http://localhost:8000/static/
3. Choose authentication method:
   - **OAuth Login**: Click "Login with [Provider]" → authorize → automatic token handling
   - **API Key**: Click "API Key" tab → enter your key → click "Set API Key"
4. Test protected endpoints using the math operation form

Both authentication methods provide access to the same endpoints. Your choice is persisted in the browser.

**Manual cURL flow:**
```bash
# 1. Get authorization URL
curl -X POST "http://localhost:8000/auth/oauth/authorize" \
  -H "Content-Type: application/json" \
  -d '{"redirect_uri": "http://localhost:8000/static/callback.html"}'

# 2. Visit the returned URL in browser and authorize

# 3. Exchange code for token
curl -X POST "http://localhost:8000/auth/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "<authorization_code>",
    "redirect_uri": "http://localhost:8000/static/callback.html"
  }'

# 4. Use the access token
curl "http://localhost:8000/math/add?A=10&B=5" \
  -H "Authorization: Bearer <access_token>"
```

</details>

## Project Structure

```
{{cookiecutter.project_name}}/
├── src/{{cookiecutter.project_name}}/
│   ├── auth/
│   │   ├── dependencies.py          # Unified auth dependency factory
│   │   ├── oauth_auth.py            # OAuth token management
│   │   └── oauth_providers.py       # OAuth provider configurations
│   ├── routers/
│   │   ├── math.py                  # Math operations (protected)
│   │   └── oauth.py                 # OAuth flow endpoints
│   ├── workers/
│   │   ├── math_operations.py       # Business logic layer
│   │   └── oauth_service.py         # OAuth service layer
│   ├── models/
│   │   ├── input.py                 # Request/response models
│   │   └── oauth.py                 # OAuth models
│   ├── utils/
│   │   └── auth_utils.py            # Hashing utilities
│   ├── static/                      # Authentication test frontend
│   │   ├── index.html               # Main test page (OAuth + API Key)
│   │   └── callback.html            # OAuth callback handler
│   ├── custom_logger/               # Logging configuration
│   ├── main.py                      # FastAPI app entry point
│   └── settings.py                  # Pydantic settings
├── tests/
│   ├── conftest.py                  # Pytest fixtures
│   └── unit/                        # Unit tests
└── pyproject.toml                   # Project metadata
```

## API Endpoints

### Math Operations (Requires `admin` or `user` role)

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/math/add` | GET | Add two numbers | `?A=10&B=5` → `{"result": 15}` |
| `/math/subtract` | GET | Subtract B from A | `?A=10&B=5` → `{"result": 5}` |
| `/math/multiply` | GET | Multiply two numbers | `?A=7&B=6` → `{"result": 42}` |
| `/math/divide` | GET | Divide A by B | `?A=10&B=2` → `{"result": 5}` |

Example request:
```bash
curl "http://localhost:8000/math/multiply?A=7&B=6" \
  -H "Authorization: Bearer your_api_key"
```

Response:
```json
{
  "operation": "multiply",
  "a": 7,
  "b": 6,
  "result": 42
}
```

### OAuth Endpoints (No auth required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/oauth/provider` | GET | Get configured OAuth provider name |
| `/auth/oauth/authorize` | POST | Get authorization URL for OAuth flow |
| `/auth/oauth/token` | POST | Exchange authorization code for JWT token |

## Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov={{cookiecutter.project_name}} --cov-report=html

# Specific test file
pytest tests/unit/test_workers.py

# Verbose output
pytest -v
```

<details>
<summary><b>Adding New Features</b></summary>

#### Step 1: Add Business Logic

```python
# src/{{cookiecutter.project_name}}/workers/math_operations.py
def power_numbers(a: float, b: float) -> float:
    """Raise a to the power of b."""
    return a ** b
```

#### Step 2: Create Route

```python
# src/{{cookiecutter.project_name}}/routers/math.py
from {{cookiecutter.project_name}}.workers.math_operations import power_numbers
from {{cookiecutter.project_name}}.models.input import InputData

@math_router.post("/power")
def power(input_data: InputData) -> dict:
    result = power_numbers(input_data.A, input_data.B)
    return {
        "operation": "power",
        "a": input_data.A,
        "b": input_data.B,
        "result": result
    }
```

#### Step 3: Add Tests

```python
# tests/unit/test_workers.py
from {{cookiecutter.project_name}}.workers.math_operations import power_numbers

def test_power_numbers():
    assert power_numbers(2, 3) == 8
    assert power_numbers(10, 2) == 100
```

</details>

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys (base64-encoded JSON)
API_KEYS="eyJ0ZXN0Ijp7InVzZXJuYW1lIjoiSm9uYXRoYW4iLCJyb2xlcyI6WyJhZG1pbiIsInVzZXIiXX19"

# OAuth Configuration
OAUTH_PROVIDER="github"
OAUTH_CLIENT_ID="your_client_id"
OAUTH_CLIENT_SECRET="your_client_secret"
OAUTH_SECRET_KEY="your-32-char-secret-key"

# Application Settings
APP_NAME="{{cookiecutter.project_name}}"
DESCRIPTION="{{cookiecutter.app_description}}"

# Logger Settings
LOG_LEVEL_CONSOLE="INFO"
LOG_LEVEL_FILE="DEBUG"
```

## Installation

### From GitHub

```bash
pip install "git+https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}.git@v1.0.0"
```

### From Source

```bash
git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}.git
cd {{cookiecutter.project_name}}
pip install -e ".[dev]"
```

### In requirements.txt

```txt
{{cookiecutter.project_name}} @ git+https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.project_name}}.git@v1.0.0
```

## CI/CD

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

<details>
<summary><b>Configured Checks</b></summary>

- Code formatting (ruff)
- Import sorting (isort)
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON syntax validation
- Case conflict detection
- Merge conflict detection
- Private key detection
- Prevent commits to main branch

**Run manually:**
```bash
pre-commit run --all-files
```

</details>

### Semantic Versioning

Automated releases based on commit messages:

| Commit Type | Version Change | Example |
|-------------|----------------|---------|
| `fix:` | Patch (1.0.0 → 1.0.1) | `fix: correct calculation error` |
| `feat:` | Minor (1.0.0 → 1.1.0) | `feat: add power operation` |
| `BREAKING CHANGE:` | Major (1.0.0 → 2.0.0) | `feat: redesign API`<br>`BREAKING CHANGE: removed old endpoints` |

## Usage Examples

<details>
<summary><b>Python requests</b></summary>

```python
import requests

url = "http://localhost:8000/math/add"
headers = {"Authorization": "Bearer your_api_key"}
params = {"A": 10, "B": 5}

response = requests.get(url, params=params, headers=headers)
print(response.json())
# Output: {"operation": "add", "a": 10, "b": 5, "result": 15}
```

</details>

<details>
<summary><b>JavaScript fetch</b></summary>

```javascript
const response = await fetch('http://localhost:8000/math/add?A=10&B=5', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer your_api_key'
  }
});

const data = await response.json();
console.log(data);
// Output: {operation: "add", a: 10, b: 5, result: 15}
```

</details>

<details>
<summary><b>Error Handling</b></summary>

**Invalid authentication:**
```bash
curl "http://localhost:8000/math/add?A=10&B=5" \
  -H "Authorization: Bearer invalid_key"

# Response: 307 Redirect to /static/
```

**Insufficient permissions:**
```bash
curl "http://localhost:8000/math/add?A=10&B=5" \
  -H "Authorization: Bearer user_without_role"

# Response: {"detail": "User does not have required role"}
# Status: 403 Forbidden
```

**Invalid input:**
```bash
curl "http://localhost:8000/math/add?A=not_a_number&B=5" \
  -H "Authorization: Bearer your_api_key"

# Response: {"detail": [{"type": "float_parsing", "loc": ["query", "A"], ...}]}
# Status: 422 Unprocessable Entity
```

</details>

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## Author

{{cookiecutter.my_name}}

---

