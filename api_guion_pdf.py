from flask import Flask, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)

@app.route('/convertir-pdf', methods=['POST'])
def convertir_pdf():
    data = request.json
    texto = data.get('texto_guion', '')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Courier", size=12)

    for line in texto.split('\n'):
        pdf.multi_cell(0, 10, line)

    output_path = "/tmp/guion_convertido.pdf"
    pdf.output(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
