def normalize_schema(data):

    normalized = {}

    normalized["name"] = data.get("name")

    # emails
    normalized["emails"] = data.get("emails") or []
    if "email" in data:
        normalized["emails"].append(data["email"])

    # phones
    normalized["phones"] = data.get("phone_numbers") or []
    if "phone" in data:
        normalized["phones"].append(data["phone"])

    # skills
    normalized["skills"] = data.get("skills", [])

    # projects
    normalized["projects"] = data.get("projects", [])

    # experience
    normalized["experience"] = data.get("experience", [])

    # education
    edu = data.get("education", [])

    if isinstance(edu, dict):
        edu = list(edu.values())

    normalized["education"] = edu

    # links
    normalized["links"] = []

    if "github" in data:
        normalized["links"].append(data["github"])

    if "linkedin" in data:
        normalized["links"].append(data["linkedin"])

    normalized["links"].extend(data.get("links", []))

    return normalized