import json
import re
import requests
from datetime import datetime

# Validation Functions

def valid_mail(email):
    pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$' #pattern for checking the authenticity of an email address
    return bool(re.match(pattern,email))

def valid_phone(phone):
    return phone.isdigit() and len(phone)==10

def valid_name(name):
    return isinstance(name, str) and len(name.strip()) > 0

def valid_dates(start, end):

    try:
        start_date = datetime.strptime(start, "%Y-%m")
        end_date = datetime.strptime(end, "%Y-%m")

        return end_date > start_date

    except:
        return False
    
def check_link(url):

    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            return True

        return False

    except:
        return False

def validate_resume(data):

    validated = {}
    invalid = {}
    grey = {}

    # -------- Name --------
    name = data.get("name")

    if valid_name(name):
        validated["name"] = name
    else:
        invalid["name"] = "Invalid name format"

    # -------- Email --------
    email = data.get("email")

    if valid_mail(email):
        validated["email"] = email
    else:
        invalid["email"] = "Invalid email format"

    # -------- Phone --------
    phone = data.get("phone")

    if valid_phone(phone):
        validated["phone"] = phone
    else:
        invalid["phone"] = "Phone must be 10 digits"

    # -------- Education --------
    education_valid = []
    education_invalid = []
    education_grey = []

    for edu in data.get("education", []):

        start = edu.get("start_date")
        end = edu.get("end_date")
        status = edu.get("status")

        if status == "Enrolled":
            education_grey.append(edu)

        elif valid_dates(start, end):
            education_valid.append(edu)

        else:
            education_invalid.append({
                "data": edu,
                "error": "Invalid date sequence"
            })

    if education_valid:
        validated["education"] = education_valid

    if education_invalid:
        invalid["education"] = education_invalid

    if education_grey:
        grey["education"] = education_grey


    # -------- Experience --------
    exp_valid = []
    exp_invalid = []

    for exp in data.get("experience", []):

        if valid_dates(exp["start_date"], exp["end_date"]):
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


# -------------------------
# Runner
# -------------------------

if __name__ == "__main__":

    with open("sample_resume.json", "r") as f:
        resume = json.load(f)

    result = validate_resume(resume)

    with open("validated_output.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Validation Complete")