# 📊 Academic Indicators Control

This project automates the monitoring of academic report submissions from teachers.  
It connects to **Google Drive** and **Google Sheets** APIs to check if documents are completed on time, and it notifies you via **WhatsApp** using **Twilio API**.

---

## ✨ Features

- 🔑 **Secure authentication** with **OAuth 2.0** (`credentials.json` + `token.json`).
- ✅ Connects securely to Google Drive & Google Sheets
- 📂 **Google Drive access** to locate and open files.
- 📑 **Google Sheets reading** to validate column completeness.
- 📅 Automatically checks columns by month (e.g., January → column 1, February → column 2)
- ⏰ **Automatic checks** during the last 3 working days of each month.
- 📢 Sends WhatsApp notifications if data is missing
- ⏰ Runs automatically on the last 3 business days of the month
- 🔒 Uses OAuth2 with `credentials.json` and generates `token.json` for access

---

## 📂 Project Structure

```bash
📦 Project
 ┣ 📜 Control02.py       # Main script (check + notify)
 ┣ 📜 auth_utils.py      # Authentication and token handling
 ┣ 📜 credentials.json   # Google Cloud credentials
 ┣ 📜 token.json         # Generated token after first login
 ┣ 📂 data/              # (optional) for logs or reports
```

---

## 🛠️ Tech Stack

- **Python 3.12+**
- [Google API Client](https://developers.google.com/drive/api/quickstart/python)
- [Google OAuthlib](https://pypi.org/project/google-auth-oauthlib/)
- [Twilio API for WhatsApp](https://www.twilio.com/whatsapp)

---

## ⚙️ Installation

### 1. Clone this repository

git clone https://github.com/yourusername/academic-indicators-control.git
cd academic-indicators-control

### 2. Install dependencies

pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib twilio

---

## 🔑 Configuration

### Google Cloud Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **Google Drive API** and **Google Sheets API**.
3. Create OAuth 2.0 credentials and download the file `credentials.json`.
4. Place it in the project root folder.

### Twilio Setup

1. Create an account on [Twilio](https://www.twilio.com/).
2. Enable **WhatsApp Sandbox**.
3. Copy your `ACCOUNT_SID` and `AUTH_TOKEN`.
4. Replace them in `chaty.py`.

---

## ▶️ Usage

Run the script:

python generarToken.py

- On the first run, a browser window will open asking you to log in with your Google account and grant permissions.
- This generates a `token.json` file that will be reused in future executions.

---

## 📅 Automatic Execution

You can schedule the script to run automatically on the **last 3 business days of each month**:

### On Windows (Task Scheduler)

1. Open **Task Scheduler**.
2. Create a new task.
3. Set the trigger for the last 3 days of the month.
4. Set the action to run:

python C:\path\to\Control02.py

---

## 📲 WhatsApp Notifications

Example notification message:

⚠️ Alert: Missing academic report in February!
Please check the file in Google Drive.

---

## 📸 Preview

<!--
![Google Drive ](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7S0s4DzQ2SF5WoLZWkKZdEDd-lGX-7PzECBZ63hXVFu0SNTvjPS576OIJrt9Veh0Y230&usqp=CAU)
)
-->

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7S0s4DzQ2SF5WoLZWkKZdEDd-lGX-7PzECBZ63hXVFu0SNTvjPS576OIJrt9Veh0Y230&usqp=CAU" alt="Google Drive" width= 200px height= 200px>

<img src="https://w7.pngwing.com/pngs/172/286/png-transparent-twilio-hd-logo.png" alt="Twilio WhatsApp" width= 200px >

---

## 🔄 Process Flow

```
😎
mermaid
flowchart TD

    A[⏰ Scheduler (last 3 business days of the month)] --> B[🐍 Python Script]

    B --> C[🔑 OAuth 2.0 Login with credentials.json]
    C --> D[📂 Google Drive API]
    C --> E[📑 Google Sheets API]

    D --> F[📄 Locate the file in the right folder]
    E --> G[📊 Check the correct column depending on month]

    G -->|All cells complete ✅| H[✔ Everything OK]
    G -->|Missing cells ❌| I[📲 Twilio API]

    I --> J[💬 WhatsApp Notification Sent]

```

---

# 👩‍💻 Author

Laura Estefanía Grajeda Cardiel
🚀 Personal project to automate academic indicator tracking with intelligent notifications.
