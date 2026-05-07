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

#### Joining a Club

On a club's detail page, click **Join Club**. You will immediately become a member and begin appearing on that club's leaderboard.

To leave a club, return to club detail page and click **Leave Club**

![Join Club Button](docs/images/08-joinclub.png)
![Leave Club Button](docs/images/09-leaveclub.png)

#### Creating a Club

1. Click **Create Club** from the Clubs page.
2. Fill in the club name, description, and optionally upload a club image.
3. Submit the form - your club will be sent to Student Engagement for approval before it appears in the public list.

![Create Club Button](docs/images/10-createbutton.png)
![Create Club Form](docs/images/11-createform.png)

#### Club Officers & Faculty Advisors

Club members can apply to become an officer by clicking **Apply for Officer Role** on the club's detail page. The club lead reviews applications and can approve or deny them from the club management panel.

Faculty advisors are assigned by Student Engagement admins.

![Officer application](docs/images/12-officerbutton.png)

---

### Events

#### Viewing Events

Approved and published events are listed on each club's detail page. It lists full details including date, time, location, and point value.

![Event List - Club Page](docs/images/13-events.png)

#### Creating an Event

Club officers, faculty advisors, and student engagement can create events:

1. Open the club's detail page and click **Create Event**
2. Fill in the event name, description, date/time, location, and point value (capped at 10 unless a special request is approved).
3. Submit the event for approval. The workflow is: **Draft → Submitted → Approved → Published → Completed**.

![Create Event Form](docs/images/14-createevents.png)

Once approved by sutdent engagement, you can publish the event so students can see it.

![Publish Event](docs/images/15-publishevent.png)

#### Attending an Event (QR Check-in)

When you arrive at an event, an officer or volunteer will be running the **Check-in Terminal**. Open your profile and display your personal QR code. The terminal will scan it and record your attenance, automatically awarding you the event's points.

![Check-In Terminal](docs/images/16-checkin.png)
![Check-In Success](docs/images/16-checkinsuccess.png)

#### Event Surveys

Event organizers can attach a survey to any event.
Surveys can include:

- **Text response** questions
- **Star rating** questions (1-5 stars)
- **Yes/No** questions

Attendees may complete the survey after the event is marked complete. Organizers can view aggregated results from the event management panel.

![Survey Creation](docs/images/19-surveycreaqte.png)

![Surveys](docs/images/18-surveys.png)

#### Exporting Attendance

Club officers can export a CSV of all attendees for any completed event. Open the event's management page and click **Export CSV**

![Export Attendance](docs/images/17-attendance.png)

---

### Leaderboard

Each club has its own leaderboard that ranks members by total points earned from event attendance. This can be viewed on the club detail page. 

![Club Leaderboard](docs/images/20-clubleaderboard.png)

There is also a leaderboard for clubs and the student body as a whole that can be viewed by clicking **Leaderboards** at the top.

![School Leaderboard](docs/images/20-schoolleaderboard.png)

---

### Bulletin Board

The Bulletin Board is where you can submit and view requests.

![Bulletin Board](docs/images/21-bulletinboard.png)

#### Submitting a Request

Click **New Request** and choose a category:

| Category | Use case |
|---|---|
| IT | Technology support or equipment needs |
| Finance | Budget or reimbursement requests |
| Custodial | Cleaning or setup needs |
| Security | Security presence or access requests |
| Event Approval | Formal event approval outside the clubs workflow |
| Other | Anything that doesn't fit above |

Fill in the details and a due date (**at least one week in advance**), then submit. You can track the status (Pending / Approved / Denied) from the Bulletin Board.

![New Request Form](docs/images/22-requestform.png)

### Admin Features

Users with a **Student Engagment** or **Admin** role have access to additional management tools:

- **Club Approvals** - Review and approve or deny newly submitted clubs.
- **Event Approvals** - Review submitted events before they go live.
- **Request Approvals** - Manage all pending Bulletin Board requests and space reservations.
- **Officer Assignments** - Assign faculty advisors to clubs.

The actions are accessible from the relevant club, event, or bulletin board pages when logged in as an admin. You may also review all pending requests from the requests page, or your profile page.

Admins/Student Engagement can also see all club analytics from the dashboard. Club officers and Faculty advisors can only see the information relevant to their clubs.

---

### Making an Admin acount

I have not yet implemented a way to do this on the front end. So in order to do so you must go through the Django Admin site. You can do this by adding 'admin/' to the end of the url and signing in with the following credentials:

Username: student_engagement
Password: Test123!

This will allow you to edit things in the database file directly. To make a registered account into an admin account click on **Profiles** on the home page.

![Django Admin Panel](docs/images/23-admindashboard.png)

Select the profile you wish to give admin status

![Profiles List](docs/images/24-profileslist.png)

Change their role to **Student Engagement**

![Profile Detail](docs/images/25-profiledetail.png)

