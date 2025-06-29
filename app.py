from flask import Flask, request, send_from_directory, jsonify
from fpdf import FPDF
import io
import os
from pathlib import Path
import re

app = Flask(
    __name__,
    static_folder="static",  # Asegura que Render sirva esta carpeta
    static_url_path="/static"
)

# ---------- Utilidades ---------- #
FONT_PATH = Path(__file__).parent / "fonts" / "DejaVuSans.ttf"
CONVERTED_DIR = Path("static/converted")
CONVERTED_DIR.mkdir(parents=True, exist_ok=True)

def slugify(text):
    """Convierte texto en un nombre de archivo seguro."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip().replace(" ", "_"))[:50]

def build_pdf(texto: str) -> Path:
    """Convierte el texto recibido en un PDF y lo guarda en disco."""
    pdf = FPDF(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font("DejaVu", "", FONT_PATH.as_posix(), uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 8, texto)

    filename = slugify(texto.split("\n")[0]) + ".pdf"
    filepath = CONVERTED_DIR / filename
    pdf.output(filepath.as_posix(), dest="F")
    return filepath


# ---------- Rutas ---------- #
@app.route("/")
def home():
    return "✅ La API está activa."

@app.route("/convertir-pdf", methods=["POST"])
def convertir_pdf():
    data = request.get_json(silent=True) or {}
    texto = data.get("texto_guion", "")
    if not texto.strip():
        return jsonify(error="Falta «texto_guion»"), 400

    try:
        pdf_path = build_pdf(texto)
        url = f"/static/converted/{pdf_path.name}"
        full_url = request.host_url.rstrip("/") + url
        return jsonify(url_pdf=full_url)
    except Exception as exc:
        return jsonify(error=f"Error generando el PDF: {exc}"), 500

# ---------- Arranque local ---------- #
if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))

