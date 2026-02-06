# fastapi_template
A cookiecutter template for FastAPI applications with modern CI/CD setup.

## Features
* FastAPI application with dual authentication (API Keys + OAuth 2.0)
* Role-based access control with granular permissions
* Worker pattern for clean separation between routes and business logic
* Structured JSON logging with request tracking
* Automated testing on PR using GitHub Actions
* Pre-commit hooks for code quality (ruff, isort, trailing whitespace, etc.)
* Semantic release using GitHub Actions
* Automatic code coverage report in README
* Automatic wheel build and GitHub Release publishing
* Modern Python packaging with pyproject.toml
* OAuth testing frontend included

*Notes*
Workflows trigger when a branch is merged into main!
To install, please follow all the instructions in this readme.
The workflows require a PAT set as secret (see GitHub Repository Setup section for instructions).
See the notes on how to create semantic releases at the bottom of the README.

If you followed all the steps, whenever a PR is merged into `main`, the workflows are triggered and should:
* Run pre-commit checks (fail fast on code quality issues)
* Ensure that tests pass (before merge)
* Create a code coverage report and commit that to the bottom of the README
* Create a semantic release (if you follow the semantic release pattern) and automatically update the version number of your code
* Build a wheel and publish it as a GitHub Release asset


# Install
Cookiecutter template:
* Cd to your new FastAPI application location
  * `cd /your/new/application/path/`
* Install cookiecutter using pip
  * `pip install cookiecutter`
* Run the cookiecutter template from this GitHub repo
  * `cookiecutter https://github.com/YOUR_USERNAME/fastapi_template`
* Fill in your new application values (including your GitHub username for CODEOWNERS)
* Create new virtual environment
  *  `python -m venv .venv`
* Activate the environment and install application with dev dependencies
  *  `pip install -e ".[dev]"`
* Install pre-commit hooks
  * `pip install pre-commit`
  * `pre-commit install`
* **Run pre-commit on all files** (important for initial commit!)
  * `pre-commit run --all-files`
* Copy the .env.example file to .env and configure your settings
  * `cp .env.example .env`
* Check proper install by running tests
  * `pytest`

## Turn the new local cookiecutter code into a git repo

Open git bash
```bash
cd C:/your/code/directory
```
To init the repository, add all files and commit
```bash
git init
git add *
git add .github
git add .gitignore
git add .pre-commit-config.yaml
git add .env.example
git commit -m "fix: Initial commit"
```

To add the new git repository to your GitHub:
*  Go to [github](https://github.com/).
-  Log in to your account.
-  Click the [new repository](https://github.com/new) button in the top-right. You'll have an option there to initialize the repository with a README file, but don't. Leave the repo empty
- Give the new repo the same name you gave your repo with the cookiecutter
-  Click the "Create repository" button.

Now we want to make sure we are using `main` as main branch name and push the code to GitHub
```bash
git remote add origin https://github.com/username/new_repo_name.git
git branch -M main
git push -u origin main
```

---

# 🔒 GitHub Repository Setup

Complete these steps in order to enable the CI/CD pipeline.

## Step 1: Create the Release Token (PAT)

The workflow needs a Personal Access Token to push to the protected `main` branch.

### Create a Fine-Grained PAT (Recommended - More Secure)

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens](https://github.com/settings/tokens?type=beta)
2. Click **"Generate new token"**
3. Configure the token:
   - **Token name:** `RELEASE_TOKEN_YOUR_REPO_NAME`
   - **Expiration:** Choose an appropriate duration (recommend 90 days, set a reminder to rotate)
   - **Repository access:** Select "Only select repositories" → choose your repository
   - **Permissions:**
     - **Contents:** Read and write (for pushing commits and tags)
     - **Metadata:** Read-only (automatically selected)
4. Click **"Generate token"**
5. **Copy the token immediately** - you won't see it again!

## Step 2: Add the Token as a Repository Secret

1. Go to your repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Configure:
   - **Name:** `RELEASE_TOKEN`
   - **Secret:** Paste your copied PAT

5. Click **"Add secret"**

## Step 3: Configure Branch Protection with Rulesets

GitHub Rulesets provide modern, flexible branch protection. The PAT allows the workflow to bypass these rules while humans must go through PRs.

1. Go to your repository → **Settings → Rules → Rulesets**
2. Click **"New ruleset"** → **"New branch ruleset"**
3. Configure the ruleset:
   - **Ruleset name:** `Protect main`
   - **Enforcement status:** Active
   - **Target branches:** Click "Add target" → "Include by pattern" → enter `main`

4. Enable these rules:
   - ✅ **Restrict deletions** - Prevent branch deletion
   - ✅ **Require a pull request before merging**
     - Required approvals: `1` (or more)
     - ✅ Dismiss stale pull request approvals when new commits are pushed
     - ✅ Require conversation resolution before merging
   - ✅ **Require status checks to pass**
     - ✅ Require branches to be up to date before merging
     - Add status checks: `Run Pre-commit Checks`  & `Run Tests and Lint`
   - ✅ **Block force pushes**

5. Click **"Create"**

## Security Model

This setup provides security through multiple layers:

| Protection | What it prevents |
|------------|------------------|
| **CODEOWNERS** | Requires your approval for any workflow changes |
| **Required PRs** | No direct pushes to main (humans must use PRs) |
| **Required reviews** | At least one approval needed for every change |
| **Status checks** | Tests must pass before merge |
| **PAT as secret** | Token only accessible to workflows, not forks |

**Why is the PAT safe?**
- The PAT is stored as a secret, never exposed in logs (GitHub auto-masks it)
- Forks cannot access repository secrets
- Any attempt to modify workflows to steal the PAT requires your explicit approval via CODEOWNERS
- The PAT can only push; it cannot change branch protection rules

---

# Semantic Release
https://python-semantic-release.readthedocs.io/en/latest/

The workflows are triggered when you merge into main!

When committing use the following format for your commit message:
* **patch** (0.0.X):
  ```
  fix: commit message
  ```
* **minor** (0.X.0):
  ```
  feat: commit message
  ```
* **major/breaking** (X.0.0) - add the breaking change on the third line:
  ```
  feat: commit message

  BREAKING CHANGE: description of breaking change
  ```

---

# Installation Options (for generated applications)
Applications created with this template support multiple installation methods:
Note that the @v1.0.0 can be updated for a specific version, or removed for the newest version

### Configure git credentials (more secure, recommended)
This method doesn't expose your token in command history:

```bash
# Store credentials in git (one-time setup)
git config --global credential.helper store

# Then install normally - git will prompt for credentials once
pip install "git+https://github.com/username/repo_name.git@v1.1.0"
# When prompted: username = your GitHub username, password = your PAT
```

### Option 1: Install from Private GitHub Release (Recommended)
```bash
# Using pip with a personal access token
pip install "git+https://YOUR_TOKEN@github.com/username/repo_name.git@v1.0.0"

# Using uv
uv pip install "git+https://YOUR_TOKEN@github.com/username/repo_name.git@v1.0.0"
```

### Option 2: Install from Wheel File in Repository
After cloning, install the wheel file from the `dist/` directory:
```bash
pip install repo_name/dist/repo_name-1.0.0-py3-none-any.whl
```

### Option 3: Install from Source (Clone Repository)
```bash
git clone https://github.com/username/repo_name.git
cd repo_name
pip install -e ".[dev]"
```

### Option 4: Building a Wheel File Locally
```bash
pip install build
python -m build --wheel
# The wheel will be created in the dist/ directory
```

### Option 5: Add to requirements.txt or pyproject.toml

**In requirements.txt:**

```txt
# Using git+https (requires GH_TOKEN environment variable to be set)
repo_name @ git+https://github.com/username/repo_name.git@v1.1.0
```

**In pyproject.toml (for projects using PEP 621):**

```toml
[project]
dependencies = [
    "repo_name @ git+https://github.com/username/repo_name.git@v1.1.0",
]
```

> **Note:** When installing from requirements.txt with a private repo, ensure your git credentials are configured (see Option 1 above)
