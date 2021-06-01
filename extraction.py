import os
import sys
import csv
from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


KEYWORDS = ["gender inequality", "gender issue", "gender justice", "gender pay gap", "gender proud", "gender gap", "gendered violence",
            "sexual harassment", "sexism", "sexual assault", "sexual crime", "sexual harassment", "sexual misconduct", "sexual violence", "sexual abuse", "sexual accusation",
            "sexually harrasing", "sexually harassed", "sexually assaulting", "sexually assaulted", "sexually abusing", "sexually abused",
            "domestic violence", "intimate partner violence", "misogyny", "hashtag activism", "feminism", "feminist", "misogyny",
            "gender equality", "Chief Diversity Officer", "Diversity and Inclusion", "Diversity & Inclusion", "D&I", "diversity delegate", "sexism awareness",
            "code of conduct on sexual harassment", "anti-harassment policy and complaint", "anti-discrimination and harassment policy", "Sexual Harassment Prevention Training",
            "bystander intervention", "Equal Employment Opportunity", "whistleblower complaint", "zero-tolerance diversity policy", "parental leave", "freedom from discrimination",
            "freedom from harassment", "freedom from violence", "reporting workplace harassment", "Commitment to women empowerment", "gender-sensitive language", "diversity"]

# Here we account for different variations of the keywords

hyphen_keywords = []
for keyword in KEYWORDS:
    hyphen_keywords.append(keyword.replace(" ", "-"))

KEYWORDS += hyphen_keywords

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
    FOUND_KEYWORDS = set()
    relevant_text_list = []
    final_relevant_text = ""
    
    split_text = text.split("\n\n")

    # for p in split_text:
    #     print(p)
    #     print('\n')

    for keyword in KEYWORDS:
        for paragraph in split_text:
            lower_keyword = keyword.lower()
            lower_paragraph_split = (paragraph.lower()).replace("\n", " ")
            # print(lower_paragraph_split)
            if lower_keyword in lower_paragraph_split and paragraph.replace("\n", " ") not in relevant_text_list:
                FOUND_KEYWORDS.add(keyword)
                relevant_text_list.append(paragraph.replace("\n", " "))

    # Check for multiple paragraphs containing keywords in same document. Append with " | " into a single string.
    if relevant_text_list:
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
    Gets the author of the document from the extracted text. If source can be found, we will leave it blank.

    Args:
        text (str): The extracted PDF text.

    Returns:
        str: The author of the PDF document.
    """
    source = ""

    split_text = text.split("\n\n")

    # Searching for the source using "SOURCE ", "Source: "
    for paragraph in split_text:
        if "SOURCE " in paragraph:
            partition = paragraph.partition("SOURCE ")
            unclean_source = partition[2]
            source = unclean_source.partition("\n")[0].strip()
            break
        elif "Source: " in paragraph:
            partition = paragraph.partition("Source: ")
            unclean_source = partition[2]
            source = unclean_source.partition("\n")[0].strip()
            break


    return source


def get_subjects(text):
    """
    Gets the subjects of the document from the extracted text if they exist.

    Args:
        text (str): The extracted PDF text.

    Returns:
        str: The subjects of the PDF document.
    """ 
    subjects = ""
    
    split_text = text.split("\n\n")

    # Search for "Subjects:" line in paragraph
    for paragraph in split_text:
        if "Subjects: " in paragraph:
            partition = paragraph.partition("Subjects: ")
            subjects = partition[2].replace("\n", " ").strip()
            break

    return subjects


def produce_final_extraction(text, path):
    """
    Produces the final extraction of keywords, relevant text, source, and subjects from the extracted text.

    Args:
        text (str): The extracted PDF text.
        path (str): The PDF's file path.

    Returns:
        dict: The dictionary containing values for the 4 queries listed above.
    """
    # Get the relevant text containing keywords from the document
    # This also produces the keywords
    relevant_text = get_relevant_text(text).strip()

    # Record the number of paragraphs and their word counts
    paragraphs = relevant_text.split(" | ")
    words = ""
    for pid, paragraph in enumerate(paragraphs):
        if pid == 0:
            if words:
                words = str(len(paragraph.split()))
            else:
                words = ""
        else:
            words += ", "
            words += str(len(paragraph.split()))

    # Get the source of the document
    source = get_source(text)

    # Get the subject of the document
    subject = get_subjects(text)

    if FOUND_KEYWORDS:
        keywords = ""
        for index, keyword in enumerate(FOUND_KEYWORDS):
            if index == 0:
                keywords += keyword
            else:
                keywords += ", "
                keywords += keyword
        final_extraction = {"relevant_text": relevant_text, "paragraphs": len(paragraphs), "words": words,
                            "keywords": keywords, "who_wrote_the_piece": source, "subject": subject, "path": path}
    else:
        final_extraction = {"relevant_text": relevant_text, "paragraphs": "", "words": words,
                            "keywords": "", "who_wrote_the_piece": source, "subject": subject, "path": path}

    return final_extraction


if __name__ == '__main__':
    # Open directory containing the PDF files and append the file names to our list of files
    files = []
    num = sys.argv[1]
    if not num:
        print("You did provide a dataset number.")
        sys.exit(1)
    
    with os.scandir(num + '/') as entries:   
        for entry in entries:
            files.append(entry.name)

    # Recreate the spreadsheet with correct column headings
    # Date/Time, Identifier(s), Headline, Source

    with open(num + "_new.csv", mode='w', encoding='utf-8', newline='') as new_input:    
        fieldnames = ["identifier", "headline", "date", "source"]
        writer = csv.DictWriter(new_input, fieldnames=fieldnames)

        writer.writeheader()

        for file in files:
            split_path = file.split("-")
            identifier = split_path[0].strip()
            headline = split_path[1].strip()
            date = (split_path[2] + "-" + split_path[3] + "-" + split_path[4]).strip()
            source = (split_path[5].split(".")[0]).strip()

            # print(identifier)
            # print(headline)
            # print(date)
            # print(source)
            # print('\n')

            file_info = {"identifier": identifier, "headline": headline, "date": date, "source": source}
            writer.writerow(file_info)


    # Go through each file and query for the requested fields
    for id, file in enumerate(files):
        text = pdf_to_text(num + "/" + file)     
        final_extraction = produce_final_extraction(text, file)
        print(final_extraction)
        print("\n")

        # Open our tmp file for writing/storing the queries - 
        with open(num + "_tmp.csv", mode='a', encoding='utf-8', newline='') as output:      
            fieldnames = ["who_wrote_the_piece", "subject", "relevant_text", "paragraphs", "words", "keywords", "path"]
            writer = csv.DictWriter(output, fieldnames)

            if id == 0:
                writer.writeheader()

            writer.writerow(final_extraction)


    # text = pdf_to_text("20_examples/AFL - Aflac Incorporated Announces First Quarter Results, Reports First Quarter Net Earnings of $566 Million, Withdraws Annual Adjusted EPS Guida... - 29-Apr-20 - PRN.pdf")
    # print(produce_final_extraction(text, ""))
