# -*- coding: utf-8 -*-
"""Дополнительные схемы для отчёта."""
import math
from pathlib import Path

from PIL import Image, ImageDraw

from report_assets import BLUE, DARK, GRAY, GREEN, LIGHT, RED, TEXT, _arrow, _font


def _box(d, xy, title, lines=(), fill=LIGHT, outline=BLUE, tsize=38, bsize=30, radius=18):
    x1, y1, x2, y2 = xy
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=4)
    d.multiline_text(((x1 + x2) / 2, (y1 + y2) / 2), title + ("\n" + "\n".join(lines) if lines else ""),
                     font=_font(tsize, True), fill=TEXT, anchor="mm", align="center", spacing=8)


def enterprise(path: Path):
    img = Image.new("RGB", (1700, 900), "white")
    d = ImageDraw.Draw(img)
    _box(d, (600, 40, 1100, 150), "Директор библиотеки", tsize=36)
    top = (850, 150)
    deps = [
        ((80, 300, 520, 450), "Отдел комплектования", "закупка и учёт фонда"),
        ((600, 300, 1100, 450), "Отдел обслуживания", "абонемент и читальный зал"),
        ((1180, 300, 1620, 450), "Административный отдел", "снабжение и бухгалтерия"),
    ]
    subs = [
        ((80, 600, 520, 750), "Каталогизация", "обработка новых изданий"),
        ((600, 600, 1100, 750), "Абонемент", "выдача и возврат книг"),
        ((1180, 600, 1620, 750), "Бухгалтерия", "учёт и отчётность"),
    ]
    for xy, title, sub in deps:
        _box(d, xy, title, (sub,), tsize=30, bsize=25)
        _arrow(d, top[0], top[1], (xy[0] + xy[2]) // 2, xy[1])
    for i in range(3):
        parent = deps[i][0]
        child = subs[i][0]
        _arrow(d, (parent[0] + parent[2]) // 2, parent[3], (child[0] + child[2]) // 2, child[1])
        _box(d, child, subs[i][1], (subs[i][2],), tsize=30, bsize=25)
    img.save(path, dpi=(200, 200))


def _actor(d, x, y, label):
    d.ellipse((x - 24, y - 90, x + 24, y - 42), fill="white", outline=DARK, width=4)
    d.line((x, y - 42, x, y + 20), fill=DARK, width=5)
    d.line((x - 55, y - 20, x + 55, y - 20), fill=DARK, width=5)
    d.line((x, y + 20, x - 45, y + 85), fill=DARK, width=5)
    d.line((x, y + 20, x + 45, y + 85), fill=DARK, width=5)
    d.text((x, y + 115), label, font=_font(30, True), fill=TEXT, anchor="mm")


def use_case(path: Path):
    img = Image.new("RGB", (1800, 1050), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((430, 50, 1290, 960), radius=24, outline=BLUE, width=4, fill="#FAFCFF")
    d.text((860, 95), "ИС библиотеки", font=_font(40, True), fill=DARK, anchor="mm")
    items = [
        "Войти в систему", "Просмотреть справочники", "Оформить выдачу",
        "Оформить возврат", "Просмотреть задолженности", "Построить прогноз",
        "Экспортировать отчёт",
    ]
    centers = []
    for i, item in enumerate(items):
        y1 = 150 + i * 110
        d.rounded_rectangle((540, y1, 1180, y1 + 66), radius=33, fill="white", outline=BLUE, width=3)
        d.text((860, y1 + 33), item, font=_font(29), fill=TEXT, anchor="mm")
        centers.append((540, y1 + 33))
    _actor(d, 170, 520, "Библиотекарь")
    for target in centers:
        d.line((235, 500, target[0], target[1]), fill=BLUE, width=3)
    _actor(d, 1600, 520, "Администратор")
    for target in centers[-3:]:
        d.line((1535, 500, target[0] + 640, target[1]), fill=BLUE, width=3)
    img.save(path, dpi=(200, 200))


def _class_box(d, xy, name, fields, methods=()):
    x1, y1, x2, y2 = xy
    d.rectangle(xy, fill="white", outline=BLUE, width=4)
    d.rectangle((x1 + 4, y1 + 4, x2 - 4, y1 + 54), fill=BLUE)
    d.text(((x1 + x2) // 2, y1 + 29), name, font=_font(30, True), fill="white", anchor="mm")
    yy = y1 + 70
    for field in fields:
        d.text((x1 + 14, yy), field, font=_font(24), fill=TEXT, anchor="la")
        yy += 30
    yy += 6
    d.line((x1 + 6, yy, x2 - 6, yy), fill=BLUE, width=2)
    yy += 10
    for method in methods:
        d.text((x1 + 14, yy), method, font=_font(23, False), fill=DARK, anchor="la")
        yy += 30


def class_diagram(path: Path):
    img = Image.new("RGB", (1900, 1320), "white")
    d = ImageDraw.Draw(img)
    _class_box(d, (50, 60, 470, 330), "Genre", ["Id", "Name"])
    _class_box(d, (570, 60, 1080, 540), "Book",
               ["Id", "Title", "Isbn", "Publisher", "Year", "CopiesTotal", "GenreId"],
               ["+ AvailableCopies()"])
    _class_box(d, (1200, 60, 1850, 320), "BookAuthor", ["BookId", "AuthorId"])
    _class_box(d, (1200, 390, 1850, 700), "Author", ["Id", "FullName"])
    _class_box(d, (50, 410, 520, 850), "Reader",
               ["Id", "TicketNumber", "FullName", "Phone", "Category", "IsActive"],
               ["+ CanBorrow()"])
    _class_box(d, (600, 620, 1130, 1250), "Loan",
               ["Id", "BookId", "ReaderId", "UserId", "IssueDate", "DueDate",
                "ReturnDate", "Fine", "ProlongCount"],
               ["+ Return(date)", "+ Prolong()"])
    _class_box(d, (1200, 790, 1850, 1130), "User",
               ["Id", "Login", "PasswordHash", "FullName", "Role", "ReaderId"])

    d.line((470, 190, 570, 190), fill=BLUE, width=4)
    d.line((1080, 190, 1200, 190), fill=BLUE, width=4)
    d.line((1525, 390, 1525, 320), fill=BLUE, width=4)
    d.line((850, 540, 850, 620), fill=BLUE, width=4)
    d.line((520, 700, 600, 780), fill=BLUE, width=4)
    d.line((1200, 960, 1130, 960), fill=BLUE, width=4)
    for x, y, label in ((500, 165, "1"), (550, 165, "*"), (1110, 165, "1"),
                        (1180, 165, "*"), (1550, 345, "*"), (1550, 380, "1"),
                        (875, 575, "1"), (875, 605, "*"), (535, 675, "1"),
                        (585, 760, "*"), (1170, 935, "*"), (1165, 980, "1")):
        d.text((x, y), label, font=_font(24, True), fill=BLUE, anchor="mm",
               stroke_width=3, stroke_fill="white")
    img.save(path, dpi=(200, 200))


def sequence(path: Path):
    img = Image.new("RGB", (1800, 1100), "#FFFFFF")
    d = ImageDraw.Draw(img)
    parts = [("Библиотекарь", 150), ("IssueForm", 500), ("LoanService", 880),
             ("LibraryDbContext", 1260), ("SQL Server", 1630)]
    for name, x in parts:
        d.rounded_rectangle((x - 140, 40, x + 140, 110), radius=10, fill=LIGHT, outline=BLUE, width=3)
        d.text((x, 75), name, font=_font(26, True), fill=DARK, anchor="mm")
        for y in range(120, 1020, 18):
            d.line((x, y, x, y + 9), fill="#9AA7B8", width=2)

    def msg(y, x1, x2, text, dashed=False, color=BLUE):
        if dashed:
            length = abs(x2 - x1)
            step = 14
            pos = 0
            sign = 1 if x2 > x1 else -1
            while pos < length:
                end = min(pos + 8, length)
                d.line((x1 + sign * pos, y, x1 + sign * end, y), fill=color, width=3)
                pos = end + 7
            head = 12 if sign > 0 else -12
            d.line((x2, y, x2 - head, y - 7), fill=color, width=3)
            d.line((x2, y, x2 - head, y + 7), fill=color, width=3)
        else:
            _arrow(d, x1, y, x2, y, color=color, width=3, head=13)
        d.text(((x1 + x2) // 2, y - 20), text, font=_font(23), fill=TEXT, anchor="mm")

    msg(190, 150, 500, "выбрать книгу и читателя")
    msg(280, 500, 880, "Issue(bookId, readerId, userId)")
    msg(370, 880, 1260, "AvailableCopies(bookId)")
    msg(450, 1260, 1630, "SELECT COUNT(*) FROM Loans")
    msg(530, 1630, 1260, "количество выдач", dashed=True)
    d.text((760, 590), "проверка правил", font=_font(23), fill=DARK, anchor="mm")
    d.rounded_rectangle((830, 600, 970, 640), radius=8, outline=DARK, width=2, fill="white")
    d.line((900, 560, 900, 600), fill=BLUE, width=3)
    msg(690, 880, 1260, "Add(Loan); SaveChanges()")
    msg(770, 1260, 1630, "INSERT INTO Loans")
    msg(850, 1630, 1260, "OK", dashed=True, color=GREEN)
    msg(930, 880, 500, "Loan", dashed=True, color=GREEN)
    img.save(path, dpi=(200, 200))


def state_diagram(path: Path):
    img = Image.new("RGB", (1500, 760), "white")
    d = ImageDraw.Draw(img)
    d.ellipse((60, 355, 100, 395), fill=TEXT)
    d.ellipse((1440, 355, 1480, 395), fill="white", outline=TEXT, width=4)
    d.ellipse((1455, 370, 1465, 380), fill=TEXT)
    boxes = {
        "issued": (170, 300, 470, 430),
        "prolonged": (640, 260, 980, 380),
        "overdue": (640, 490, 980, 610),
        "returned": (1110, 300, 1410, 430),
    }
    for key, xy in boxes.items():
        d.rounded_rectangle(xy, radius=28, fill="#EAF1FB", outline=BLUE, width=4)
    d.text((320, 365), "Выдана", font=_font(34, True), fill=TEXT, anchor="mm")
    d.text((810, 320), "Продлена", font=_font(34, True), fill=TEXT, anchor="mm")
    d.text((810, 550), "Просрочена", font=_font(34, True), fill=TEXT, anchor="mm")
    d.text((1260, 365), "Возвращена", font=_font(34, True), fill=TEXT, anchor="mm")
    _arrow(d, 100, 375, 170, 375)
    _arrow(d, 470, 365, 640, 330)
    d.text((555, 285), "продление", font=_font(24), fill=TEXT, anchor="mm")
    _arrow(d, 470, 375, 1110, 365)
    d.text((790, 405), "возврат в срок", font=_font(24), fill=TEXT, anchor="mm")
    _arrow(d, 980, 320, 1110, 340)
    d.text((1040, 275), "возврат", font=_font(24), fill=TEXT, anchor="mm")
    _arrow(d, 470, 410, 640, 540)
    d.text((545, 490), "срок истёк", font=_font(24), fill=TEXT, anchor="mm")
    _arrow(d, 980, 530, 1110, 400)
    d.text((1095, 520), "возврат + пеня", font=_font(24), fill=TEXT, anchor="mm")
    _arrow(d, 1410, 365, 1440, 375)
    img.save(path, dpi=(200, 200))


def deployment(path: Path):
    img = Image.new("RGB", (1600, 850), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((60, 80, 760, 650), radius=18, fill="#FAFCFF", outline=BLUE, width=4)
    d.text((410, 120), "Рабочая станция", font=_font(36, True), fill=DARK, anchor="mm")
    _box(d, (110, 180, 710, 290), "LibraryIS.App", ("Windows Forms, .NET 8",), tsize=30, bsize=24)
    _box(d, (110, 330, 710, 440), "Windows 10 / 11", (".NET 8 Desktop Runtime",), tsize=30, bsize=24)
    _box(d, (110, 480, 710, 590), "Экспорт отчёта", ("файл XLSX",), tsize=30, bsize=24)

    d.rounded_rectangle((940, 80, 1540, 650), radius=18, fill="#FDF7EC", outline="#B26A00", width=4)
    d.text((1240, 120), "Сервер базы данных", font=_font(36, True), fill=DARK, anchor="mm")
    _box(d, (990, 190, 1490, 310), "SQL Server 2022", ("СУБД",), tsize=30, bsize=24)
    _box(d, (990, 350, 1490, 470), "База LibraryIS", ("7 таблиц",), tsize=30, bsize=24)

    _arrow(d, 710, 370, 940, 370, width=4)
    d.text((825, 335), "TCP 1433", font=_font(27, True), fill=GRAY, anchor="mm")
    d.text((825, 405), "Trusted Connection", font=_font(23), fill=GRAY, anchor="mm")
    d.text((410, 620), "сохраняется локально", font=_font(23), fill=GRAY, anchor="mm")
    img.save(path, dpi=(200, 200))


def idef0(path: Path):
    img = Image.new("RGB", (1700, 950), "white")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((480, 320, 1220, 610), radius=16, fill=LIGHT, outline=BLUE, width=4)
    d.multiline_text((850, 465), "Учёт библиотечного фонда,\nчитателей и выдач",
                     font=_font(36, True), fill=TEXT, anchor="mm", align="center", spacing=10)
    _arrow(d, 60, 380, 480, 380, width=4)
    d.text((270, 350), "данные о книгах", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 60, 520, 480, 520, width=4)
    d.text((270, 490), "данные о читателях", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 650, 90, 650, 320, width=4)
    d.text((650, 60), "правила обслуживания", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 1000, 90, 1000, 320, width=4)
    d.text((1000, 60), "требования ГОСТ", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 1220, 380, 1640, 380, width=4)
    d.text((1430, 350), "выдачи и возвраты", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 1220, 520, 1640, 520, width=4)
    d.text((1430, 490), "отчёты и прогноз", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 650, 860, 650, 610, width=4)
    d.text((650, 895), "ИС библиотеки", font=_font(25), fill=TEXT, anchor="mm")
    _arrow(d, 1000, 860, 1000, 610, width=4)
    d.text((1000, 895), "SQL Server", font=_font(25), fill=TEXT, anchor="mm")
    img.save(path, dpi=(200, 200))


def dfd(path: Path):
    img = Image.new("RGB", (1700, 900), "white")
    d = ImageDraw.Draw(img)
    _box(d, (60, 380, 340, 520), "Библиотекарь", tsize=30)
    _box(d, (470, 160, 920, 330), "1. Оформление\nвыдачи", tsize=30)
    _box(d, (470, 560, 920, 730), "2. Расчёт\nзадолженностей", tsize=30)
    d.rectangle((1120, 120, 1580, 230), fill="#FFF4E5", outline="#B26A00", width=4)
    d.text((1350, 175), "D1 | Книги, читатели", font=_font(27, True), fill=TEXT, anchor="mm")
    d.rectangle((1120, 390, 1580, 500), fill="#FFF4E5", outline="#B26A00", width=4)
    d.text((1350, 445), "D2 | Выдачи", font=_font(27, True), fill=TEXT, anchor="mm")
    d.rectangle((1120, 660, 1580, 770), fill="#FFF4E5", outline="#B26A00", width=4)
    d.text((1350, 715), "D3 | Пользователи", font=_font(27, True), fill=TEXT, anchor="mm")

    _arrow(d, 340, 430, 470, 300, width=3)
    d.text((370, 350), "запрос", font=_font(23), fill=TEXT, anchor="lm")
    _arrow(d, 920, 230, 1120, 175, width=3)
    d.text((965, 175), "проверка", font=_font(23), fill=TEXT, anchor="lm")
    _arrow(d, 920, 310, 1120, 420, width=3)
    d.text((965, 385), "новая запись", font=_font(23), fill=TEXT, anchor="lm")
    _arrow(d, 1120, 470, 920, 620, width=3)
    d.text((965, 535), "просрочки", font=_font(23), fill=TEXT, anchor="lm")
    _arrow(d, 470, 660, 340, 500, width=3)
    d.text((350, 610), "отчёт", font=_font(23), fill=TEXT, anchor="lm")
    d.line((1120, 715, 1040, 715), fill=BLUE, width=3)
    d.line((1040, 715, 1040, 300), fill=BLUE, width=3)
    _arrow(d, 1040, 300, 920, 300, width=3)
    d.text((930, 560), "роль и права", font=_font(23), fill=TEXT, anchor="lm")
    img.save(path, dpi=(200, 200))


def make_diagrams(assets: Path):
    assets.mkdir(parents=True, exist_ok=True)
    enterprise(assets / "enterprise.png")
    use_case(assets / "usecase.png")
    class_diagram(assets / "classes.png")
    sequence(assets / "sequence.png")
    state_diagram(assets / "states.png")
    deployment(assets / "deployment.png")
    idef0(assets / "idef0.png")
    dfd(assets / "dfd.png")


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "report_assets"
    make_diagrams(target)
    print("diagrams:", [p.name for p in target.glob("*.png")])
