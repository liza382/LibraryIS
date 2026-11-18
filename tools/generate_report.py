# -*- coding: utf-8 -*-
"""Сборка итогового отчёта."""
from pathlib import Path

import report_content_a as a
import report_content_b as b
import report_content_c as c
from report_assets import make_images
from report_diagrams import make_diagrams
from report_lib import Report

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path(__file__).resolve().parent / "report_assets"
OUT = ROOT / "Отчет_ИС_библиотеки.docx"


def main():
    metrics = make_images(ASSETS)
    make_diagrams(ASSETS)

    r = Report(OUT)
    a.title_page(r)
    r.page_break()
    r.toc()
    a.introduction(r)
    a.chapter1(r, ASSETS)
    b.chapter2(r, ASSETS)
    b.chapter3(r, ASSETS, metrics)
    b.chapter4(r)
    c.chapter5(r)
    c.chapter6(r, ASSETS)
    c.chapter7(r)
    c.conclusion(r)
    c.sources(r)
    c.appendix_a(r)
    c.appendix_b(r)
    c.appendix_c(r, ASSETS)
    c.appendix_d(r)
    c.appendix_e(r)
    c.appendix_f(r, ASSETS)
    path = r.save()
    print("REPORT:", path)
    print("SIZE:", path.stat().st_size)


if __name__ == "__main__":
    main()
