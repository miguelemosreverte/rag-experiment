# File Format Converter Tool

## Description
Converts files between common formats: PDF, DOCX, HTML, Markdown, CSV, JSON, XLSX, and plain text. Uses `pandoc` as the backend for document conversions and `openpyxl` for spreadsheet operations.

## Parameters
- `input_path` (required): Path to the source file.
- `output_format` (required): Target format. One of: "pdf", "docx", "html", "md", "csv", "json", "xlsx", "txt".
- `output_path` (optional): Where to save the converted file. Default: same directory, new extension.
- `options` (optional): Format-specific options as a dict.

## Supported Conversions
| From | To |
|------|-----|
| PDF | txt, md, html, docx |
| DOCX | pdf, html, md, txt |
| HTML | pdf, docx, md, txt |
| Markdown | pdf, docx, html |
| CSV | json, xlsx |
| JSON | csv, xlsx |
| XLSX | csv, json |

## Example Usage
```python
result = convert_file(
    input_path="/documents/report.docx",
    output_format="pdf",
    options={"page_size": "A4", "margin": "1in"}
)
# Returns: {"output_path": "/documents/report.pdf", "size_bytes": 245832, "pages": 12}
```

## PDF-Specific Options
- `page_size`: "letter", "A4", "legal". Default: "letter".
- `margin`: Margin size. Default: "1in".
- `font_size`: Base font size. Default: 12.
- `toc`: Include table of contents. Default: false.

## Spreadsheet Options
- `sheet_name`: For XLSX with multiple sheets. Default: first sheet.
- `header_row`: Row number containing headers. Default: 1.
- `delimiter`: For CSV output. Default: comma.

## Limitations
- Maximum file size: 50MB
- PDF to text extraction quality depends on PDF structure (scanned PDFs may need OCR)
- Complex formatting (tables, images) may not survive all conversion paths
