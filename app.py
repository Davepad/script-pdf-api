from flask import Flask, request, jsonify
from fpdf import FPDF
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta donde se guardarán los PDFs
OUTPUT_FOLDER = "static/converted"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Guion en PDF", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def chapter_body(self, text):
        self.set_font("Arial", "", 12)
        lines = text.split("\n")
        for line in lines:
            self.multi_cell(0, 10, line)
            self.ln()

@app.route("/convertir-pdf", methods=["POST"])
def convertir_pdf():
    data = request.get_json()
    texto_guion = data.get("texto_guion", "")
    
    if not texto_guion:
        return jsonify({"error": "Falta el campo 'texto_guion'"}), 400

    # Nombre del archivo basado en la primera línea del guion
    primera_linea = texto_guion.split("\n")[0].strip().replace(" ", "_")
    nombre_archivo = f"{primera_linea}.pdf"
    ruta_archivo = os.path.join(OUTPUT_FOLDER, nombre_archivo)

    # Crear el PDF
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(texto_guion)
    pdf.output(ruta_archivo)

    # Construir URL absoluta
    pdf_url = f"{request.host_url}static/converted/{nombre_archivo}"
    
    return jsonify({"pdf_url": pdf_url}), 200

if __name__ == "__main__":
    app.run(debug=True)
