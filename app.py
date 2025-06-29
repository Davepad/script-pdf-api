from flask import Flask, request, send_file, jsonify
from fpdf import FPDF
import io
import os
from pathlib import Path

app = Flask(__name__)

# ---------- Configuración ---------- #
FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"

# ---------- Generador de PDF ---------- #
def build_pdf(texto: str) -> io.BytesIO:
    pdf = FPDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Añadimos la fuente Unicode solo una vez
    pdf.add_font("DejaVu", "", FONT_PATH.as_posix(), uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 8, texto)

    return io.BytesIO(pdf.output(dest="S").encode("latin-1"))

# ---------- Rutas ---------- #
@app.route("/")
def home():
    return "✅ La API está viva y coleando 🐭"

@app.route("/convertir-pdf", methods=["POST"])
def convertir_pdf():
    data = request.get_json(silent=True) or {}
    texto = data.get("texto_guion", "")

    if not texto.strip():
        return jsonify(error="Falta «texto_guion»"), 400

    try:
        pdf_buffer = build_pdf(texto)
        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            download_name="guion.pdf",
            as_attachment=True
        )
    except Exception as exc:
        return jsonify(error=f"Error generando el PDF: {exc}"), 500

# ---------- Ejecutar localmente ---------- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
