from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

loader = PyPDFLoader("/Users/yingmanyouyu/Desktop/Desktop/knowledge_extraction_from_table/table.pdf")
pages = loader.load()

print(len(pages))
page = pages[0]
print(page.page_content)
print("\n\n\n")

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=100,
    chunk_overlap=0,
    length_function=len
)
docs = text_splitter.split_documents(pages)
for d in docs:
 print(d.page_content)

with open("output.txt", "w", encoding="utf-8") as file:
    file.write(page.page_content)