import fitz  # PyMuPDF

# 将毫米转换为 PDF 用户单位（1 pt = 1/72 inch, 1 inch = 25.4 mm）
def mm_to_pt(mm):
    return mm * 72 / 25.4  # 1 mm = 2.83465 pt

# 你的 PDF 文件路径
pdf_path = "233.pdf"
output_pdf = "output23.pdf"

# 打开 PDF
doc = fitz.open(pdf_path)

# 选择第二页（索引从 0 开始）
page_number = 1  # 第二页
page = doc[page_number]

x,y = 92.81,5.91
# 你的目标坐标（从 PDF XChange Editor 获取的毫米坐标）
x_mm, y_mm = 57.05, 206.54

# 转换为 PDF 坐标（单位 pt）
x_pt = mm_to_pt(x_mm - x/2)
y_pt = mm_to_pt(y_mm - y/2)

# 适配 PyMuPDF 坐标系（从底部计算）
page_height = page.rect.height  # 获取页面总高度
adjusted_y_pt = page_height - y_pt  # 调整 Y 轴坐标

# 添加文本
text = "Magicxxxx"  # 你要写入的文本
page.insert_text((x_pt, adjusted_y_pt), text, fontsize=12, color=(1, 0, 0))  # 颜色为红色

# 保存文件
doc.save(output_pdf)
doc.close()

print(f"文本已成功填充到 第 {page_number + 1} 页 {x_mm} mm, {y_mm} mm 对应的 PDF 位置！")
