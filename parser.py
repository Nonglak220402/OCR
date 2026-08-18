import re
from pathlib import Path


def clean_text(text):
    """
    Basic cleanup of OCR text.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    lines = []

    for line in text.split("\n"):
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_value(pattern, text, default=""):
    """
    Extract the first regex match from OCR text.
    """

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return default


def parse_cacti(text, filename=""):
    """
    Convert raw Cacti OCR text into structured data.

    Parameters
    ----------
    text : str
        Raw OCR.Space text.
    filename : str
        Original image filename.

    Returns
    -------
    dict
        Parsed Cacti information.
    """

    text = clean_text(text)

    result = {
        "File": Path(filename).name if filename else "",
        "Site": "",
        "Circuit": "",
        "Start Date": "",
        "End Date": "",
        "Inbound Current": "",
        "Inbound Average": "",
        "Inbound Maximum": "",
        "Outbound Current": "",
        "Outbound Average": "",
        "Outbound Maximum": "",
        "Raw OCR": text,
    }

    # --------------------------------------------------
    # TODO:
    # Put your existing Cacti parsing rules here.
    # --------------------------------------------------

    return result
