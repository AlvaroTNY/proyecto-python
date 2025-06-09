from fpdf import FPDF

def exportar_estudiantes_pdf(estudiantes, filename="estudiantes.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Listado de Estudiantes", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(20, 10, "ID", 1)
    pdf.cell(80, 10, "Nombre", 1)
    pdf.cell(30, 10, "Edad", 1)
    pdf.ln()
    for est in estudiantes:
        pdf.cell(20, 10, str(est[0]), 1)
        pdf.cell(80, 10, str(est[1]), 1)
        pdf.cell(30, 10, str(est[2]), 1)
        pdf.ln()
    pdf.output(filename)
