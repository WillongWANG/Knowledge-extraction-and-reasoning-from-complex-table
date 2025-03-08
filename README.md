# Knowledge extraction from complex table

Large Language Models (LLMs) like GPT-4 (ChatGPT), AskyourPDF, and Unstract have demonstrated notable capabilities in extracting and understanding information from tables in raw PDF. However, __complex tables__ often contain various advanced features such as multiple column items (columns that span more than one field), merged cells (span multiple rows or columns), parenthetical explanations, and superscripts with corresponding footnotes or annotations, all of which pose significant challenges for table extraction and understanding. These features demand a high level of precision and contextual awareness from extraction tools. 

[Final Report on Knowledge Extraction](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/Final%20Report%20on%20Knowledge%20Extraction.pdf) evaluates the performance of several LLMs in table knowledge extraction and understanding. Recognizing the inherent limitations of LLMs in processing unstructured table data, the report introduces a preprocessing pipeline that utilizes Optical Character Recognition and rule-based methods to reconstruct tables into structured data formats, aiming to improve the accuracy and reliability of LLMs when handling tabular content. The code is in [code.py](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/code.py) based on screenshot table images.

a sample table
![a sample table](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/biao.png)

[Knowledge extraction tools](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/Knowledge%20extraction%20tools.pdf) collects some knowledge extraction tools, including Document Parser supporting PDF (some support extractions of tables in PDF for LLM), OCR-based Document Parser supporting PDF, Layout Analysis, and other types of tools.

## Python Requirements:
cv2
<br>pytesseract
<br>pandas

## How to Run:
python code.py

