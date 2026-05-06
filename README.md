# OTCPulse

A campus community platform for Ozarks Technical Community College.

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/sgravesOTC/Hack2Gether.git
cd Hack2Gether
```

**2. Create and activate a virtual environment**

macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> If PowerShell blocks the script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first.

**3. Install dependencies**
```bash
pip install -r otc_engage/requirements.txt
```

**4. Apply migrations**
```bash
cd otc_engage
python3 manage.py migrate
```

**5. Create a superuser**
```bash
python3 manage.py createsuperuser
```

**6. Run the development server**
```bash
python3 manage.py runserver
```

The app will be available at `http://127.0.0.1:8000`


---

## User Guide

### Table of Contents
- [Getting Started](#getting-started)
- [Account & Profile](#account--profile)
- [Dashboard](#dashboard)
- [Clubs](#clubs)
    - [Browsing Clubs](#browsing-clubs)
    - [Joining a Club](#joining-a-club)
    - [Creating a Club](#creating-a-club)
    - [Club Officers & Faculty Advisors](#club-officers--faculty-advisors)
- [Events](#events)
    - [Viewing Events](#viewing-events)
    - [Creating an Event](#creating-an-event)
    - [Attending an Event (QR Check-in)](#attending-an-event-qr-check-in)
    - [Event Surveys](#event-surveys)
    - [Exporting Attendance](#exporting-attendance)
- [Leaderboard](#leaderboard)
- [Bulletin Board](#bulletin-board)
    - [Submitting a Request](#submitting-a-request)
    - [Reserving a Space](#reserving-a-space)
- [Admin Features](#admin-features)

---

### Getting Started

When you first visit OTCPulse, you will land on the home page. You'll see two buttons that give you the option to either "Login" or "Get Started".

![Home Page](docs/images/00-home.png)

#### Login

If you already have an account you can log in.

![Login Page](docs/images/01-login.png)

---

### Account & Profile

#### Registering

Click **Get Started** to go to the registration form where you'll be prompted to fill out a form. The form requires you enter an email ending in @otc.edu, among other things that will be validated automatically.

![Registration Form](docs/images/02-register.png)

#### Your Profile

Once Logged in, you can visit your profile by clicking on your name or avatar in the navigation bar. From here you can:

- Update your display name and profile picture
- Change your password
- View your personal QR code (used for event check-in)

![Profile Page](docs/images/03-profile.png)

#### Your QR Code

Every account has a unique QR code. Event organizers scan this code at the door to record your attendance and award points.

![Personal QR Code](docs/images/04-qrcode.png)

--- 

### Dashboard

The dashboard is your home screen after loggin in. It gives you a quick overview of upcoming events, your clubs, and recent activity on campus.

![Dashboard](docs/images/05-dashboard.png)

---

### Clubs

#### Browsing Clubs

Navigate to **Clubs** in the top menu to see all approved campus clubs. Clubs are listed eight per page - use the pagination controls at the bottom to see more.

![Club List](docs/images/06-clublist.png)

Click any club card to open its detail page, where you can read the club description, see current members, and view upcoming events.

![Club Detail Page](docs/images/07-clubdetail.png)