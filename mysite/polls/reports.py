import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from .models import Pregunta, Eleccion

"""
Genera un buffer de bytes con la información para generar un
documento PDF con la información de una pregunta.
"""

def generaInformeResultado(pregunta, response):
    """
    Genera un buffer de bytes con la información para generar un
    documento PDF con la información de una pregunta.
    """
    pdf = canvas.Canvas(response)
    pdf.translate(inch, inch)
    texto = pdf.beginText()

    texto.setTextOrigin(inch, inch)
    texto.setFont("Helvetica-Bold", 24)
    texto.textLine(pregunta.texto_pregunta)

    texto.setFont("Courier", 14)
    texto.textLine()

    for e in pregunta.eleccion_set.all():
        texto.textLine(e.texto_eleccion + ' - ' + str(e.votos) + ' votos.')    

    pdf.drawText(texto)

    # Ya construido el objeto, se cierra y devuelve.
    pdf.showPage()
    pdf.save()

    return pdf