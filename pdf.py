from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def criar_pdf(mapa, nome_usuario, filename="mapa.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, f"Mapa Astral de {nome_usuario}")
    c.setFont("Helvetica", 14)
    y = 760
    for planeta, pos in mapa.items():
        c.drawString(50, y, f"{planeta}: {pos}")
        y -= 30
    c.showPage()
    c.save()
    return filename