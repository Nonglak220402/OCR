import streamlit as st
import zipfile
import tempfile
from pathlib import Path

from ocr import ocr_space_file, extract_text
from parser import parse_cacti
from excel import create_excel


# --------------------------------------------------
# Page setup
# --------------------------------------------------

st.set_page_config(
    page_title="Cacti Bandwidth OCR Extractor",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Cacti Bandwidth OCR Extractor")


# --------------------------------------------------
# File upload
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Cacti graphs",
    type=["zip", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)


# --------------------------------------------------
# ZIP extraction
# --------------------------------------------------

def extract_zip(zip_file, output_folder):

    with zipfile.ZipFile(zip_file) as z:
        z.extractall(output_folder)


# --------------------------------------------------
# Get all images
# --------------------------------------------------

def get_images(files):

    images = []

    temp_dir = tempfile.mkdtemp()

    for file in files:

        # ZIP file
        if file.name.lower().endswith(".zip"):

            extract_zip(
                file,
                temp_dir
            )

        # Direct image upload
        else:

            file_path = Path(temp_dir) / file.name

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

    # Find all supported images
    for extension in ["*.png", "*.jpg", "*.jpeg"]:

        images.extend(
            Path(temp_dir).rglob(extension)
        )

    return images


# --------------------------------------------------
# Start OCR
# --------------------------------------------------

if st.button(
    "🚀 Start OCR",
    type="primary"
):

    if not uploaded_files:

        st.warning(
            "Please upload at least one ZIP or image file."
        )

    else:

        # Find images
        images = get_images(
            uploaded_files
        )

        if not images:

            st.error(
                "No PNG, JPG, or JPEG images were found."
            )

        else:

            st.success(
                f"Found {len(images)} images."
            )

            # ------------------------------------------
            # Initialize results
            # ------------------------------------------

            results = []
            ocr_errors = []

            # ------------------------------------------
            # Progress
            # ------------------------------------------

            progress = st.progress(0)

            status = st.empty()

            # ------------------------------------------
            # Process images
            # ------------------------------------------

            for i, image in enumerate(images):

                status.write(
                    f"Processing "
                    f"{i + 1}/{len(images)}: "
                    f"`{image.name}`"
                )

                # --------------------------------------
                # OCR
                # --------------------------------------

                result = ocr_space_file(
                    image
                )

                text = extract_text(
                    result
                )

                # --------------------------------------
                # Check OCR result
                # --------------------------------------

                if not text:

                    error = result.get(
                        "error",
                        "OCR failed"
                    )

                    ocr_errors.append(
                        [
                            image.name,
                            error
                        ]
                    )

                else:

                    # ----------------------------------
                    # Parse OCR text
                    # ----------------------------------

                    row = parse_cacti(
                        text,
                        filename=image.name
                    )

                    results.append(
                        row
                    )

                # --------------------------------------
                # Update progress
                # --------------------------------------

                progress.progress(
                    (i + 1) / len(images)
                )

            # ------------------------------------------
            # Finished
            # ------------------------------------------

            status.success(
                "Processing completed! 🎉"
            )

            # ------------------------------------------
            # Create Excel
            # ------------------------------------------

            excel_file = create_excel(
                results,
                ocr_errors
            )

            # ------------------------------------------
            # Summary
            # ------------------------------------------

            st.success(
                f"Successfully processed "
                f"{len(results)} / "
                f"{len(images)} images."
            )

            if ocr_errors:

                st.warning(
                    f"{len(ocr_errors)} images "
                    f"failed OCR."
                )

            # ------------------------------------------
            # Download Excel
            # ------------------------------------------

            st.download_button(
                label="📥 Download Result.xlsx",
                data=excel_file,
                file_name="Result.xlsx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.spreadsheetml.sheet"
                )
            )
