'''
def extract_text_from_image(image):
    # 使用 OCR 检测表格内容
    config = '--psm 6'  # 页面分割模式 6，假设有一堆相互关联的文本块
    text = pytesseract.image_to_string(image, config=config)
    
    return text

#binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# 检测水平和垂直线条
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
horizontal_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
vertical_lines = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

# 合并线条以形成单元格边框
table_structure = cv2.add(horizontal_lines, vertical_lines)

# 寻找线条的交点（即单元格的四角）
corners = cv2.bitwise_and(horizontal_lines, vertical_lines)
contours, _ = cv2.findContours(corners, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 获取单元格的边界坐标
cells = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 10 and h > 10:  # 排除过小的噪声区域
        cells.append((x, y, x + w, y + h))

# 按 y 坐标排序，组织为行
cells = sorted(cells, key=lambda b: (b[1], b[0]))

# 识别每个单元格中的文本
data = []
current_row = []
previous_y = cells[0][1]

for (x1, y1, x2, y2) in cells:
    # 如果当前单元格在新的一行，保存上一行的数据
    if y1 > previous_y + 10:  # 假设行间距大于10像素
        data.append(current_row)
        current_row = []
        previous_y = y1

    # 提取单元格图像
    cell_image = image[y1:y2, x1:x2]
    
    # 使用 OCR 识别文本
    cell_text = pytesseract.image_to_string(cell_image, config='--psm 6').strip()
    if cell_text:  # 仅存储非空内容
        print(f"识别到的文本: '{cell_text}' at位置: {(x1, y1, x2, y2)}")  # 调试打印
        current_row.append((cell_text, (x1, y1, x2, y2)))  # 存储单元格内容和坐标
'''
import cv2   
import pytesseract
import pandas as pd

# 配置 Tesseract 可执行文件路径（如果需要）
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# 读取图像
image_path = '/Users/yingmanyouyu/Desktop/knowledge_extraction_from_table/biao.png'
output_path='/Users/yingmanyouyu/Desktop/1.csv'
image = cv2.imread(image_path)

# 转为灰度图像并二值化（增强文字区域）
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 使用 Tesseract OCR 提取文字及坐标
custom_config = r'--oem 3 --psm 6'
results = pytesseract.image_to_data(binary, config=custom_config, output_type=pytesseract.Output.DICT)

# 将提取的文字和坐标存入 DataFrame
data = pd.DataFrame({
    "text": results["text"],
    "left": results["left"],
    "top": results["top"],
    "width": results["width"],
    "height": results["height"]
})

# 过滤掉空白文本
data = data[data["text"].str.strip() != ""]

# 添加 right 和 bottom 坐标
data["right"] = data["left"] + data["width"]
data["bottom"] = data["top"] + data["height"]

# 计算中心点
data["center_x"] = data["left"] + data["width"] / 2
data["center_y"] = data["top"] + data["height"] / 2

data.to_csv(output_path, index=False)
print(f"字符及坐标数据已保存到：{output_path}")

for i, row in data.iterrows():
    x1, y1, x2, y2 = row["left"], row["top"], row["right"], row["bottom"]
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绿色矩形框

cv2.imshow("Bounding Boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()    


# 读取 CSV 文件
df = pd.read_csv("2.csv")

# 存储合并后的文本列表
texts = []  # 每个文本是一个字典，包含字符列表及其上下边界
visited = set()  # 标记已处理的字符索引

# 遍历字符列表
for i in range(len(df)):
    if i in visited:  # 跳过已处理的字符
        continue
    
    # 初始化当前文本
    current_text = [df.loc[i, "text"]]  # 存储当前文本的字符
    current_top = df.loc[i, "top"]  # 初始化文本的 top
    current_bottom = df.loc[i, "bottom"]  # 初始化文本的 bottom
    visited.add(i)  # 标记当前字符为已处理

    # 当前字符的坐标信息
    current_left = df.loc[i, "left"]
    current_right = df.loc[i, "right"]

    # 从当前字符开始合并后续字符
    for j in range(i + 1, len(df)):
        if j in visited:  # 跳过已处理的字符
            continue
        
        # 后续字符的坐标信息
        next_left = df.loc[j, "left"]
        next_right = df.loc[j, "right"]
        next_top = df.loc[j, "top"]
        next_bottom = df.loc[j, "bottom"]
        
        # 判断是否是同一个文本
        if (0 < next_left - current_right < 57) and ((next_top <= current_bottom and next_top >= current_top) or (current_top <= next_bottom <= current_bottom) or (next_top >= current_top and next_bottom <= current_bottom) or (next_top <= current_top and next_bottom >= current_bottom)):
            # 合并字符
            current_text.append(" ")
            current_text.append(df.loc[j, "text"])
            # 更新边界
            current_top = min(current_top, next_top)
            current_bottom = max(current_bottom, next_bottom)
            current_left=min(current_left,next_left)
            current_right=max(current_right,next_right)
            visited.add(j)  # 标记为已处理

    # 将合并后的文本及其上下边界保存
    texts.append({
        "text": "".join(current_text),  # 合并字符为文本
        "top": current_top,  # 最小 top
        "bottom": current_bottom,  # 最大 bottom
        "left":current_left,
        "right":current_right
    })

# 保存结果到文件
output_file = "merged_texts.csv"
result_df = pd.DataFrame(texts)
result_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"合并后的文本已保存至 {output_file}")


# 读取 merged_texts.csv 文件
df = pd.read_csv("merged_texts.csv")

# 存储最终合并后的文本列表
merged_texts = []  # 每个文本段是一个字典，包含合并的文本及其边界
visited = set()  # 标记已处理的文本段索引

# 遍历文本段列表
for i in range(len(df)):
    if i in visited:  # 跳过已处理的文本段
        continue
    
    # 初始化当前文本段
    current_texts = [df.loc[i, "text"]]  # 存储当前文本段的内容
    current_top = df.loc[i, "top"]  # 初始化 top
    current_bottom = df.loc[i, "bottom"]  # 初始化 bottom
    current_left = df.loc[i, "left"]  # 初始化 left
    current_right = df.loc[i, "right"]  # 初始化 right
    visited.add(i)  # 标记当前文本段为已处理

    # 从当前文本段开始合并后续文本段
    for j in range(i + 1, len(df)):
        if j in visited:  # 跳过已处理的文本段
            continue
        
        # 后续文本段的坐标信息
        next_top = df.loc[j, "top"]
        next_bottom = df.loc[j, "bottom"]
        next_left = df.loc[j, "left"]
        next_right = df.loc[j, "right"]
        
        # 判断是否是同一个文本段
        if (-4 < next_top - current_bottom < 8) and ((next_left <= current_right and next_left >= current_left) or (current_left <= next_right <= current_right) or (next_left >= current_left and next_right <= current_right) or (next_left <= current_left and next_right >= current_right)):
            # 合并文本内容
            current_texts.append(df.loc[j, "text"])
            # 更新边界
            current_top = min(current_top, next_top)
            current_bottom = max(current_bottom, next_bottom)
            current_left = min(current_left, next_left)
            current_right = max(current_right, next_right)
            visited.add(j)  # 标记为已处理

    # 将合并后的文本段及其边界保存
    merged_texts.append({
        "text": " ".join(current_texts).strip(),  # 合并文本内容
        "top": current_top,
        "bottom": current_bottom,
        "left": current_left,
        "right": current_right
    })

# 保存结果到文件
output_file = "final_merged_texts.csv"
result_df = pd.DataFrame(merged_texts)
result_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"合并后的文本段已保存至 {output_file}")


# 加载数据
df = pd.read_csv("final_merged_texts.csv")

# 列的初始定义（列名和对应的边界）
columns = [
    {"name": "Item", "top": 127, "bottom": 146, "left": 27, "right": 79},
    {"name": "Personal Customer", "top": 172, "bottom": 191, "left": 1056, "right": 1282},
    {"name": "Personal Integrated Account", "top": 154, "bottom": 211, "left": 1390, "right": 1660},
    {"name": "HSBC One", "top": 172, "bottom": 191, "left": 1780, "right": 2024},
    {"name": "HSBC Premier", "top": 172, "bottom": 191, "left": 2087, "right": 2319},
    {"name": "HSBC Jade", "top": 172, "bottom": 191, "left": 2420, "right": 2552},
]

if 'column' not in df.columns:
    df['column'] = None
# 添加列索引到每个文本段
for index, row in df.iterrows():
    if index in range(0,9):  # 跳过列标题行
        continue
    left, right = row["left"], row["right"]
    coll=[]
    assigned_column = False
    for col_index, col in enumerate(columns):
        # 如果文本段的 [left, right] 与某列的 [left, right] 有交集
        if ((left <= col["right"] and left >= col["left"]) or (col["left"] <= right <= col["right"]) or (left >= col["left"] and right <= col["right"]) or (left <= col["left"] and right >= col["right"])):
            coll.append(col_index)
            assigned_column = True
    df.at[index, "column"] = coll if coll else None
    print(f"{row['text']}   {coll}")
    if not assigned_column:
        print(f"警告: 文本段 '{row['text']}' 没有匹配到任何列。")

# 初始化存储行的列表
rows = []
visited = set()  # 用于标记已处理的文本段索引

# 遍历每一行文本段
for i in range(9,len(df)):
    if i in visited:  # 跳过未分配列的文本段
        continue

    # 初始化当前行，长度为总列数
    current_row = [""] * len(columns)
    assigned_columns = df.loc[i, "column"]  # 获取该文本段的列归属（可能是列表）

    if assigned_columns:
       for col in assigned_columns:
            current_row[col] = df.loc[i, "text"]

    # 初始化当前行的上下边界
    current_top = df.loc[i, "top"]
    current_bottom = df.loc[i, "bottom"]
    visited.add(i)  # 标记当前文本段已处理

    # 合并同一行的其他文本段
    for j in range(i + 1, len(df)):
        if j in visited:  # 跳过未分配列的文本段
            continue

        # 获取其他文本段的上下边界
        next_top = df.loc[j, "top"]
        next_bottom = df.loc[j, "bottom"]

        # 如果两个文本段在 [top, bottom] 有交集
        if not (next_top > current_bottom or next_bottom < current_top):  # 条件简化为没有交集时跳过
            assigned_columns = df.loc[j, "column"]

            if assigned_columns:
                for col in assigned_columns:
                    current_row[col] = df.loc[j, "text"]

            # 更新上下边界
            current_top = min(current_top, next_top)
            current_bottom = max(current_bottom, next_bottom)
            visited.add(j)  # 标记已处理

    rows.append(current_row)  # 添加当前行到结果列表

# 将结果保存到文件
output_df = pd.DataFrame(rows, columns=[col["name"] for col in columns])
output_file = "organized_table.csv"
output_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"组织化表格已保存至 {output_file}")

