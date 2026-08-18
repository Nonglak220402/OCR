import pandas as pd
from io import BytesIO


def create_excel(results, ocr_errors=None):

    df = pd.DataFrame(results)

    if ocr_errors is None:
        ocr_errors = []

    error_df = pd.DataFrame(
        ocr_errors,
        columns=[
            "File",
            "Error"
        ]
    )

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # Main results
        df.to_excel(
            writer,
            sheet_name="Results",
            index=False
        )

        # Failed OCR
        error_df.to_excel(
            writer,
            sheet_name="OCR Errors",
            index=False
        )

    output.seek(0)

    return output
