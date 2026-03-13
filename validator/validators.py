import re
from datetime import datetime


EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'


def validate_email(email):

    if not email:
        return False

    return bool(re.match(EMAIL_REGEX, email))


def normalize_phone(phone):

    if not phone:
        return None

    phone = phone.replace(" ", "").replace("-", "")

    if phone.startswith("+91"):
        phone = phone[3:]

    return phone


def validate_phone(phone):

    phone = normalize_phone(phone)

    if not phone:
        return False

    return phone.isdigit() and len(phone) >= 10


def clean_skills(skills):

    cleaned = []

    for skill in skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()

        if len(skill) > 1:
            cleaned.append(skill)

    return list(set(cleaned))


def parse_date(date_str):

    if not date_str:
        return None

    if str(date_str).lower() in ["present", "current"]:
        return datetime.now()

    try:
        return datetime.strptime(date_str, "%Y-%m")
    except:
        return None


def validate_date_order(start, end):

    start = parse_date(start)
    end = parse_date(end)

    if not start or not end:
        return False

    return end >= start