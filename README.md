# OTCPulse

A campus community platform for Ozarks Technical Community College.

---

## Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/GravesSoftwareDev/otc_pulse.git
cd otc_pulse
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
pip install -r requirements.txt
```

**4. Apply migrations**
```bash
cd otc_pulse
python3 manage.py migrate
```

**5. Seed demo data**
```bash
python3 manage.py shell -c "exec(open('seed.py').read())"
```

**6. Run the development server**
```bash
python3 manage.py runserver
```

The app will be available at `http://127.0.0.1:8000`.
Demo admin login: `gravess` / `Test123!`

---

## Deployment (Railway)

The project is configured for Railway with a PostgreSQL database.

Set the following environment variables in Railway → Variables:

| Variable | Value |
|---|---|
| `SECRET_KEY` | A long random string |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.up.railway.app,otc-pulse.gravessoftware.dev` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app,https://otc-pulse.gravessoftware.dev` |
| `DATABASE_URL` | Auto-set by Railway Postgres plugin |

On deploy, Railway runs migrations and collectstatic automatically via `railway.toml`.

---

## User Guide

### Table of Contents
- [Getting Started](#getting-started)
- [Account & Profile](#account--profile)
- [Dashboard](#dashboard)
- [Clubs](#clubs)
    - [Browsing & Searching Clubs](#browsing--searching-clubs)
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
    - [Managing User Roles](#managing-user-roles)

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

Click **Get Started** to go to the registration form. The form requires an `@otc.edu` email address, which is validated automatically.

![Registration Form](docs/images/02-register.png)

#### Your Profile

Once logged in, click your name or avatar in the navigation bar to open your profile. From here you can:

- Update your display name and profile picture
- Change your password
- View your personal QR code (used for event check-in)
- Track your support requests and space reservations

![Profile Page](docs/images/03-profile.png)

#### Your QR Code

Every account has a unique QR code. Event organizers scan this code at the door to record your attendance and award points.

![Personal QR Code](docs/images/04-qrcode.png)

#### Forgot Password

Password resets are handled by Student Engagement. Click **Forgot password?** on the login page to open a pre-addressed email to the Student Engagement office.

---

### Dashboard

The dashboard is your home screen after logging in. It gives a quick overview of upcoming events, your clubs, and recent activity.

![Dashboard](docs/images/05-dashboard.png)

---

### Clubs

#### Browsing & Searching Clubs

Navigate to **Clubs** in the top menu to see all approved campus clubs. Use the search bar to filter by name or description. Results are paginated eight per page.

![Club List](docs/images/06-clublist.png)

Click any club card to open its detail page, where you can read the club description, see current members, and view upcoming events.

![Club Detail Page](docs/images/07-clubdetail.png)

#### Joining a Club

On a club's detail page, click **Join Club**. You will immediately become a member and appear on that club's leaderboard.

To leave, return to the detail page and click **Leave Club**.

![Join Club Button](docs/images/08-joinclub.png)
![Leave Club Button](docs/images/09-leaveclub.png)

#### Creating a Club

1. Click **+ Create Club** from the Clubs page.
2. Fill in the club name, description, and optionally upload a club image.
3. Submit — the club is sent to Student Engagement for approval before it appears in the public list.

![Create Club Button](docs/images/10-createbutton.png)
![Create Club Form](docs/images/11-createform.png)

#### Club Officers & Faculty Advisors

Members can apply to become an officer by clicking **Apply for Officer Role** on the club's detail page. Club leads review applications and approve or deny them from the club management panel.

Faculty advisors are assigned by Student Engagement admins via the Manage Users page.

![Officer application](docs/images/12-officerbutton.png)

---

### Events

#### Viewing Events

Click **Events** in the top nav to see all published upcoming events across campus. Use the search bar to filter by event title or club name.

![Event List - Club Page](docs/images/13-events.png)

#### Creating an Event

Club officers, faculty advisors, and Student Engagement can create events:

1. Open a club's detail page and click **Create Event**.
2. Fill in the title, date/time, location, and point value.
3. Submit for approval. The workflow is: **Draft → Submitted → Approved → Published → Completed**.

![Create Event Form](docs/images/14-createevents.png)

Once approved by Student Engagement, officers can publish the event so students can see it.

![Publish Event](docs/images/15-publishevent.png)

#### Attending an Event (QR Check-in)

When you arrive at an event, an officer will be running the **Check-in Terminal**. Open your profile and display your QR code. The terminal scans it, records your attendance, and automatically awards points.

![Check-In Terminal](docs/images/16-checkin.png)
![Check-In Success](docs/images/16-checkinsuccess.png)

#### Event Surveys

Organizers can attach a survey to any event. Survey question types:

- **Text response**
- **Star rating** (1–5 stars)
- **Yes / No**

Attendees complete the survey after the event ends and earn bonus points for doing so. Organizers can view aggregated results from the event management panel.

![Survey Creation](docs/images/19-surveycreaqte.png)
![Surveys](docs/images/18-surveys.png)

#### Exporting Attendance

Officers can export a CSV of all attendees for any completed event. Open the event's management page and click **Export CSV**.

![Export Attendance](docs/images/17-attendance.png)

---

### Leaderboard

Each club has its own leaderboard ranking members by total points earned. View it on the club's detail page.

![Club Leaderboard](docs/images/20-clubleaderboard.png)

There is also a campus-wide leaderboard for clubs and individual students, accessible via **Leaderboard** in the top nav.

![School Leaderboard](docs/images/20-schoolleaderboard.png)

---

### Bulletin Board

The Bulletin Board is where club officers submit and track support requests and space reservations.

![Bulletin Board](docs/images/21-bulletinboard.png)

Use the search bar to filter requests by club name or notes.

#### Submitting a Request

Click **+ New Request** and choose a category:

| Category | Use case |
|---|---|
| IT | Technology support or equipment needs |
| Finance | Budget or reimbursement requests |
| Custodial | Cleaning or room setup needs |
| Security | Security presence or access requests |
| Event Approval | Formal event approval outside the clubs workflow |
| Other | Anything that doesn't fit above |

Fill in the details and a due date (**at least one week in advance**), then submit. Track status (Pending / Approved / Denied) from the Bulletin Board or your profile.

![New Request Form](docs/images/22-requestform.png)

#### Reserving a Space

Officers and advisors can reserve a room for a meeting or club activity without needing to create a full public event — useful for officer meetings, planning sessions, and internal gatherings.

**Two ways to reserve:**
- Click **📍 Reserve a Space** on your club's detail page (club is pre-selected).
- Click **+ Reserve a Space** from your profile's Reservations card.

Fill in the club, purpose, location, and time. Reservations are submitted to Student Engagement for approval. Approved reservations appear on your profile.

---

### Admin Features

Users with the **Student Engagement** role have access to additional management tools across the platform:

- **Club Approvals** — Review and approve or deny newly submitted clubs from the club detail page.
- **Event Approvals** — Approve submitted events and publish them to the events feed.
- **Request & Reservation Approvals** — Manage all pending Bulletin Board requests and space reservations from the profile page or Bulletin Board.
- **Full Visibility** — Admins see all clubs (including pending and denied), all requests, and all reservations platform-wide.

#### Managing User Roles

Student Engagement admins can promote any registered user to **Faculty Advisor** or **Student Engagement** (admin) directly from the app — no Django admin panel required.

1. Click your avatar in the top-right corner.
2. Select **⚙️ Manage Users** from the dropdown.
3. Search for the user by name, username, or OTC email.
4. Select the new role from the dropdown next to their name and click **Update**.
