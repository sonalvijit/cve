# CVE Walkthrough

## INTRO

Practicing Infamous CVE Walkthroughs via Docker Containers. By this, learners and security researchers can safely study how these vulnerabilities were exploited in real-world scenarios without risking their host machines.

This repository contains walkthroughs and simulations for various CVEs (Common Vulnerabilities and Exposures). Each folder represents a specific CVE and includes relevant files for understanding, exploiting, and mitigating the vulnerability.

## Folder Structure

- **[CVE-2023-26115](CVE-2023-26115/)**  
  A Node.js application vulnerable to issues in the `word-wrap` package. Includes:
  - `Dockerfile` for containerization.
  - `app/` folder with application code and dependencies (`package.json`).

- **[CVE-2023-3817](CVE-2023-3817/)**  
  A Flask application demonstrating HTTP request handling. Includes:
  - `app.py` for the vulnerable application.
  - `docker-compose.yml` and `Dockerfile` for deployment.

- **[CVE-2024-2383](CVE-2024-2383/)**  
  A simulation of a clickjacking vulnerability. Includes:
  - `attacker/` and `victim/` folders for simulating an attack scenario.
  - `docker-compose.yml` for orchestration.

- **[CVE-2024-28756](CVE-2024-28756/)**  
  A Python application with potential security issues. Includes:
  - `app.py` and `attack.py` for exploitation.
  - `Dockerfile` for containerization.

- **[CVE-2024-30126](CVE-2024-30126/)**  
  Demonstrates security headers to prevent clickjacking. Includes:
  - `victim/app.py` for the vulnerable application.
  - `attacker/Dockerfile` for simulating an attacker.

- **[CVE-2025-0108](CVE-2025-0108/)**  
  A basic PHP application. Includes:
  - `src/index.php` for the vulnerable endpoint.

- **[CVE-2025-1509](CVE-2025-1509/)**  
  A WordPress setup with potential vulnerabilities. Includes:
  - `docker-compose.yml` for deployment.

- **[CVE-2025-20116](CVE-2025-20116/)**  
  Demonstrates a stored XSS vulnerability in a Flask application. Includes:
  - `app.py` for the vulnerable application.
  - `templates/index.html` for the frontend.

- **[CVE-2025-21526](CVE-2025-21526/)**  
  Simulates unauthorized access in a Flask application. Includes:
  - `app.py` and `exploit.py` for exploitation.
  - `docker-compose.yml` and `README.md` for setup and usage.

- **[CVE-2025-22145](CVE-2025-22145/)**  
  A PHP application with potential vulnerabilities. Includes:
  - `docker-compose.yml` and `composer.json` for setup.

- **[CVE-2025-22508](CVE-2025-22508/)**  
  A PHP application with potential issues. Includes:
  - `docker-compose.yml` and `composer.json` for setup.

- **[CVE-2025-22599](CVE-2025-22599/)**  
  Demonstrates a reflected XSS vulnerability. Includes:
  - `README.md` with exploit details.

- **[CVE-2025-22656](CVE-2025-22656/)**  
  A WordPress plugin vulnerability in Akismet. Includes:
  - Plugin files (`class.akismet-admin.php`, `LICENSE.txt`, etc.).
  - `README.md` with exploit details.

- **[CVE-2025-26264](CVE-2025-26264/)**  
  A Flask application with potential issues. Includes:
  - `requirements.txt` for dependencies.

- **[CVE-2025-28010](CVE-2025-28010/)**  
  A Dockerized application. Includes:
  - `build.sh` for building and running the application.

## Usage

1. Navigate to the folder of the CVE you want to explore.
2. Follow the instructions in the `README.md` or relevant files within the folder.
3. Use Docker or other tools as specified to simulate and analyze the vulnerability.

## Disclaimer

This repository is for **educational purposes only**. Do not use these simulations on production systems or without proper authorization.
