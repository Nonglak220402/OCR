import requests
import streamlit as st


OCR_API_URL = "https://api.ocr.space/parse/image"


def ocr_space_file(filename, language="eng", overlay=False):
    """
    Send a local image file to OCR.Space API.

    Parameters
    ----------
    filename : str or Path
        Path to the image file.
    language : str
        OCR language. Default = English.
    overlay : bool
        Whether OCR.Space should return overlay information.

    Returns
    -------
    dict
        OCR.Space JSON response.
    """

    api_key = st.secrets["OCR_SPACE_API_KEY"]

    payload = {
        "apikey": api_key,
        "language": language,
        "isOverlayRequired": overlay,
        "OCREngine": "2"
    }

    try:

        with open(filename, "rb") as f:

            response = requests.post(
                OCR_API_URL,
                files={
                    "file": f
                },
                data=payload,
                timeout=120
            )

        response.raise_for_status()

        result = response.json()

        return result

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": "OCR request timed out."
        }

    except requests.exceptions.RequestException as e:

        return {
            "success": False,
            "error": f"API request failed: {str(e)}"
        }

    except Exception as e:

        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }


def extract_text(result):
    """
    Extract OCR text from OCR.Space response.
    """

    if not result:
        return ""

    # Our own error response
    if result.get("success") is False:
        return ""

    # OCR.Space processing error
    if result.get("IsErroredOnProcessing"):
        return ""

    parsed_results = result.get("ParsedResults")

    if not parsed_results:
        return ""

    return parsed_results[0].get("ParsedText", "")
