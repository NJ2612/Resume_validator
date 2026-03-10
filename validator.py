import re
import requests
from datetime import datetime


# -------------------------
# Validation Functions
# -------------------------

def valid_mail(email):
    if not email:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def valid_phone(phone):
    if not phone:
        return False
    return phone.isdigit() and len(phone) == 10


def valid_name(name):
    return isinstance(name, str) and len(name.strip()) > 2


def valid_dates(start, end):

    if not start or not end:
        return False

    try:
        start_date = datetime.strptime(start, "%Y-%m")
        end_date = datetime.strptime(end, "%Y-%m")

        return end_date > start_date

    except:
        return False


def check_link(url):

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        return response.status_code == 200

    except:
        return False


# -------------------------
# Main Validation Engine
# -------------------------

def validate_resume(data):

    validated = {}
    invalid = {}
    grey = {}

    # -------- Name --------
    name = data.get("name")

    if valid_name(name):
        validated["name"] = name
    else:
        invalid["name"] = {
            "value": name,
            "error": "Invalid name format"
        }

    # -------- Email --------
    email = data.get("email", "").strip()

    if valid_mail(email):
        validated["email"] = email
    else:
        invalid["email"] = {
            "value": email,
            "error": "Invalid email format"
        }

    # -------- Phone --------
    phone = data.get("phone")

    if valid_phone(phone):
        validated["phone"] = phone
    else:
        invalid["phone"] = {
            "value": phone,
            "error": "Phone must be 10 digits"
        }

    # -------- Education --------
    edu_valid = []
    edu_invalid = []
    edu_grey = []

    for edu in data.get("education", []):

        start = edu.get("start_date")
        end = edu.get("end_date")
        status = edu.get("status")

        if status == "Enrolled":
            edu_grey.append(edu)

        elif valid_dates(start, end):
            edu_valid.append(edu)

        else:
            edu_invalid.append({
                "data": edu,
                "error": "Invalid date sequence"
            })

    if edu_valid:
        validated["education"] = edu_valid

    if edu_invalid:
        invalid["education"] = edu_invalid

    if edu_grey:
        grey["education"] = edu_grey

    # -------- Experience --------
    exp_valid = []
    exp_invalid = []

    for exp in data.get("experience", []):

        start = exp.get("start_date")
        end = exp.get("end_date")

        if valid_dates(start, end):
            exp_valid.append(exp)
        else:
            exp_invalid.append({
                "data": exp,
                "error": "End date before start date"
            })

    if exp_valid:
        validated["experience"] = exp_valid

    if exp_invalid:
        invalid["experience"] = exp_invalid

    # -------- Projects --------
    project_valid = []
    project_invalid = []
    project_grey = []

    for proj in data.get("projects", []):

        link = proj.get("link")

        if not link:
            project_grey.append(proj)

        elif check_link(link):
            project_valid.append(proj)

        else:
            project_invalid.append({
                "data": proj,
                "error": "Broken project link"
            })

    if project_valid:
        validated["projects"] = project_valid

    if project_invalid:
        invalid["projects"] = project_invalid

    if project_grey:
        grey["projects"] = project_grey

    # -------- Links --------
    valid_links = []
    invalid_links = []

    for link in data.get("links", []):

        if check_link(link):
            valid_links.append(link)
        else:
            invalid_links.append({
                "url": link,
                "error": "Broken link"
            })

    if valid_links:
        validated["links"] = valid_links

    if invalid_links:
        invalid["links"] = invalid_links

    # -------- Skills --------
    skills = data.get("skills", [])

    if len(skills) >= 2:
        validated["skills"] = skills
    else:
        grey["skills"] = skills

    return {
        "validated_sections": validated,
        "invalid_sections": invalid,
        "grey_area": grey
    }