# Knowledge extraction from complex table

Large Language Models (LLMs) like GPT-4 (ChatGPT), AskyourPDF, and Unstract have demonstrated notable capabilities in extracting and understanding information from tables in raw PDF. However, __complex tables__ often contain various advanced features such as multiple column items (columns that span more than one field), merged cells (span multiple rows or columns), parenthetical explanations, and superscripts with corresponding footnotes or annotations, all of which pose significant challenges for table extraction and understanding. These features demand a high level of precision and contextual awareness from extraction tools. 

[Final Report on Knowledge Extraction](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/Final%20Report%20on%20Knowledge%20Extraction.pdf) evaluates the performance of several LLMs in table knowledge extraction and understanding. Recognizing the inherent limitations of LLMs in processing unstructured table data, the report introduces a preprocessing pipeline that utilizes Optical Character Recognition and rule-based methods to reconstruct tables into structured data formats, aiming to improve the accuracy and reliability of LLMs when handling tabular content. The code is in [code.py](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/code.py) based on screenshot table images.

a sample table in 'Bank tariff guide for HSBC Wealth and Personal Banking Customers':
![a sample table](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/biao.png)

Follow the code through four main steps, handling each output csv in each step accordingly:  
1. Extract and Save Text with Coordinates from the Image  
2. Merge Text into Blocks Based on Row Distance  
3. Merge Text Blocks into Cells Based on Column Distance  
4. Reconstruct and Output the Original Table  
The final result will be an organized table of your original table image saved as organized_table.csv, effectively addressing challenges such as multi-field columns, merged cells, and superscripts referencing footnotes or annotations in complex tables.
   
[Knowledge extraction tools](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/Knowledge%20extraction%20tools.pdf) collects some knowledge extraction tools, including Document Parser supporting PDF (some support extractions of tables in PDF for LLM), OCR-based Document Parser supporting PDF, Layout Analysis, and other types of tools.

# Improvements

I further designed few-shot and chain-of-thought (COT) prompts to test the ability of LLMs to perform table information extraction, understanding, and reasoning tasks. Langchain...

## Python Requirements:
cv2
<br>pytesseract
<br>pandas

## How to Run:
```python code.py```

## Prompt strategies  
In the report, the prompts are designed in a zero-shot style, such as "Summarize the ways to save money" and "I have a Personal Integrated Account, how much does it cost me to have a cashier's check?". The results reveal that while LLMs demonstrate strong abilities in locating and summarizing information, they fall short in understanding and reasoning tasks involving tables.

To address this limitation, I further adopt few-shot and chain-of-thought (COT) prompting to investigate whether the performance of GPT-4o could be improved in table understanding and reasoning tasks, using the sample table shown above.

(Few-shot)[https://arxiv.org/pdf/2012.15723]
one-shot
two-shot

(zero-shot COT)[https://arxiv.org/pdf/2205.11916]
task agnostic and cheap

(few-shot COT)[https://arxiv.org/pdf/2201.11903]
improve OOD generalization

### Discussions

As mentioned in (Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?)[https://arxiv.org/pdf/2202.12837], ground truth demonstrations are in fact not required—randomly replacing labels in the demonstrations barely hurts performance on a range of classification and multi-choce tasks. using the demonstrations significantly outperforms the no demonstrations method even with small k (k = 4),  model performance does not increase much as k increases when k ≥ 8, both with gold labels and with random labels.  in-distribution inputs and  conditioning on the label space in the demonstrations substantially contribute to performance gains. For all of these cases, removing inputs instead of using OOD inputs, or removing labels instead of using random English words is significantly worse, indicating that keeping the format of the input-label pairs is key

table is generation task

#### Possible future directions

(prompt templates)[https://prompts.chat/]

(AUTOPROMPT)[https://arxiv.org/pdf/2010.15980] an automated method to create prompts for a diverse set of tasks, based on a gradient-guided search

(Black-Box Prompt Optimization)[https://arxiv.org/pdf/2311.04155] optimize user prompts to enhances LLMs’ alignment to human preferences without updating LLMs’ parameters, outperforming the same models aligned by RLHF, PPO and DPO

