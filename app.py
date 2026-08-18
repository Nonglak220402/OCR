import streamlit as st
import zipfile
import tempfile
from pathlib import Path


st.set_page_config(
    page_title="Cacti Bandwidth OCR Extractor",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Cacti Bandwidth OCR Extractor")

uploaded_files = st.file_uploader(
    "Upload Cacti graphs",
    type=["zip", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)


def extract_zip(zip_file, output_folder):

    with zipfile.ZipFile(zip_file) as z:
        z.extractall(output_folder)


def get_images(files):

    images = []
    temp_dir = tempfile.mkdtemp()

    for file in files:

        # ZIP file
        if file.name.lower().endswith(".zip"):

            extract_zip(file, temp_dir)

        # Direct image upload
        else:

            file_path = Path(temp_dir) / file.name

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

    # Find all supported images
    for extension in ["*.png", "*.jpg", "*.jpeg"]:
        images.extend(Path(temp_dir).rglob(extension))

    return images


if st.button("🚀 Start OCR", type="primary"):

    if not uploaded_files:
        st.warning("Please upload at least one ZIP or image file.")

    else:

        images = get_images(uploaded_files)

        if not images:
            st.error("No PNG, JPG, or JPEG images were found.")

        else:

            st.success(f"Found {len(images)} images.")

            progress = st.progress(0)
            status = st.empty()

            for i, image in enumerate(images):

                status.write(
                    f"Processing {i + 1}/{len(images)}: `{image.name}`"
                )

                # OCR will go here
                # result = ocr_space_file(image)

                progress.progress(
                    (i + 1) / len(images)
                )

            status.success("Processing completed! 🎉")
