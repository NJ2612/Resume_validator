from validator.schema_normaliser import normalize_schema
from validator.validators import (
    validate_email,
    validate_phone,
    clean_skills
)
from validator.link_checker import check_link


def validate_resume(data):

    data = normalize_schema(data)

    validated = {}
    invalid = {}
    suspicious = {}

    # Name
    name = data.get("name")

    if isinstance(name, str) and len(name.strip()) > 2:
        validated["name"] = name.strip()
    else:
        invalid["name"] = name

    # Emails
    valid_emails = []
    invalid_emails = []

    for email in data.get("emails", []):

        if not isinstance(email, str):
            invalid_emails.append(email)
            continue
        email = email.strip()
        
        if validate_email(email):
            valid_emails.append(email)
        else:
            invalid_emails.append(email)

    if valid_emails:
        validated["emails"] = valid_emails

    if invalid_emails:
        invalid["emails"] = invalid_emails

    # Phones
    valid_phones = []
    invalid_phones = []

    for phone in data.get("phones", []):
        if not isinstance(phone, str):
            invalid_phones.append(phone)
            continue
        phone = phone.strip()
        if validate_phone(phone):
            valid_phones.append(phone)
        else:
            invalid_phones.append(phone)

    if valid_phones:
        validated["phones"] = valid_phones

    if invalid_phones:
        invalid["phones"] = invalid_phones

    # Skills
    skills = clean_skills(data["skills"])

    if len(skills) >= 2:
        validated["skills"] = skills
    else:
        suspicious["skills"] = skills

    # Links
    valid_links = []
    broken_links = []

    for link in data["links"]:

        if check_link(link):
            valid_links.append(link)
        else:
            broken_links.append(link)

    if valid_links:
        validated["links"] = valid_links

    if broken_links:
        invalid["links"] = broken_links

    return {
        "validated": validated,
        "invalid": invalid,
        "suspicious": suspicious
    }