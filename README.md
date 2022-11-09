# mixer
mixing questions in a test.docx

# flow
- libre to save docx as html (not export) (to preserve all the images of equations and subscripts)
- python to mix and output the tests (in html) with its answers (txt)
- libre writer to save html as docx, then export to pdf to preserve all the images

# input format
#### docx file should be formatted properly:
- mark the letter of the answer with underline (underline A for example)
- there is only two dots in each answer, after the letter and at the end: "A. here comes the answer A. "

# python steps
- silent all the style
- collect questions in ol tags
- shuffle the questions
- shuffle the answer, save the answer (underlined)
- output mixed test + its answers
