"""
seed.py — populate the OTCPulse database with realistic demo data.

Usage (from the otc_pulse/ directory):
    python manage.py shell < ../seed.py
"""

import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from account.models import Profile
from clubhouse.models import (
    Attendance, Club, Event, Location,
    Survey, SurveyQuestion, SurveyResponse,
)
from bulletin_board.models import Request, Reservation

User = get_user_model()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user(username, first, last, password="otcpulse2025", email=None, is_staff=False, is_superuser=False):
    user, created = User.objects.get_or_create(
        username=username,
        defaults=dict(
            first_name=first,
            last_name=last,
            email=email or f"{username}@otc.edu",
            is_staff=is_staff,
            is_superuser=is_superuser,
        ),
    )
    if created:
        user.set_password(password)
        user.save()
    return user


def make_profile(user, role, points=None):
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults=dict(
            otc_email=f"{user.username}@otc.edu",
            role=role,
            points=points if points is not None else random.randint(0, 600),
        ),
    )
    return profile


now = timezone.now()

def future(days=0, hours=0):
    return now + timedelta(days=days, hours=hours)

def past(days=0, hours=0):
    return now - timedelta(days=days, hours=hours)


# ---------------------------------------------------------------------------
# 1. Users & Profiles
# ---------------------------------------------------------------------------

print("Creating users and profiles...")

# ── gravess: primary admin account ──────────────────────────────────────────
gravess_user = make_user(
    "gravess", "Shanna", "Graves",
    password="Test123!",
    is_staff=True, is_superuser=True,
)
gravess_profile = make_profile(gravess_user, Profile.Role.ADMIN, points=0)

# ── Faculty advisors ─────────────────────────────────────────────────────────
advisor_data = [
    ("dmorgan",   "David",    "Morgan"),
    ("lpatterson","Laura",    "Patterson"),
    ("rchavez",   "Rosa",     "Chavez"),
    ("tmitchell", "Thomas",   "Mitchell"),
]
advisor_users    = [make_user(*d) for d in advisor_data]
advisor_profiles = [make_profile(u, Profile.Role.ADVISOR) for u in advisor_users]

# ── Club officers ────────────────────────────────────────────────────────────
officer_data = [
    ("jcollins",  "Jordan",   "Collins"),
    ("anavarrete","Alejandra","Navarrete"),
    ("bwallace",  "Brandon",  "Wallace"),
    ("tnguyen",   "Tiffany",  "Nguyen"),
    ("mreynolds", "Marcus",   "Reynolds"),
    ("schaney",   "Sierra",   "Chaney"),
]
officer_users    = [make_user(*d) for d in officer_data]
officer_profiles = [make_profile(u, Profile.Role.LEAD) for u in officer_users]

# ── Regular students ─────────────────────────────────────────────────────────
student_data = [
    ("awright",   "Amber",    "Wright"),
    ("cford",     "Cameron",  "Ford"),
    ("dbaker",    "Destiny",  "Baker"),
    ("ekim",      "Ethan",    "Kim"),
    ("fmartinez", "Faith",    "Martinez"),
    ("gporter",   "Gabriel",  "Porter"),
    ("hcooper",   "Hannah",   "Cooper"),
    ("iross",     "Isaiah",   "Ross"),
    ("jbutler",   "Jasmine",  "Butler"),
    ("kreed",     "Kyle",     "Reed"),
    ("lflores",   "Lydia",    "Flores"),
    ("mbell",     "Mason",    "Bell"),
    ("nalexander","Natalie",  "Alexander"),
    ("ograham",   "Owen",     "Graham"),
    ("pwood",     "Paige",    "Wood"),
    ("rjames",    "Riley",    "James"),
]
student_users    = [make_user(*d) for d in student_data]
student_profiles = [make_profile(u, Profile.Role.STUDENT) for u in student_users]

all_non_admin_profiles = officer_profiles + student_profiles

print(f"  {User.objects.count()} users ready.")


# ---------------------------------------------------------------------------
# 2. Locations
# ---------------------------------------------------------------------------

print("Creating locations...")

location_data = [
    ("ICW",   "101",  "Computer Lab"),
    ("ICW",   "205",  "Innovation Hub"),
    ("IC",    "110",  "Conference Room A"),
    ("IC",    "220",  "Conference Room B"),
    ("ICE",   "301",  "Auditorium"),
    ("ITTC",  "102",  "Auto Lab"),
    ("ITTC",  "210",  "Welding Shop"),
    ("PMC",   "115",  None),
    ("LNC",   "103",  "Study Lounge"),
    ("GRAFF", "201",  "Seminar Room"),
]

locations = []
for building, room_num, room_name in location_data:
    loc, _ = Location.objects.get_or_create(
        building=building, room_num=room_num,
        defaults=dict(room_name=room_name),
    )
    locations.append(loc)

print(f"  {len(locations)} locations ready.")


# ---------------------------------------------------------------------------
# 3. Clubs
# ---------------------------------------------------------------------------

print("Creating clubs...")

club_data = [
    {
        "name":        "Phi Theta Kappa Honor Society",
        "description": "PTK is the premier honor society for community college students. We recognize academic achievement, develop leadership skills, and serve our campus and community.",
        "emoji":       "🎓",
        "approved":    True,
        "advisor_idx": 0,
        "officer_idxs": [0, 1],
        "member_idxs":  list(range(0, 10)),
    },
    {
        "name":        "SkillsUSA",
        "description": "A national career and technical student organization preparing students for careers in trade, technical, and skilled service occupations. We compete regionally and nationally.",
        "emoji":       "🔧",
        "approved":    True,
        "advisor_idx": 3,
        "officer_idxs": [2, 4],
        "member_idxs":  list(range(4, 14)),
    },
    {
        "name":        "HOSA – Future Health Professionals",
        "description": "HOSA empowers healthcare students to become competent, compassionate health professionals. We host health fairs, CPR certifications, and career prep workshops.",
        "emoji":       "🩺",
        "approved":    True,
        "advisor_idx": 1,
        "officer_idxs": [1, 3],
        "member_idxs":  list(range(2, 12)),
    },
    {
        "name":        "Computer Science & Coding Club",
        "description": "Weekly hack sessions, project showcases, and industry guest speakers. Whether you're writing your first loop or deploying your fifth app, you belong here.",
        "emoji":       "💻",
        "approved":    True,
        "advisor_idx": 0,
        "officer_idxs": [0, 5],
        "member_idxs":  list(range(0, 8)),
    },
    {
        "name":        "Veteran Student Organization",
        "description": "Connecting veteran and military-affiliated students with campus resources, peer support, and community service opportunities.",
        "emoji":       "🎖️",
        "approved":    True,
        "advisor_idx": 2,
        "officer_idxs": [4, 2],
        "member_idxs":  list(range(6, 16)),
    },
    {
        "name":        "Creative Arts Collective",
        "description": "A welcoming space for visual artists, graphic designers, photographers, and makers. We host exhibitions, critique nights, and collaborative installations.",
        "emoji":       "🎨",
        "approved":    True,
        "advisor_idx": 1,
        "officer_idxs": [3, 5],
        "member_idxs":  list(range(1, 9)),
    },
    {
        "name":        "Esports & Gaming Club",
        "description": "Compete in organized tournaments, practice with teammates, and connect with the broader gaming community. We play everything from PC titles to tabletop RPGs.",
        "emoji":       "🎮",
        "approved":    True,
        "advisor_idx": 3,
        "officer_idxs": [5, 0],
        "member_idxs":  list(range(3, 13)),
    },
    {
        "name":        "Student Government Association",
        "description": "The SGA represents the voice of OTC students. We advocate for student needs, allocate activity funds, and plan campus-wide events throughout the year.",
        "emoji":       "🏛️",
        "approved":    True,
        "advisor_idx": 2,
        "officer_idxs": [1, 4],
        "member_idxs":  list(range(0, 12)),
    },
    {
        "name":        "Automotive Technology Club",
        "description": "Hands-on club for auto tech students and enthusiasts. We work on real vehicles, attend car shows, and bring in guest mechanics and industry professionals.",
        "emoji":       "🚗",
        "approved":    True,
        "advisor_idx": 3,
        "officer_idxs": [2, 5],
        "member_idxs":  list(range(5, 15)),
    },
    {
        "name":        "Psychology & Wellness Club",
        "description": "Promoting mental health awareness and peer support on campus. We host workshops, panel discussions, and a weekly open circle for anyone who needs a space to connect.",
        "emoji":       "🧠",
        "approved":    True,
        "advisor_idx": 1,
        "officer_idxs": [3, 1],
        "member_idxs":  list(range(0, 10)),
    },
    {
        "name":        "Entrepreneurship & Business Club",
        "description": "Pitch ideas, build business plans, and network with local professionals and OTC alumni. We partner with the Springfield Chamber of Commerce for our annual pitch competition.",
        "emoji":       "🚀",
        "approved":    False,  # pending — good for testing that flow
        "advisor_idx": 0,
        "officer_idxs": [0],
        "member_idxs":  list(range(8, 16)),
    },
]

clubs = []
for cd in club_data:
    club, _ = Club.objects.get_or_create(
        name=cd["name"],
        defaults=dict(
            description=cd["description"],
            emoji=cd["emoji"],
            approved=cd["approved"],
        ),
    )
    club.advisors.add(advisor_profiles[cd["advisor_idx"]])
    for i in cd["officer_idxs"]:
        club.officers.add(officer_profiles[i])
        club.members.add(officer_profiles[i])
    for i in cd["member_idxs"]:
        club.members.add(all_non_admin_profiles[i])
    clubs.append(club)

print(f"  {len(clubs)} clubs ready.")


# ---------------------------------------------------------------------------
# 4. Events
# ---------------------------------------------------------------------------

print("Creating events...")

event_specs = [
    # Phi Theta Kappa
    dict(title="Spring Induction Ceremony",      club=clubs[0], status="PUBLISHED", loc=locations[4],
         start=future(7),  end=future(7, 2),    points=25),
    dict(title="Leadership Retreat Planning",    club=clubs[0], status="DRAFT",     loc=None,
         start=future(21), end=future(21, 4),   points=20),

    # SkillsUSA
    dict(title="Regional Competition Prep",      club=clubs[1], status="PUBLISHED", loc=locations[6],
         start=future(3),  end=future(3, 3),    points=20),
    dict(title="Tool & Trade Safety Workshop",   club=clubs[1], status="APPROVED",  loc=locations[5],
         start=future(10), end=future(10, 2),   points=15),

    # HOSA
    dict(title="CPR Certification Day",          club=clubs[2], status="PUBLISHED", loc=locations[2],
         start=future(2),  end=future(2, 4),    points=30),
    dict(title="Spring Health Fair",             club=clubs[2], status="SUBMITTED", loc=locations[4],
         start=future(14), end=future(14, 6),   points=25),

    # CS & Coding Club
    dict(title="Hack Night #14",                 club=clubs[3], status="PUBLISHED", loc=locations[0],
         start=future(1),  end=future(1, 3),    points=10),
    dict(title="Intro to Django Workshop",       club=clubs[3], status="APPROVED",  loc=locations[1],
         start=future(9),  end=future(9, 2),    points=15),
    dict(title="Spring Hackathon",               club=clubs[3], status="DRAFT",     loc=None,
         start=future(28), end=future(29),      points=50),

    # Veteran Student Organization
    dict(title="Welcome & Resource Fair",        club=clubs[4], status="PUBLISHED", loc=locations[8],
         start=future(4),  end=future(4, 2),    points=10),
    dict(title="Community Service Day",          club=clubs[4], status="APPROVED",  loc=None,
         start=future(18), end=future(18, 5),   points=20),

    # Creative Arts
    dict(title="Portfolio Critique Night",       club=clubs[5], status="PUBLISHED", loc=locations[9],
         start=future(3),  end=future(3, 2),    points=10),
    dict(title="Spring Exhibition Opening",      club=clubs[5], status="SUBMITTED", loc=locations[4],
         start=future(16), end=future(16, 3),   points=20),

    # Esports
    dict(title="Valorant Tournament",            club=clubs[6], status="PUBLISHED", loc=locations[0],
         start=future(5),  end=future(5, 4),    points=15),
    dict(title="Game Design Showcase",           club=clubs[6], status="DRAFT",     loc=None,
         start=future(25), end=future(25, 3),   points=20),

    # SGA
    dict(title="Student Budget Forum",           club=clubs[7], status="PUBLISHED", loc=locations[2],
         start=future(2),  end=future(2, 2),    points=10),
    dict(title="Campus Improvement Townhall",    club=clubs[7], status="APPROVED",  loc=locations[4],
         start=future(12), end=future(12, 2),   points=15),

    # Auto Club
    dict(title="Spring Car Show",                club=clubs[8], status="PUBLISHED", loc=locations[5],
         start=future(6),  end=future(6, 4),    points=15),

    # Psychology & Wellness
    dict(title="Weekly Check-in Circle",         club=clubs[9], status="PUBLISHED", loc=locations[3],
         start=future(2),  end=future(2, 1),    points=5),
    dict(title="Stress Less Finals Workshop",    club=clubs[9], status="APPROVED",  loc=locations[9],
         start=future(11), end=future(11, 2),   points=10),

    # ── Past / completed events (for attendance & survey data) ──────────────
    dict(title="Fall Induction Ceremony",        club=clubs[0], status="COMPLETED", loc=locations[4],
         start=past(30),  end=past(29, 22),     points=25),
    dict(title="Hack Night #13",                 club=clubs[3], status="COMPLETED", loc=locations[0],
         start=past(14),  end=past(13, 21),     points=10),
    dict(title="CPR Recertification",            club=clubs[2], status="COMPLETED", loc=locations[2],
         start=past(21),  end=past(20, 20),     points=30),
    dict(title="Open Support Circle",            club=clubs[9], status="COMPLETED", loc=locations[3],
         start=past(7),   end=past(6, 23),      points=5),
    dict(title="Regional Skills Preview",        club=clubs[1], status="COMPLETED", loc=locations[6],
         start=past(10),  end=past(9, 21),      points=20),
]

events = []
for spec in event_specs:
    ev, _ = Event.objects.get_or_create(
        title=spec["title"],
        club=spec["club"],
        defaults=dict(
            status=spec["status"],
            start_time=spec["start"],
            end_time=spec["end"],
            location=spec["loc"],
            point_value=spec["points"],
        ),
    )
    events.append(ev)

print(f"  {len(events)} events ready.")


# ---------------------------------------------------------------------------
# 5. Attendance (past events only)
# ---------------------------------------------------------------------------

print("Creating attendance records...")

past_events = [e for e in events if e.status == "COMPLETED"]

for ev in past_events:
    pool = random.sample(student_users, k=random.randint(4, min(10, len(student_users))))
    for user in pool:
        att, created = Attendance.objects.get_or_create(event=ev, user=user)
        if created:
            profile = user.profile
            profile.points += ev.point_value
            profile.save(update_fields=["points"])

print(f"  Attendance records: {Attendance.objects.count()}")


# ---------------------------------------------------------------------------
# 6. Survey questions & responses
# ---------------------------------------------------------------------------

print("Creating surveys...")

survey_specs = {
    "Fall Induction Ceremony": {
        "questions": [
            ("How would you rate the ceremony overall?",           "STARS", 0, True),
            ("Did the ceremony meet your expectations?",           "YESNO", 1, True),
            ("Would you recommend PTK to a fellow student?",       "YESNO", 2, True),
            ("What was your favorite part of the evening?",        "TEXT",  3, False),
            ("Any suggestions for next semester's ceremony?",      "TEXT",  4, False),
        ],
        "text_pools": {
            "What was your favorite part of the evening?": [
                "The keynote speaker was incredibly motivating.",
                "Getting to meet other honor students was awesome.",
                "The candle lighting tradition was really moving.",
                "The officers did a great job running everything.",
                "Finally feeling recognized for my GPA — it means a lot.",
            ],
            "Any suggestions for next semester's ceremony?": [
                "More seating for family members would be great.",
                "Could we add a reception with light refreshments?",
                "The room was a bit warm — better AC would help.",
                "Maybe a slideshow of inductee photos?",
                "",
            ],
        },
        "star_weights":  [0, 1, 2, 4, 5],
        "yesno_weights": [[1, 5], [0, 6]],
    },
    "Hack Night #13": {
        "questions": [
            ("How would you rate this hack night?",                "STARS", 0, True),
            ("Did you make meaningful progress on a project?",     "YESNO", 1, True),
            ("Was the time slot long enough?",                     "YESNO", 2, False),
            ("What did you build or work on tonight?",             "TEXT",  3, False),
            ("Suggestions for future hack nights?",                "TEXT",  4, False),
        ],
        "text_pools": {
            "What did you build or work on tonight?": [
                "A Django REST API for a personal finance tracker.",
                "Practiced React hooks and built a to-do app.",
                "Set up a CI/CD pipeline with GitHub Actions.",
                "Started learning Flask — made a small image upload app.",
                "Worked on my portfolio site — finally deployed it!",
            ],
            "Suggestions for future hack nights?": [
                "A themed challenge would make it more exciting.",
                "Having mentors rotate around to help would be awesome.",
                "Snacks would go a long way!",
                "Mini demos at the end so we can see each other's work.",
                "",
            ],
        },
        "star_weights":  [0, 1, 3, 5, 4],
        "yesno_weights": [[2, 5], [1, 3]],
    },
    "CPR Recertification": {
        "questions": [
            ("How would you rate this certification session?",     "STARS", 0, True),
            ("Do you feel confident performing CPR after today?",  "YESNO", 1, True),
            ("Was the instructor easy to follow?",                 "YESNO", 2, True),
            ("What did you find most valuable about this session?","TEXT",  3, False),
            ("Is there another health skill you'd like us to cover?","TEXT",4, False),
        ],
        "text_pools": {
            "What did you find most valuable about this session?": [
                "The hands-on manikin practice — repetition really helped.",
                "Learning the updated compression ratio was eye-opening.",
                "Knowing I could actually help someone in an emergency now.",
                "The AED walkthrough was something I'd never done before.",
                "The instructor kept it engaging and low-pressure.",
            ],
            "Is there another health skill you'd like us to cover?": [
                "Basic first aid and wound care.",
                "Heimlich maneuver and choking response.",
                "Mental health first aid — how to help someone in crisis.",
                "Narcan training for opioid overdoses.",
                "",
            ],
        },
        "star_weights":  [0, 0, 1, 4, 7],
        "yesno_weights": [[0, 8], [0, 8]],
    },
    "Open Support Circle": {
        "questions": [
            ("How would you rate this week's circle?",             "STARS", 0, True),
            ("Did you feel safe and heard today?",                 "YESNO", 1, True),
            ("Would you encourage a friend to attend?",            "YESNO", 2, True),
            ("What made today's session valuable to you?",         "TEXT",  3, False),
            ("Is there a topic you'd like us to address?",         "TEXT",  4, False),
        ],
        "text_pools": {
            "What made today's session valuable to you?": [
                "Knowing I'm not the only one dealing with stress.",
                "The breathing exercise at the start really helped me settle.",
                "No judgment — just people listening. That's rare.",
                "Hearing others share made me feel less alone.",
                "The check-in format was simple but really effective.",
            ],
            "Is there a topic you'd like us to address?": [
                "Managing exam anxiety.",
                "Balancing school, work, and family.",
                "Resources for students experiencing food insecurity.",
                "How to support a friend who's struggling.",
                "",
            ],
        },
        "star_weights":  [0, 0, 1, 3, 7],
        "yesno_weights": [[0, 7], [0, 7]],
    },
    "Regional Skills Preview": {
        "questions": [
            ("How would you rate this preview session?",           "STARS", 0, True),
            ("Do you feel more prepared for regionals?",           "YESNO", 1, True),
            ("Was the event well-organized?",                      "YESNO", 2, True),
            ("What skill area do you feel strongest in?",          "TEXT",  3, False),
            ("What should we focus on before the competition?",    "TEXT",  4, False),
        ],
        "text_pools": {
            "What skill area do you feel strongest in?": [
                "Electrical wiring and safety procedures.",
                "Welding — especially MIG.",
                "Automotive diagnostics and troubleshooting.",
                "Cabinet-making and precision measuring.",
                "HVAC fundamentals.",
            ],
            "What should we focus on before the competition?": [
                "Time management under pressure.",
                "More practice on the written exam portion.",
                "Reviewing safety regulations — those trip people up.",
                "Mock judging rounds would help a lot.",
                "",
            ],
        },
        "star_weights":  [0, 1, 2, 5, 4],
        "yesno_weights": [[1, 6], [0, 7]],
    },
}

for ev in past_events:
    spec = survey_specs.get(ev.title)
    if not spec:
        continue

    for prompt, qtype, order, required in spec["questions"]:
        SurveyQuestion.objects.get_or_create(
            event=ev, prompt=prompt,
            defaults=dict(question_type=qtype, order=order, required=required),
        )

    questions   = list(ev.survey_questions.order_by("order"))
    attendances = ev.attendees.select_related("user").all()

    for attendance in attendances:
        user   = attendance.user
        survey, created = Survey.objects.get_or_create(
            event=ev, attendee=user,
            defaults=dict(bonus_points_awarded=True),
        )
        if not created:
            continue

        yesno_counter = 0
        for q in questions:
            if q.question_type == "STARS":
                answer = random.choices(range(1, 6), weights=spec["star_weights"])[0]
                SurveyResponse.objects.get_or_create(
                    survey=survey, question=q,
                    defaults=dict(int_answer=answer),
                )
            elif q.question_type == "YESNO":
                w      = spec["yesno_weights"][yesno_counter % len(spec["yesno_weights"])]
                answer = random.choices([0, 1], weights=w)[0]
                SurveyResponse.objects.get_or_create(
                    survey=survey, question=q,
                    defaults=dict(int_answer=answer),
                )
                yesno_counter += 1
            else:
                pool = spec["text_pools"].get(q.prompt, [""])
                SurveyResponse.objects.get_or_create(
                    survey=survey, question=q,
                    defaults=dict(text_answer=random.choice(pool)),
                )

print(f"  Surveys: {Survey.objects.count()}, Responses: {SurveyResponse.objects.count()}")


# ---------------------------------------------------------------------------
# 7. Bulletin Board Requests
# ---------------------------------------------------------------------------

print("Creating requests...")

request_specs = [
    dict(club=clubs[2], event=events[4],  type="IT",       notes="Need 12 laptop stations with CPR training software pre-installed.",
         approval="O", due=future(2)),
    dict(club=clubs[3], event=events[6],  type="IT",       notes="WiFi whitelist for ~20 devices during hack night. Need bandwidth priority.",
         approval="O", due=future(1)),
    dict(club=clubs[7], event=events[15], type="CUSTODIAL", notes="Room setup: 40 chairs in a circle, podium, and whiteboard for budget forum.",
         approval="-", due=future(2)),
    dict(club=clubs[0], event=events[0],  type="SECURITY", notes="Extended keycard access to auditorium until 10 PM for induction ceremony.",
         approval="-", due=future(7)),
    dict(club=clubs[2], event=events[5],  type="FINANCE",  notes="Budget request: $350 for health fair supplies, brochures, and tables.",
         approval="-", due=future(14)),
    dict(club=clubs[6], event=events[13], type="IT",       notes="Need 10 high-spec gaming PCs in Computer Lab for tournament. Requesting reserved slots.",
         approval="-", due=future(5)),
    dict(club=clubs[4], event=events[9],  type="EVENT",    notes="Approval for welcome & resource fair — expecting 60+ attendees, need main hallway access.",
         approval="-", due=future(4)),
    dict(club=clubs[5], event=events[11], type="CUSTODIAL", notes="Easels, display boards, and extra lighting needed for portfolio critique night.",
         approval="-", due=future(3)),
    dict(club=clubs[8], event=events[17], type="SECURITY", notes="Parking lot access for car show — need cones and security for exterior lot.",
         approval="X", due=future(6)),
    dict(club=clubs[3], event=events[20], type="IT",       notes="Laptop loan for 4 students without personal devices for hack night.",
         approval="O", due=past(12), complete=True),
]

for spec in request_specs:
    Request.objects.get_or_create(
        club=spec["club"],
        notes=spec["notes"],
        defaults=dict(
            event=spec.get("event"),
            type=spec["type"],
            approval_status=spec.get("approval", "-"),
            due_date=spec["due"],
            complete=spec.get("complete", False),
        ),
    )

print(f"  Requests: {Request.objects.count()}")


# ---------------------------------------------------------------------------
# 8. Reservations
# ---------------------------------------------------------------------------

print("Creating reservations...")

reservation_specs = [
    # Event-linked
    dict(club=clubs[2], loc=locations[2],  event=events[4],  purpose="",
         start=future(2),  end=future(2, 4),   approved=True),
    dict(club=clubs[3], loc=locations[0],  event=events[6],  purpose="",
         start=future(1),  end=future(1, 3),   approved=True),
    dict(club=clubs[7], loc=locations[2],  event=events[15], purpose="",
         start=future(2),  end=future(2, 2),   approved=False),
    dict(club=clubs[0], loc=locations[4],  event=events[0],  purpose="",
         start=future(7),  end=future(7, 2),   approved=False),
    # Standalone meeting reservations
    dict(club=clubs[0], loc=locations[8],  event=None, purpose="Officer planning meeting",
         start=future(4),  end=future(4, 1),   approved=True),
    dict(club=clubs[3], loc=locations[1],  event=None, purpose="Project team sync",
         start=future(3),  end=future(3, 1),   approved=False),
    dict(club=clubs[7], loc=locations[9],  event=None, purpose="SGA executive meeting",
         start=future(5),  end=future(5, 2),   approved=True),
    # Past
    dict(club=clubs[3], loc=locations[0],  event=events[20], purpose="",
         start=past(14),   end=past(13, 22),   approved=True),
]

for spec in reservation_specs:
    lookup = dict(club=spec["club"], event=spec["event"], start_time=spec["start"])
    Reservation.objects.get_or_create(
        **lookup,
        defaults=dict(
            location=spec["loc"],
            end_time=spec["end"],
            purpose=spec["purpose"],
            approved=spec["approved"],
        ),
    )

print(f"  Reservations: {Reservation.objects.count()}")


# ---------------------------------------------------------------------------
# 9. Officer applicants
# ---------------------------------------------------------------------------

print("Adding officer applicants...")

clubs[0].officer_applicants.add(student_profiles[3], student_profiles[8])
clubs[3].officer_applicants.add(student_profiles[1], student_profiles[6])
clubs[7].officer_applicants.add(student_profiles[0])

print("  Done.")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n✅ Seed complete!")
print(f"   Users:        {User.objects.count()}")
print(f"   Profiles:     {Profile.objects.count()}")
print(f"   Clubs:        {Club.objects.count()}")
print(f"   Locations:    {Location.objects.count()}")
print(f"   Events:       {Event.objects.count()}")
print(f"   Attendance:   {Attendance.objects.count()}")
print(f"   Surveys:      {Survey.objects.count()}")
print(f"   Requests:     {Request.objects.count()}")
print(f"   Reservations: {Reservation.objects.count()}")
print()
print("Admin login:  username=gravess  password=Test123!")
print("All other accounts default password: otcpulse2025")
