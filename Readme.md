# Intelligent Validation Engine

This project implements the Intelligent Validation Engine for the Smart Resume Audit & Verification System.

## Features

- Email format validation
- Phone number validation
- Name validation
- Temporal logic validation for experience and education
- URL accessibility verification
- Tri-state classification system

## Input

Raw resume JSON.

## Output

JSON file containing:

- validated_sections
- invalid_sections
- grey_area

## Run

pip install -r requirements.txt

python validator.py