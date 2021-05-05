from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


KEYWORDS = ["gender inequality", "gender issue", "gender justice", "gender pay gap", "gender proud", "gender gap", "gendered violence",
            "sexual harassment", "sexism", "sexual assault", "sexual crime", "sexual harassment", "sexual misconduct", "sexual violence", "sexual abuse", "sexual accusation",
            "domestic violence", "intimate partner violence", "misogyny", "hashtag activism", "feminism", "feminist", "misogyny",
            "gender equality", "Chief Diversity Officer", "Diversity and Inclusion", "Diversity & Inclusion", "D&I", "diversity delegate", "sexism awareness",
            "code of conduct on sexual harassment", "anti-harassment policy and complaint", "anti-discrimination and harassment policy", "Sexual Harassment Prevention Training",
            "bystander intervention", "Equal Employment Opportunity", "whistleblower complaint", "zero-tolerance diversity policy", "parental leave", "freedom from discrimination",
            "freedom from harassment", "freedom from violence", "reporting workplace harassment", "Commitment to women empowerment", "gender-sensitive language", "diversity"]

FOUND_KEYWORDS = set()


def pdf_to_text(path):
    """
    Extract a PDF's text while preserving it's layout (paragraphs and line breaks).

    Args:
        path (str): The file path of the PDF.

    Returns:
        str: The extracted text in the form a string.
    """
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    filepath.close()
    device.close()
    retstr.close()

    return text.decode('utf-8')


def get_relevant_text(text):
    """
    Finds relevant text (paragraph) containing any of the keywords.

    Args:
        text (str): The extracted PDF text.

    Return:
        str: The list of paragraphs containing relevant text that contains any of the keywords joined by " | ".
    """
    global FOUND_KEYWORDS
    relevant_text_list = []
    final_relevant_text = ""
    
    split_text = text.split("\n\n")

    for keyword in KEYWORDS:
        for paragraph in split_text:
            lower_keyword = keyword.lower()
            lower_paragraph_split = (paragraph.lower()).replace("\n", " ")
            if lower_keyword in lower_paragraph_split:
                FOUND_KEYWORDS.add(keyword)
                relevant_text_list.append(paragraph.replace("\n", " "))

    # Check for multiple paragraphs containing keywords in same document. Append with " | " into a single string.
    if len(relevant_text_list) > 1:
        for index, paragraph in enumerate(relevant_text_list):
            if index == 0:
                final_relevant_text += paragraph
            else:
                final_relevant_text += " | "
                final_relevant_text += paragraph
    else:
        final_relevant_text = relevant_text_list[0]


    return final_relevant_text


def get_source(text):
    """


    Args:
        text ([type]): [description]

    Returns:
        str: The author of the PDF document.
    """


if __name__ == '__main__':
    # Path of document
    path = 'documents/test3.pdf'

    # Extracted text
    text = pdf_to_text(path)

    # print(text)

    # Get the relevant text containing keywords from the document
    relevant_text = get_relevant_text(text)

    final_extraction = {"relevant_text": relevant_text, "keywords": FOUND_KEYWORDS}

    print(final_extraction)


    # TODO:
    # 1. Extract the date of the event. This may or may not be the same date of the news piece.
    # 2. Extract the author of the piece. 
    #       a. This may be preceded by "SOURCE" or "Source:"
    # 3. Extract the subjects. A document may or may not have this. 
    #       a. If any, will be preceded by "Subjects":