# app.py
from flask import Flask, request, jsonify
from fpdf import FPDF
import os
from pathlib import Path

app = Flask(__name__)

# ---------- Utilidades ---------- #
FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"
STATIC_FOLDER = Path(__file__).parent / "static"
STATIC_FOLDER.mkdir(exist_ok=True)

def build_pdf(texto: str, output_path: Path):
    """Convierte el texto en un PDF y lo guarda en disco."""
    pdf = FPDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font("DejaVu", "", FONT_PATH.as_posix(), uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 8, texto)
    pdf.output(str(output_path))


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
        filename = "guion_formateado.pdf"
        output_path = STATIC_FOLDER / filename

        build_pdf(texto, output_path)

        public_url = f"{request.host_url}static/{filename}"
        return jsonify(url=public_url)

    except Exception as exc:
        return jsonify(error=f"Error generando el PDF: {exc}"), 500


# ---------- Arranque local ---------- #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
