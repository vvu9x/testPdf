from flask import Flask, request, send_file, jsonify
import fitz  # PyMuPDF
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
CONFIG_FILE = "config.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def mm_to_pt(mm):
    return mm * 72 / 25.4  # 1 mm = 2.83465 pt

def adjust_coordinates(x_mm, y_mm, x_offset, y_offset):
    return mm_to_pt(x_mm - x_offset / 2), mm_to_pt(y_mm - y_offset / 2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@app.route("/upload", methods=["POST"])
def upload_and_fill_pdf():
    if "pdf" not in request.files or "data" not in request.form:
        return jsonify({"error": "Missing PDF file or data"}), 400

    pdf_file = request.files["pdf"]
    user_data = json.loads(request.form["data"])  # 解析用户输入数据
    config = load_config()  # 加载配置文件
    
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)
    output_pdf_path = os.path.join(OUTPUT_FOLDER, f"filled_{pdf_file.filename}")
    
    doc = fitz.open(pdf_path)
    
    for field_name, value in user_data.items():
        if field_name not in config:
            continue  # 跳过未定义的字段
        
        for entry in config[field_name]:
            page_number = entry.get("page", 1) - 1  # 页码从 1 开始，转换为索引
            if page_number >= len(doc):
                continue  # 防止索引越界
            
            page = doc[page_number]
            page_height = page.rect.height  # 获取页面总高度
            field_type = entry.get("type", "text")  # 默认类型
            
            if field_type == "multi_text":  # 处理多行文本(或者多框文本)
                for key, subvalue in value.items():
                    if key in entry["positions"]:
                        pos = entry["positions"][key]
                        x_pt, y_pt = adjust_coordinates(pos["x"], pos["y"], pos["width"], pos["height"])
                        adjusted_y_pt = page_height - y_pt
                        page.insert_text((x_pt, adjusted_y_pt), subvalue, fontsize=12, color=(0, 0, 0))
            elif field_type == "choice":  # 处理选择题，画 X
                if value.lower() in entry["positions"]:
                    pos = entry["positions"][value.lower()]
                    x_pt, y_pt = adjust_coordinates(pos["x"], pos["y"], pos["width"], pos["height"])
                    adjusted_y_pt = page_height - y_pt
                    page.insert_text((x_pt, adjusted_y_pt), "X", fontsize=12, color=(0, 0, 0))
            else:  # 普通文本处理
                for position in entry.get("positions", []):
                    x_pt, y_pt = adjust_coordinates(position["x"], position["y"], position["width"], position["height"])
                    adjusted_y_pt = page_height - y_pt
                    page.insert_text((x_pt, adjusted_y_pt), value, fontsize=12, color=(0, 0, 0))
    
    doc.save(output_pdf_path)
    doc.close()
    
    return send_file(output_pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)