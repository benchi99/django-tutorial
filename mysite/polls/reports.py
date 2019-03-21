import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from .models import Pregunta, Eleccion

"""
Genera un buffer de bytes con la información para generar un
documento PDF con la información de una pregunta.
"""

def generaInformeResultado(pregunta):
    buffer = io.BytesIO()

    p = pregunta
    pdf = canvas.Canvas(buffer, A4)
    texto = pdf.beginText()

    texto.setTextOrigin(inch, inch*4.5)
    texto.setFont("Helvetica-Bold", 24)
    texto.textLine(p.texto_pregunta)

    texto.setFont("Courier", 14)
    texto.textLine()

    for e in p.eleccion_set.all():
        texto.textLine(e.texto_eleccion + '-' + str(e.votos))    

    pdf.drawText(texto)

    pdf.showPage()
    pdf.save()

    return buffer
