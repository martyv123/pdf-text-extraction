# PDF Text Extraction

Preliminary research and starter code for extracting text from PDF files which contain press releases, company report, shareholder report and company statements. <br>

These keywords are presented below: <br>

```
KEYWORDS = ["gender inequality", "gender issue", "gender justice", "gender pay gap", "gender proud", "gender gap", "gendered violence",
            "sexual harassment", "sexism", "sexual assault", "sexual crime", "sexual harassment", "sexual misconduct", "sexual violence", "sexual abuse", "sexual accusation",
            "domestic violence", "intimate partner violence", "misogyny", "hashtag activism", "feminism", "feminist", "misogyny",
            "gender equality", "Chief Diversity Officer", "Diversity and Inclusion", "Diversity & Inclusion", "D&I", "diversity delegate", "sexism awareness",
            "code of conduct on sexual harassment", "anti-harassment policy and complaint", "anti-discrimination and harassment policy", "Sexual Harassment Prevention Training",
            "bystander intervention", "Equal Employment Opportunity", "whistleblower complaint", "zero-tolerance diversity policy", "parental leave", "freedom from discrimination",
            "freedom from harassment", "freedom from violence", "reporting workplace harassment", "Commitment to women empowerment", "gender-sensitive language", "diversity"]
```

We are searching for:
- Date of the event: note that this might or might not correspond with the actual date of the news piece (column A). The news can be reported the day after or refer to an event earlier on. 
- Who wrote the piece:  This information is found at the end of the document. 
- Subject: This information is found at the end of the document.
- Relevant text: this is the paragraph that contains one or more of our keywords; If there is more than one paragraph, please report them separated by | symbol (see example row 3).
- Keywords mentioned: please report the keywords mentioned in the paragraph.
- “Notes” column (K): includes the observations on whether the keywords are not central to the news piece. For instance, the news piece 2, is not directly about our keywords (i.e. donation to a hospital) but the keywords are just mentioned in the news piece. 
