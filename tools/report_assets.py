# -*- coding: utf-8 -*-
"""Рисунки для отчёта: архитектура, ER-модель, блок-схема выдачи, прогноз."""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BLUE = "#2F5597"
DARK = "#16365C"
LIGHT = "#EAF1FB"
TEXT = "#1F1F1F"
GREEN = "#2E7D32"
RED = "#C62828"
GRAY = "#666666"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", size)


def _arrow(d: ImageDraw.ImageDraw, x1, y1, x2, y2, color=BLUE, width=4, head=16):
    d.line((x1, y1, x2, y2), fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for delta in (math.radians(155), math.radians(-155)):
        d.line((x2, y2, x2 + head * math.cos(ang + delta), y2 + head * math.sin(ang + delta)),
               fill=color, width=width)


def _box(d, xy, title, lines, title_size=42, body_size=31):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=20, fill=LIGHT, outline=BLUE, width=4)
    d.text(((x1 + x2) // 2, y1 + 38), title, font=_font(title_size, True),
           fill=DARK, anchor="mm")
    d.multiline_text(((x1 + x2) // 2, y1 + 84), "\n".join(lines), font=_font(body_size),
                     fill=TEXT, anchor="ma", align="center", spacing=10)


def _entity(d, xy, name, fields):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=14, fill="white", outline=BLUE, width=4)
    d.rectangle((x1 + 4, y1 + 4, x2 - 4, y1 + 62), fill=BLUE)
    d.text(((x1 + x2) // 2, y1 + 33), name, font=_font(31, True), fill="white", anchor="mm")
    yy = y1 + 82
    for field in fields:
        d.text((x1 + 18, yy), field, font=_font(25), fill=TEXT, anchor="la")
        yy += 33


def _rel_label(d, x, y, text):
    d.text((x, y), text, font=_font(24, True), fill=BLUE, anchor="mm",
           stroke_width=3, stroke_fill="white")


def architecture(path: Path):
    img = Image.new("RGB", (1800, 1120), "white")
    d = ImageDraw.Draw(img)
    _box(d, (60, 40, 1740, 280), "Слой представления — LibraryIS.App (WinForms)", [
        "LoginForm · MainForm · BooksForm · ReadersForm · AuthorsForm",
        "GenresForm · IssueForm · ReturnForm · DebtsForm · ForecastForm",
        "меню, таблицы данных, диалоги, график ScottPlot"])
    _box(d, (60, 400, 840, 700), "Бизнес-логика — LibraryIS.Core", [
        "AuthService — вход и роли",
        "LoanService — выдача и возврат",
        "LoanSettings — правила обслуживания",
        "PasswordHasher — PBKDF2"], title_size=36, body_size=28)
    _box(d, (960, 400, 1740, 700), "Аналитика и отчёты — LibraryIS.Core", [
        "DemandSeriesBuilder — ряд по месяцам",
        "DemandForecaster — регрессия",
        "MAE и MAPE — оценка точности",
        "ExcelReportExporter — ClosedXML"], title_size=36, body_size=28)
    _box(d, (60, 800, 1740, 1040), "Доступ к данным", [
        "LibraryDbContext — EF Core 8, DbSet<Book>, DbSet<Loan> и др.",
        "SQL Server — база LibraryIS (7 таблиц)",
        "appsettings.json — строка подключения и параметры обслуживания"])

    _arrow(d, 450, 280, 450, 400)
    _arrow(d, 1350, 280, 1350, 400)
    _arrow(d, 450, 700, 450, 800)
    _arrow(d, 1350, 700, 1350, 800)
    d.text((470, 340), "вызовы методов", font=_font(26), fill=GRAY)
    d.text((1370, 340), "вызовы методов", font=_font(26), fill=GRAY)
    d.text((470, 740), "LINQ, SaveChanges", font=_font(26), fill=GRAY)
    d.text((1370, 740), "запросы к БД", font=_font(26), fill=GRAY)
    d.text((60, 1065), "Формы также обращаются к LibraryDbContext напрямую при чтении справочников.",
           font=_font(26, False), fill=GRAY)
    img.save(path, dpi=(200, 200))


def er_model(path: Path):
    img = Image.new("RGB", (1800, 1320), "white")
    d = ImageDraw.Draw(img)

    _entity(d, (60, 60, 500, 330), "Genres", ["Id (PK)", "Name"])
    _entity(d, (620, 60, 1180, 500), "Books", [
        "Id (PK)", "Title", "Isbn", "Publisher", "Year", "CopiesTotal", "GenreId (FK)"])
    _entity(d, (1300, 60, 1740, 390), "BookAuthors", [
        "BookId (PK, FK)", "AuthorId (PK, FK)"])
    _entity(d, (1300, 470, 1740, 760), "Authors", ["Id (PK)", "FullName"])
    _entity(d, (60, 470, 560, 940), "Readers", [
        "Id (PK)", "TicketNumber", "FullName", "Phone", "Email", "Category",
        "RegisteredAt", "IsActive"])
    _entity(d, (650, 620, 1230, 1240), "Loans", [
        "Id (PK)", "BookId (FK)", "ReaderId (FK)", "UserId (FK)", "IssueDate",
        "DueDate", "ReturnDate", "Fine", "ProlongCount"])
    _entity(d, (1300, 840, 1740, 1200), "Users", [
        "Id (PK)", "Login", "PasswordHash", "FullName", "Role", "ReaderId"])

    d.line((500, 190, 620, 190), fill=BLUE, width=4)
    _rel_label(d, 520, 165, "1")
    _rel_label(d, 600, 165, "N")
    d.line((1180, 190, 1300, 190), fill=BLUE, width=4)
    _rel_label(d, 1200, 165, "1")
    _rel_label(d, 1280, 165, "N")
    d.line((1520, 470, 1520, 390), fill=BLUE, width=4)
    _rel_label(d, 1545, 450, "1")
    _rel_label(d, 1545, 410, "N")
    d.line((900, 500, 900, 620), fill=BLUE, width=4)
    _rel_label(d, 925, 535, "1")
    _rel_label(d, 925, 600, "N")
    d.line((560, 690, 650, 760), fill=BLUE, width=4)
    _rel_label(d, 575, 665, "1")
    _rel_label(d, 645, 745, "N")
    d.line((1300, 1030, 1230, 1030), fill=BLUE, width=4)
    _rel_label(d, 1275, 1005, "1")
    _rel_label(d, 1245, 1005, "N")
    img.save(path, dpi=(200, 200))


def issue_flow(path: Path):
    img = Image.new("RGB", (1320, 1480), "white")
    d = ImageDraw.Draw(img)
    cx = 560

    def rect(xy, text, fill=LIGHT, outline=BLUE, fsize=29, bold=False):
        d.rounded_rectangle(xy, radius=16, fill=fill, outline=outline, width=4)
        d.multiline_text(((xy[0] + xy[2]) // 2, (xy[1] + xy[3]) // 2), text,
                         font=_font(fsize, bold), fill=TEXT, anchor="mm",
                         align="center", spacing=8)

    def diamond(cy, text):
        pts = [(cx, cy - 72), (cx + 270, cy), (cx, cy + 72), (cx - 270, cy)]
        d.polygon(pts, fill="#FFF4E5", outline="#B26A00")
        d.multiline_text((cx, cy), text, font=_font(28), fill=TEXT, anchor="mm",
                         align="center", spacing=6)

    def err(cy, text):
        rect((900, cy - 62, 1260, cy + 62), text, fill="#FDE7E7", outline=RED, fsize=26)
        _arrow(d, 830, cy, 900, cy, color=RED)
        d.text((860, cy - 32), "нет", font=_font(24, True), fill=RED, anchor="mm",
               stroke_width=3, stroke_fill="white")

    rect((410, 30, 710, 100), "Начало", fill="#E8F5E9", outline=GREEN, fsize=30, bold=True)
    diamond(220, "Читатель\nактивен?")
    diamond(400, "Есть свободные\nэкземпляры?")
    diamond(580, "Книг на руках\nменьше 5?")
    diamond(760, "Нет просроченных\nкниг?")

    rect((250, 880, 870, 1010),
         "Создать Loan:\nIssueDate = сегодня,  DueDate = +14 дней", fsize=27)
    rect((250, 1060, 870, 1160), "Сохранить изменения (SaveChanges)", fsize=27)
    d.ellipse((450, 1210, 670, 1290), fill="#E8F5E9", outline=GREEN, width=4)
    d.text((560, 1250), "Конец", font=_font(30, True), fill=TEXT, anchor="mm")

    for y1, y2 in ((100, 148), (292, 328), (472, 508), (652, 688), (832, 880), (1010, 1060), (1160, 1210)):
        _arrow(d, cx, y1, cx, y2)
    for y in (220, 400, 580, 760):
        d.text((cx + 16, y + 76), "да", font=_font(24, True), fill=GREEN, anchor="la",
               stroke_width=3, stroke_fill="white")

    err(220, "Отказ: билет\nзаблокирован")
    err(400, "Отказ: нет\nсвободных копий")
    err(580, "Отказ: лимит\n5 книг")
    err(760, "Отказ: есть\nпросрочка")
    img.save(path, dpi=(200, 200))


def _dashed(d, p1, p2, color, width=4, dash=14, gap=10):
    x1, y1 = p1
    x2, y2 = p2
    length = math.hypot(x2 - x1, y2 - y1)
    if length == 0:
        return
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    pos = 0.0
    while pos < length:
        end = min(pos + dash, length)
        d.line((x1 + ux * pos, y1 + uy * pos, x1 + ux * end, y1 + uy * end),
               fill=color, width=width)
        pos = end + gap


def forecast(path: Path):
    # Фактические месячные выдачи из демонстрационной базы LibraryIS
    # (24 полных месяца: ноябрь 2024 — октябрь 2026).
    values = [14, 34, 78, 27, 34, 26, 25, 26, 3, 29, 72, 29,
              31, 32, 80, 29, 36, 25, 27, 29, 4, 26, 64, 38, 15]
    labels = []
    for i in range(25):
        month = (10 + i) % 12 + 1
        year = 2024 + (10 + i) // 12
        labels.append(f"{month:02d}.{str(year)[2:]}")

    n = len(values)
    ts = list(range(1, n + 1))
    st = sum(ts)
    sy = sum(values)
    sty = sum(t * y for t, y in zip(ts, values))
    st2 = sum(t * t for t in ts)
    b = (sty - st * sy / n) / (st2 - st * st / n)
    a = sy / n - b * st / n
    fitted = [a + b * t for t in ts]
    fc = [a + b * (n + k) for k in (1, 2, 3)]
    mae = sum(abs(y - f) for y, f in zip(values, fitted)) / n
    nz = [(y, f) for y, f in zip(values, fitted) if y > 0]
    mape = sum(abs((y - f) / y) for y, f in nz) / len(nz) * 100

    W, H = 1600, 900
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    left, right, top, bottom = 150, 1540, 100, 780
    total = n + 3
    ymax = max(max(values), max(fc)) * 1.18
    ymax = math.ceil(ymax / 20) * 20

    def px(i):
        return left + i * (right - left) / (total - 1)

    def py(v):
        return bottom - v / ymax * (bottom - top)

    for val in range(0, int(ymax) + 1, 20):
        y = py(val)
        d.line((left, y, right, y), fill="#E5E5E5", width=2)
        d.text((left - 15, y), str(val), font=_font(26), fill=GRAY, anchor="rm")

    d.line((left, top, left, bottom), fill="#444444", width=3)
    d.line((left, bottom, right, bottom), fill="#444444", width=3)

    for i in range(0, n, 3):
        x = px(i)
        d.line((x, bottom, x, bottom + 8), fill="#444444", width=2)
        d.text((x, bottom + 18), labels[i], font=_font(24), fill=GRAY, anchor="ma")

    d.line([(px(i), py(v)) for i, v in enumerate(fitted)], fill=GREEN, width=4)
    for i, v in enumerate(values):
        x, y = px(i), py(v)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=BLUE)

    prev = (px(n - 1), py(fitted[-1]))
    for k, v in enumerate(fc, start=1):
        point = (px(n - 1 + k), py(v))
        _dashed(d, prev, point, RED, width=4)
        d.ellipse((point[0] - 8, point[1] - 8, point[0] + 8, point[1] + 8), fill=RED)
        prev = point

    d.text(((left + right) // 2, 865), "Месяц", font=_font(28), fill=TEXT, anchor="mm")
    d.text((78, (top + bottom) // 2), "Выдачи, шт.", font=_font(26), fill=TEXT,
           anchor="mm")
    d.text((W // 2, 40), "Фактические выдачи, тренд и прогноз на 3 месяца",
           font=_font(34, True), fill=DARK, anchor="mm")

    lx, ly = left + 30, top + 30
    d.rounded_rectangle((lx, ly, lx + 300, ly + 150), radius=12, fill="white", outline="#BBBBBB", width=2)
    d.line((lx + 20, ly + 30, lx + 80, ly + 30), fill=BLUE, width=6)
    d.text((lx + 95, ly + 30), "Факт", font=_font(28), fill=TEXT, anchor="lm")
    d.line((lx + 20, ly + 78, lx + 80, ly + 78), fill=GREEN, width=5)
    d.text((lx + 95, ly + 78), "Тренд", font=_font(28), fill=TEXT, anchor="lm")
    _dashed(d, (lx + 20, ly + 126), (lx + 80, ly + 126), RED, width=5)
    d.text((lx + 95, ly + 126), "Прогноз", font=_font(28), fill=TEXT, anchor="lm")

    d.text((right - 20, top + 25), f"y = {a:.2f} + {b:.2f}·t", font=_font(30), fill=DARK, anchor="ra")
    d.text((right - 20, top + 70), f"MAE = {mae:.2f}", font=_font(30), fill=DARK, anchor="ra")
    d.text((right - 20, top + 115), f"MAPE = {mape:.1f} %", font=_font(30), fill=DARK, anchor="ra")
    img.save(path, dpi=(200, 200))
    return {"a": a, "b": b, "mae": mae, "mape": mape, "forecast": fc,
            "values": values, "labels": labels}


def make_images(assets: Path) -> dict:
    assets.mkdir(parents=True, exist_ok=True)
    architecture(assets / "architecture.png")
    er_model(assets / "er.png")
    issue_flow(assets / "flow.png")
    return forecast(assets / "forecast.png")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "report_assets"
    print(make_images(out))
