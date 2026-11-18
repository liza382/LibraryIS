using ClosedXML.Excel;

namespace LibraryIS.Core.Reports;

public class DebtRow
{
    public string Ticket { get; set; } = "";
    public string Reader { get; set; } = "";
    public string Book { get; set; } = "";
    public DateTime Due { get; set; }
    public int Days { get; set; }
    public decimal Fine { get; set; }
}

public static class ExcelReportExporter
{
    public static void ExportDebts(IEnumerable<DebtRow> rows, string path)
    {
        using var wb = new XLWorkbook();
        var ws = wb.Worksheets.Add("Задолженности");
        ws.Cell(1, 1).Value = "Отчёт по задолженностям библиотеки";
        ws.Range(1, 1, 1, 6).Merge().Style.Font.SetBold().Font.SetFontSize(14);
        ws.Cell(2, 1).Value = $"Сформирован: {DateTime.Now:dd.MM.yyyy HH:mm}";

        string[] h = { "№ билета", "Читатель", "Книга", "Срок возврата", "Дней просрочки", "Пеня, ₽" };
        for (int i = 0; i < h.Length; i++) ws.Cell(4, i + 1).Value = h[i];
        ws.Range(4, 1, 4, 6).Style.Font.SetBold().Fill.BackgroundColor = XLColor.LightGray;

        int r = 5;
        foreach (var x in rows)
        {
            ws.Cell(r, 1).Value = x.Ticket;
            ws.Cell(r, 2).Value = x.Reader;
            ws.Cell(r, 3).Value = x.Book;
            ws.Cell(r, 4).Value = x.Due;
            ws.Cell(r, 5).Value = x.Days;
            ws.Cell(r, 6).Value = x.Fine;
            if (x.Days > 30) ws.Range(r, 1, r, 6).Style.Fill.BackgroundColor = XLColor.LightPink;
            r++;
        }
        ws.Cell(r, 5).Value = "Итого:";
        ws.Cell(r, 6).FormulaA1 = $"SUM(F5:F{r - 1})";
        ws.Columns().AdjustToContents();
        ws.SheetView.FreezeRows(4);
        wb.SaveAs(path);
    }
}