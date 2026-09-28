import PyPDF2


def extract_text_from_pdf(file):

    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_txt(file):

    return file.read().decode("utf-8")