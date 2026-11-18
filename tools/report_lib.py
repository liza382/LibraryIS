# -*- coding: utf-8 -*-
"""Стили и вспомогательные функции для сборки отчёта DOCX."""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor

FONT = "Times New Roman"


class Report:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.doc = Document()
        self.table_no = 0
        self.figure_no = 0
        self.formula_no = 0
        self._setup()

    # ------------------------------------------------------------------ setup
    def _setup(self):
        sec = self.doc.sections[0]
        sec.page_width = Mm(210)
        sec.page_height = Mm(297)
        sec.left_margin = Cm(3)
        sec.right_margin = Cm(1.5)
        sec.top_margin = Cm(2)
        sec.bottom_margin = Cm(2)
        sec.footer_distance = Cm(1.2)
        sec.different_first_page_header_footer = True

        normal = self.doc.styles["Normal"]
        normal.font.name = FONT
        normal.font.size = Pt(14)
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        pf = normal.paragraph_format
        pf.line_spacing = 1.5
        pf.first_line_indent = Cm(1.25)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)

        for name, size in (("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 14)):
            st = self.doc.styles[name]
            st.font.name = FONT
            st.font.size = Pt(size)
            st.font.bold = True
            st.font.color.rgb = RGBColor(0, 0, 0)
            st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
            spf = st.paragraph_format
            spf.first_line_indent = Cm(0)
            spf.line_spacing = 1.5
            spf.space_before = Pt(12)
            spf.space_after = Pt(6)
            spf.keep_with_next = True
            if name == "Heading 1":
                spf.alignment = WD_ALIGN_PARAGRAPH.CENTER
                spf.page_break_before = True
            else:
                spf.alignment = WD_ALIGN_PARAGRAPH.LEFT

        footer = sec.footer
        footer.is_linked_to_previous = False
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.paragraph_format.first_line_indent = Cm(0)
        self._add_field(fp, "PAGE", size=12)

        first = sec.first_page_footer
        first.is_linked_to_previous = False
        for par in first.paragraphs:
            par.text = ""

        self.doc.core_properties.title = "Информационная система библиотеки"
        self.doc.core_properties.subject = "Отчёт по курсовому проекту"
        self.doc.core_properties.author = "Студент группы 9б-23"

    def _add_field(self, paragraph, instruction, size=14):
        run = paragraph.add_run()
        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = instruction
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        run._r.append(begin)
        run._r.append(instr)
        run._r.append(end)
        run.font.size = Pt(size)
        run.font.name = FONT

    # ------------------------------------------------------------------ text
    def h1(self, text):
        return self.doc.add_heading(text, level=1)

    def h2(self, text):
        return self.doc.add_heading(text, level=2)

    def p(self, text, lead=None):
        par = self.doc.add_paragraph()
        if lead:
            run = par.add_run(lead)
            run.bold = True
        par.add_run(text)
        return par

    def bullet(self, text):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(1.25)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        par.add_run("– " + text)
        return par

    def num(self, text, n):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(1.25)
        pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        par.add_run(f"{n}) " + text)
        return par

    def formula(self, text):
        self.formula_no += 1
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0)
        pf.space_before = Pt(6)
        pf.space_after = Pt(6)
        pf.tab_stops.add_tab_stop(Cm(8.25), WD_TAB_ALIGNMENT.CENTER)
        pf.tab_stops.add_tab_stop(Cm(16.4), WD_TAB_ALIGNMENT.RIGHT)
        par.add_run("\t")
        run = par.add_run(text)
        run.italic = True
        par.add_run("\t")
        par.add_run(f"({self.formula_no})")
        return self.formula_no

    def centered(self, text="", size=14, bold=False, italic=False, before=0, after=0, spacing=1.0):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(before)
        pf.space_after = Pt(after)
        pf.line_spacing = spacing
        run = par.add_run(text)
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        return par

    def page_break(self):
        self.doc.add_page_break()

    def spacer(self, pts=6):
        par = self.doc.add_paragraph()
        par.paragraph_format.space_after = Pt(0)
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.line_spacing = 1.0
        par.paragraph_format.first_line_indent = Cm(0)
        run = par.add_run("")
        run.font.size = Pt(pts)

    # ------------------------------------------------------------------ blocks
    def _caption(self, text, align=WD_ALIGN_PARAGRAPH.LEFT):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = align
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(8)
        pf.space_after = Pt(3)
        pf.line_spacing = 1.0
        pf.keep_with_next = True
        run = par.add_run(text)
        run.font.size = Pt(12)

    def table(self, caption, headers, rows, widths, center_cols=(), font_size=11, label=None):
        self.table_no += 1
        number = label if label else str(self.table_no)
        if caption:
            self._caption(f"Таблица {number} — {caption}")
        table = self.doc.add_table(rows=1, cols=len(headers))
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        table.rows[0]._tr.get_or_add_trPr().append(self._el("w:tblHeader", {"w:val": "true"}))

        for idx, header in enumerate(headers):
            cell = table.rows[0].cells[idx]
            cell.width = Cm(widths[idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            self._cell(cell, header, bold=False, center=True, size=font_size)
            self._shade(cell, "DEEAF6")

        for row in rows:
            added = table.add_row()
            added._tr.get_or_add_trPr().append(self._el("w:cantSplit", {"w:val": "true"}))
            cells = added.cells
            for idx, value in enumerate(row):
                cells[idx].width = Cm(widths[idx])
                cells[idx].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                self._cell(cells[idx], str(value), center=idx in center_cols, size=font_size)
        if len(table.rows) <= 18:
            for row in table.rows[:-1]:
                for cell in row.cells:
                    for par in cell.paragraphs:
                        par.paragraph_format.keep_with_next = True
        self.spacer(4)
        return number

    def _cell(self, cell, text, bold=False, center=False, size=11):
        par = cell.paragraphs[0]
        par.text = ""
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.line_spacing = 1.0
        pf.space_before = Pt(2)
        pf.space_after = Pt(2)
        run = par.add_run(text)
        run.bold = bold
        run.font.size = Pt(size)
        run.font.name = FONT
        run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), FONT)

    @staticmethod
    def _el(tag, attrs):
        el = OxmlElement(tag)
        for key, value in attrs.items():
            el.set(qn(key), value)
        return el

    @staticmethod
    def _shade(cell, fill):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = Report._el("w:shd", {"w:val": "clear", "w:color": "auto", "w:fill": fill})
        tcPr.insert_element_before(
            shd, "w:noWrap", "w:tcMar", "w:textDirection", "w:tcFitText", "w:vAlign",
            "w:hideMark", "w:headers", "w:cellIns", "w:cellDel", "w:cellMerge",
            "w:tcPrChange")

    def figure(self, image, caption, width_cm=16.0, label=None):
        self.figure_no += 1
        number = label if label else str(self.figure_no)
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = Cm(0)
        pf.space_before = Pt(8)
        pf.space_after = Pt(4)
        pf.keep_with_next = True
        par.add_run().add_picture(str(image), width=Cm(width_cm))
        self._caption(f"Рисунок {number} — {caption}", align=WD_ALIGN_PARAGRAPH.CENTER)
        return number

    def code(self, text):
        par = self.doc.add_paragraph()
        pf = par.paragraph_format
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.first_line_indent = Cm(0)
        pf.left_indent = Cm(0.4)
        pf.line_spacing = 1.0
        pf.space_before = Pt(4)
        pf.space_after = Pt(8)
        pf.keep_together = True
        pPr = par._p.get_or_add_pPr()
        shd = self._el("w:shd", {"w:val": "clear", "w:color": "auto", "w:fill": "F4F4F4"})
        pPr.insert_element_before(
            shd, "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
            "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
            "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
            "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
            "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
            "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")
        run = par.add_run(text.strip("\n"))
        run.font.name = "Consolas"
        run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Consolas")
        run.font.size = Pt(9)

    # ------------------------------------------------------------------ toc
    def toc(self):
        self.centered("СОДЕРЖАНИЕ", size=16, bold=True, after=12)
        par = self.doc.add_paragraph()
        par.paragraph_format.first_line_indent = Cm(0)
        par.paragraph_format.line_spacing = 1.0
        def _run_with(el):
            run = par.add_run()
            run._r.append(el)
            return run

        begin = OxmlElement("w:fldChar")
        begin.set(qn("w:fldCharType"), "begin")
        _run_with(begin)
        instr = OxmlElement("w:instrText")
        instr.set(qn("xml:space"), "preserve")
        instr.text = 'TOC \\o "1-2" \\h \\z \\u'
        _run_with(instr)
        separate = OxmlElement("w:fldChar")
        separate.set(qn("w:fldCharType"), "separate")
        _run_with(separate)
        placeholder = OxmlElement("w:t")
        placeholder.text = "Оглавление обновится при открытии документа (F9)."
        _run_with(placeholder)
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        _run_with(end)

        settings = self.doc.settings.element
        settings.append(self._el("w:updateFields", {"w:val": "true"}))

    def save(self):
        self.doc.save(self.path)
        return self.path
