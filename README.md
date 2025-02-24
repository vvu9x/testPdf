# [PdfApi](https://github.com/vvu9x/testPdf.git)
for pdf input
# PDF Auto-Fill API

## Overview
This API allows users to upload a PDF file and provide structured data to automatically fill specific fields in the document. It supports text input, multi-line text, date fields, and multiple-choice selections.

## Features
- Upload a PDF file
- Fill text fields
- Handle multi-line text (e.g., addresses, phone numbers)
- Populate date fields (day, month, year)
- Mark multiple-choice selections (e.g., yes/no options)
- Download the modified PDF

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/vvu9x/PdfApi.git
   cd PdfApi
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the API:
   ```sh
   python app.py
   ```

## API Endpoints
### 1. Upload and Fill PDF
**Endpoint:**
```
POST /upload
```
**Request Parameters:**
- **pdf** (File) - The PDF file to be processed
- **data** (JSON) - JSON object containing form field values

**Example Request (Postman or cURL):**
```sh
curl -X POST "http://127.0.0.1:5000/upload" \
    -F "pdf=@path/to/your/file.pdf" \
    -F 'data={
        "family_name": "Smith",
        "date_of_birth": { "dd": "25", "mm": "08", "yyyy": "1995" },
        "do_you_need_driving": "yes"
    }'
```

**Example JSON Data:**
```json
{
    "family_name": "Smith",
    "date_of_birth": {
        "dd": "25",
        "mm": "08",
        "yyyy": "1995"
    },
    "do_you_need_driving": "yes"
}
```

**Response:**
- Returns the filled PDF file as an attachment.

## Configuration (config.json)
The API uses a `config.json` file to map data fields to their positions in the PDF.

### Example `config.json`
```json
{
    "family_name": [
        {
            "page": 1,
            "type": "text",
            "positions": [
                {"x": 57.05, "y": 218.04, "width": 92.81, "height": 5.91}
            ]
        }
    ],
    "date_of_birth": [
        {
            "page": 1,
            "type": "multi_text",
            "positions": {
                "dd": {"x": 17.13, "y": 195.37, "width": 13.73, "height": 4.82},
                "mm": {"x": 30.18, "y": 195.58, "width": 13.73, "height": 4.82},
                "yyyy": {"x": 43.34, "y": 194.84, "width": 13.73, "height": 4.82}
            }
        }
    ],
    "do_you_need_driving": [
        {
            "page": 1,
            "type": "choice",
            "positions": {
                "no": {"x": 118.11, "y": 192.26, "width": 4, "height": 4},
                "yes": {"x": 133.86, "y": 192.26, "width": 3.91, "height": 3.91}
            }
        }
    ]
}
```

## Error Handling
- `400 Bad Request`: If the required parameters (`pdf` or `data`) are missing.
- `500 Internal Server Error`: If there is an unexpected issue processing the PDF.

## License
This project is licensed under the MIT License.
