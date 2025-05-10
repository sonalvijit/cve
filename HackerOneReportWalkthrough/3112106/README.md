# PoC for HackerOne Report #3112106: Bypassing Chatbot Restrictions

This repository contains a Proof of Concept (PoC) for the vulnerability reported in HackerOne report #3112106, titled "BAC – Bypass chatbot restrictions via unauthorized mention injection." The vulnerability allows a member user to bypass admin-imposed restrictions on the Dust platform's Gemini chatbot by manipulating API request parameters.

## Vulnerability Overview

- **Report ID**: #3112106
- **Title**: BAC – Bypass chatbot restrictions via unauthorized mention injection
- **Platform**: Dust
- **Severity**: Medium (CVSS 5.4)
- **Weakness**: Broken Access Control (BAC)
- **Reported by**: yoyomiski
- **Reported on**: April 25, 2025
- **Resolved on**: May 6, 2025
- **Description**: A member user without permission to access the Gemini chatbot can bypass restrictions by editing the `mention` and `configurationId` fields in a POST request to the `/api/w/.../edit` endpoint. This allows unauthorized interaction with the disabled chatbot, violating admin access controls.

## Repository Contents

- **`chatbot_app_sqlalchemy.py`**: A Flask application that simulates the vulnerable Dust platform, including a vulnerable endpoint (`/api/assistant/conversations/<conv_id>/messages/<msg_id>/edit`) and a fixed endpoint (`/edit_fixed`). It uses Flask-SQLAlchemy for database management.
- **`exploit.py`**: A Python script using the `requests` library to demonstrate the vulnerability by sending HTTP requests to the Flask app, mimicking the report’s exploitation steps.
- **`README.md`**: This file, providing setup and usage instructions.

## Prerequisites

- **Python**: Version 3.8 or higher
- **Dependencies**:
  - Flask (`flask`)
  - Flask-SQLAlchemy (`flask_sqlalchemy`)
  - Requests (`requests`)
- **Operating System**: Tested on Windows 10; should work on Linux/macOS with minor adjustments.
- **Tools**: Command-line interface (e.g., PowerShell, Terminal), `curl` (optional for manual testing).

## Setup Instructions

1. **Clone or Download the Repository**:
   - Download the files (`chatbot_app_sqlalchemy.py`, `exploit.py`, `README.md`) to a local directory, e.g., `C:\Users\YourUser\Desktop\HackerOne-3112106`.

2. **Install Dependencies**:
   - Open a terminal in the directory and install the required Python packages:
     ```bash
     pip install flask flask_sqlalchemy requests
     ```

3. **Verify Files**:
   - Ensure `chatbot_app_sqlalchemy.py` and `exploit.py` are in the directory.
   - The Flask app simulates the Dust platform with an in-memory SQLite database.
   - The PoC script sends HTTP requests to `http://localhost:5000`.

## Running the Flask Application

1. **Start the Flask Server**:
   - Navigate to the directory:
     ```bash
     cd C:\Users\YourUser\Desktop\HackerOne-3112106
     ```
   - Run the Flask application:
     ```bash
     python chatbot_app_sqlalchemy.py
     ```
   - Expected output:
     ```
      * Serving Flask app 'chatbot_app_sqlalchemy'
      * Debug mode: on
      * Running on http://0.0.0.0:5000
     ```
   - The server will listen on `http://localhost:5000`.

2. **Verify Server Accessibility**:
   - Test the admin endpoint manually using `curl` or a browser (via Postman or similar):
     ```bash
     curl -H "Authorization: admin" http://localhost:5000/api/manage_agents
     ```
   - Expected response:
     ```json
     [
         {
             "id": 1,
             "name": "Gemini",
             "configurationId": "gemini-pro",
             "enabled": false
         },
         {
             "id": 2,
             "name": "Default",
             "configurationId": "default-agent",
             "enabled": true
         }
     ]
     ```
   - If the server is inaccessible, check for port conflicts (see Troubleshooting).

## Running the PoC Script

1. **Execute the PoC**:
   - With the Flask server running, open a new terminal in the same directory.
   - Run the PoC script:
     ```bash
     python exploit.py
     ```
   - The script performs three steps:
     - **Step 1**: Checks agent status as an admin, confirming `Gemini` is disabled.
     - **Step 2**: Tests the vulnerable endpoint as a member, attempting to bypass restrictions.
     - **Step 3**: Tests the fixed endpoint, verifying that access is blocked.

2. **Expected Output**:
   ```
   === PoC: Bypassing Chatbot Restrictions ===

   Step 1: Checking agent status as admin
   Admin - Agent Status:
   [
     {
       "id": 1,
       "name": "Gemini",
       "configurationId": "gemini-pro",
       "enabled": false
     },
     {
       "id": 2,
       "name": "Default",
       "configurationId": "default-agent",
       "enabled": true
     }
   ]

   Step 2: Testing vulnerable endpoint as member
   Vulnerable Endpoint Test:
   Status Code: 200
   Response: {
     "message": "Response from Gemini: Hello! You reached gemini-pro."
   }
   Success: Bypassed restrictions! Member accessed disabled Gemini agent.

   Step 3: Testing fixed endpoint as member
   Fixed Endpoint Test:
   Status Code: 403
   Response: {
     "error": {
       "type": "invalid_request_error",
       "message": "This agent is either disabled or you don't have access to it."
     }
   }
   Success: Fixed endpoint blocked access to disabled Gemini agent.
   ```

## How the PoC Works

- **Flask Application**:
  - Simulates the Dust platform with a vulnerable endpoint that allows a member user to access the disabled `Gemini` agent by specifying its `configurationId` (`gemini-pro`) in a POST request.
  - The fixed endpoint enforces server-side validation, blocking access to disabled agents.
  - An admin endpoint (`/api/manage_agents`) allows viewing and updating agent status.

- **PoC Script**:
  - Sends a GET request to `/api/manage_agents` to verify `Gemini` is disabled.
  - Sends a POST request to the vulnerable endpoint (`/api/assistant/conversations/123/messages/456/edit`) with a manipulated payload, demonstrating the bypass.
  - Sends the same POST request to the fixed endpoint (`/edit_fixed`), confirming the fix prevents unauthorized access.

## Troubleshooting

1. **Connection Error: "No connection could be made"**:
   - **Cause**: The Flask server is not running or is inaccessible on `http://localhost:5000`.
   - **Fix**:
     - Ensure the Flask server is running (`python chatbot_app_sqlalchemy.py`).
     - Check for port conflicts:
       ```bash
       netstat -aon | findstr :5000
       ```
     - If port `5000` is in use, change the port in `chatbot_app_sqlalchemy.py` (e.g., `app.run(host="0.0.0.0", port=5001)`) and update `BASE_URL` in `exploit.py`:
       ```python
       BASE_URL = "http://localhost:5001"
       ```
     - Verify firewall settings allow connections to port `5000`.

2. **Module Not Found Error**:
   - **Cause**: Missing dependencies.
   - **Fix**: Install required packages:
     ```bash
     pip install flask flask_sqlalchemy requests
     ```

3. **Unexpected Response from Server**:
   - **Cause**: Mismatched endpoints or server state.
   - **Fix**:
     - Confirm `exploit.py` uses the correct `BASE_URL` and endpoint paths.
     - Restart the Flask server to reset the in-memory database.

4. **Windows-Specific Issues**:
   - If using WSL or a virtual environment, ensure `localhost` resolves correctly. Try `127.0.0.1` in `BASE_URL`:
     ```python
     BASE_URL = "http://127.0.0.1:5000"
     ```

## Additional Notes

- **Security Warning**: This PoC is for educational purposes only. Do not use it against production systems without permission.
- **Limitations**:
  - The Flask app uses simplified authentication (header-based) to focus on the vulnerability.
  - The PoC assumes `Gemini` is disabled by default, as per the report.
- **Extending the PoC**:
  - Add JWT-based authentication for realism.
  - Test additional `configurationId` values or payloads.
  - Log requests/responses for detailed analysis.

## References

- **HackerOne Report**: [Report #3112106](https://hackerone.com/reports/3112106) (requires access)
- **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Flask-SQLAlchemy**: [flask-sqlalchemy.palletsprojects.com](https://flask-sqlalchemy.palletsprojects.com)
- **Requests Library**: [requests.readthedocs.io](https://requests.readthedocs.io)

For issues or questions, contact the repository maintainer or refer to the HackerOne report for context.