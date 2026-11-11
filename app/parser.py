import io
import re
import pdfplumber


def find(pattern, text, group=0):
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(group)
    else:
        return None


def extract_cv_data(pdf_bytes):
    # Extract text from the PDF
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"

    # Extract personal information
    email = find(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text)

    linkedin = find(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+", text)

    mobile = find(r"(?:\+972[- ]?|0)5\d(?:[- ]?\d){7}", text)

    personal_id = find(r"(?:ID Number|ID|תעודת זהות|ת\.?ז\.?)\s*:\s*(\d{9})",text, 1)

    name = find(r"^(?:Full Name|Name|שם מלא)\s*:\s*(.+)$", text, 1)

    if not name:
        lines = text.strip().splitlines()
        if lines:
            name = lines[0]
        else:
            name = ""

    first_name = None
    family_name = None

    parts = name.split("|")[0].split()

    if 2 <= len(parts) <= 4:
        first_name = parts[0]
        family_name = " ".join(parts[1:])

    # Return results
    return {
        "personalId": personal_id,
        "firstName": first_name,
        "familyName": family_name,
        "email": email,
        "linkedinUrl": linkedin,
        "mobile": mobile,
        "rawData": text
    }