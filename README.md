# Knowledge extraction and reasoning from complex table

Large Language Models (LLMs) like **GPT-4 (ChatGPT)**, **AskyourPDF**, and **Unstract** have demonstrated notable capabilities in extracting and understanding information from tables in raw PDF. However, __complex tables often contain various advanced features such as multiple column items (columns that span more than one field), merged cells (span multiple rows or columns), parenthetical explanations, and superscripts with corresponding footnotes or annotations__, all of which pose significant challenges for table extraction and understanding. These features demand a high level of precision and contextual awareness from extraction tools. 

[Final Report on Knowledge Extraction](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/Final%20Report%20on%20Knowledge%20Extraction.pdf) evaluates the performance of several LLMs in table knowledge extraction and understanding. Recognizing the inherent limitations of LLMs in processing unstructured table data, the report introduces a preprocessing pipeline that utilizes Optical Character Recognition and rule-based methods to reconstruct tables into structured data formats, aiming to improve the accuracy and reliability of LLMs when handling tabular content. The code is in [code.py](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/code.py) based on screenshot table images.

a sample table in 'Bank tariff guide for HSBC Wealth and Personal Banking Customers':
![a sample table](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/biao.png)

Follow the code through four main steps, handling each output csv in each step accordingly:  
1. Extract and Save Text with Coordinates from the Image  
2. Merge Text into Blocks Based on Row Distance  
3. Merge Text Blocks into Cells Based on Column Distance  
4. Reconstruct and Output the Original Table
   
The final result will be an organized table of your original table image saved as ```organized_table.csv```, **effectively addressing challenges such as multi-field columns, merged cells, and superscripts referencing footnotes or annotations in complex tables.**
   
Additionally, [Knowledge extraction tools](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/Knowledge%20extraction%20tools.pdf) collects some knowledge extraction tools, including Document Parser supporting PDF (some support extractions of tables in PDF for LLM), OCR-based Document Parser supporting PDF, Layout Analysis, and other types of tools.

# Improvements

I further designed **few-shot** and **chain-of-thought (COT)** prompts to test the ability of LLMs to perform table information extraction, understanding, and reasoning tasks.  
Langchain...The lines extracted by **LangChain’s PyPDFLoader** are in the same order as the original PDF, achieving a **100%** recognition accuracy for the aforementioned table PDF, including special symbols and superscripts.

## Python Requirements:
cv2
<br>pytesseract
<br>pandas  
langchain  
pypdf

## How to Run:
```
python code.py
```
```
python document.py      # using LangChain’s PyPDFLoader to extract information from tables
```


## Prompt strategies  
In the report, the prompts are designed in a **zero-shot** style, such as ```"Summarize the ways to save money"``` and ```"I have a Personal Integrated Account, how much does it cost me to have a cashier's check?"```. The results reveal that while LLMs demonstrate strong abilities in locating and summarizing information, they fall short in understanding and reasoning tasks involving tables.

To address this limitation, I further adopt **few-shot** and **chain-of-thought (COT)** prompting to investigate whether the performance of GPT-4o could be improved in table understanding and reasoning tasks, using the sample table shown above.

[Few-shot](https://arxiv.org/pdf/2012.15723) for knowledge extraction:  

**1. one-shot**  
The answers to the following three questions correspond to cell located in the same row as the demostration, the same column as the demostration, different row and column from the demostration, respectively.   
The first two answers are correct, but the third answer is sometimes correct and sometimes incorrect, indicating that the LLM still has limitations in accurately identifying the relative row and column positions of cells.
 
![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/1.png)  
![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/2.png)  
![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/11.png)
![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/12.png)

The following two questions are the same but with different demonstrations: the demonstration for the first question is the cell (HK$60) to the right of the answer cell, while the demonstration for the second question is the cell two cells to the right of the answer cell.   
The answer corresponds to cell located **within a merged cell** (the question was incorrectly answered (HK$60) by **GPT-4o** in a **zero-shot** style in the original report).   
The second answer is incorrect (HK$60), and even if the first answer is correct, it might be because the demonstration helped eliminate the wrong answer.

![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/13.png)
![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/14.png)

**2. two-shot**  
The answer corresponding to cell in the same row as the input is also answered correctly.

![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/3.png)

[Zero-shot COT](https://arxiv.org/pdf/2205.11916) for reasoning:  
Task-agnostic and cheap  

![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/4.png)  

Surprisingly, it produced the correct answer and recognized the footnotes simply by adding ```"Let's think step by step"```!  
It seems there’s no need to follow the two-step approach outlined in the original paper — it managed to succeed in just one step.  

![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/1.pic.jpg)

[Few-shot COT](https://arxiv.org/pdf/2201.11903) for reasoning:  
It can improve OOD generalization.  

![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/5.png)  

The reasoning chain is correct, but it’s somewhat like cheating since both questions share the same footnotes.  

Answering the following question requires a different footnote than the one used in the demonstration.  

![](https://github.com/WillongWANG/Knowledge-extraction-from-complex-table/blob/main/pics/6.png)  

The reasoning chain is also correct.

It seems that **COT** helps the LLM reason to arrive at the correct answer. However, further testing is needed in more complex situations, such as multi-field columns and merged cells.

### Discussions

As mentioned in [Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?](https://arxiv.org/pdf/2202.12837), the factors influencing model performance in **few-shot** learning are as follows:
1. Using demonstrations significantly outperforms the no-demonstration method. Even with small k (k = 4), model performance doesn’t increase much as k increases when k ≥ 8, both with gold labels and random labels.  
2. Ground truth demonstrations are not required — replacing labels randomly in the demonstrations barely affects performance on a range of classification and multi-choice tasks.
3. In-distribution inputs and conditioning on the label space in the demonstrations contribute substantially to performance gains.
4. Removing inputs instead of using OOD inputs, or removing labels instead of using random English words is significantly worse, indicating that keeping the format of the input-label pairs is key.

Therefore, to better leverage **few-shot** prompts, we need to explore and adopt the input distribution, label space, and the format of the input-label pairs related to table understanding in **GPT-4o** training data. Additionally, table understanding is a more complex generation task, involving extracting and reasoning based on unstructured input files. This task differs from the classification tasks addressed in the original paper and is somewhat not the same as in-context learning.

#### Possible future directions

1. Use carefully crafted [prompt templates](https://prompts.chat/)

2. [AUTOPROMPT](https://arxiv.org/pdf/2010.15980): an automated method to create prompts for a diverse set of tasks, based on a gradient-guided search

3. [Black-Box Prompt Optimization](https://arxiv.org/pdf/2311.04155): optimize user prompts to enhances LLMs’ alignment to human preferences without updating LLMs’ parameters, outperforming the same models aligned by RLHF, PPO and DPO

