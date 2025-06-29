from flask import Flask, request, send_file
from fpdf import FPDF
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "La API está funcionando correctamente"

@app.route('/convertir-pdf', methods=['POST'])
def convertir_pdf():
    data = request.get_json()
    texto = data.get('texto_guion', '')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)

    for line in texto.split('\n'):
        pdf.multi_cell(0, 10, line)

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/pdf',
        download_name='guion.pdf',
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
