from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def gerar_contrato_pdf(entry):
    path = f"./data/contracts/{entry.id}.pdf"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path, pagesize=A4)
    c.drawString(50, 800, "CONTRATO DE SERVIÇOS LIMITCLEAN")
    c.drawString(50, 770, f"Nome: {entry.nome}")
    c.drawString(50, 750, f"Documento: {entry.doc}")
    c.drawString(50, 730, f"E-mail: ...")  # Complete conforme seu modelo
    c.drawString(50, 710, f"Tipo de serviço: {entry.tipo}")
    c.drawString(50, 690, f"Valor bruto: R$ {entry.valor}")
    c.drawString(50, 670, f"Desconto: R$ {entry.desconto}")
    c.drawString(50, 650, f"Valor líquido: R$ {entry.liquido}")
    c.drawString(50, 630, f"Data: ...")
    c.drawString(50, 610, f"Assinatura: {entry.nome}")
    c.showPage()
    c.save()
    return path