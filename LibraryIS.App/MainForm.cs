using LibraryIS.Core.Data;
using LibraryIS.Core.Reports;
using LibraryIS.Core.Services;
using Microsoft.Extensions.Configuration;

namespace LibraryIS.App;

public partial class MainForm : Form
{
    private readonly LibraryDbContext _db;
    private readonly IConfiguration _cfg;
    private readonly AuthService _auth;

    public MainForm(LibraryDbContext db, IConfiguration cfg, AuthService auth)
    {
        _db = db; _cfg = cfg; _auth = auth;
        Text = $"ИС Библиотеки — {_auth.Current!.FullName} ({_auth.Current.Role})";
        Size = new Size(900, 600);
        StartPosition = FormStartPosition.CenterScreen;

        var menu = new MenuStrip();
        var mSprav = new ToolStripMenuItem("Справочники");
        mSprav.DropDownItems.AddRange(new ToolStripItem[] {
            new ToolStripMenuItem("Книги", null, (s,e) => new BooksForm(_db).ShowDialog()),
            new ToolStripMenuItem("Читатели", null, (s,e) => new ReadersForm(_db).ShowDialog()),
            new ToolStripMenuItem("Авторы", null, (s,e) => new AuthorsForm(_db).ShowDialog()),
            new ToolStripMenuItem("Жанры", null, (s,e) => new GenresForm(_db).ShowDialog()),
        });

        var mOps = new ToolStripMenuItem("Операции");
        mOps.DropDownItems.AddRange(new ToolStripItem[] {
            new ToolStripMenuItem("Выдача книги", null, (s,e) => new IssueForm(_db, _auth).ShowDialog()),
            new ToolStripMenuItem("Возврат книги", null, (s,e) => new ReturnForm(_db).ShowDialog()),
        });

        var mRep = new ToolStripMenuItem("Отчёты и аналитика");
        mRep.DropDownItems.AddRange(new ToolStripItem[] {
            new ToolStripMenuItem("Задолженности", null, (s,e) => new DebtsForm(_db).ShowDialog()),
            new ToolStripMenuItem("Прогноз спроса", null, (s,e) => new ForecastForm(_db).ShowDialog()),
            new ToolStripMenuItem("Экспорт в Excel", null, (s,e) => ExportExcel()),
        });

        var mExit = new ToolStripMenuItem("Выход");
        mExit.Click += (s, e) => { Close(); Application.Exit(); };

        menu.Items.AddRange(new ToolStripItem[] { mSprav, mOps, mRep, mExit });
        MainMenuStrip = menu;
        Controls.Add(menu);

        var lbl = new Label
        {
            Text = $"Добро пожаловать, {_auth.Current.FullName}!\n\n" +
                   $"Книг в фонде: {_db.Books.Count()}\n" +
                   $"Читателей: {_db.Readers.Count()}\n" +
                   $"Выдач всего: {_db.Loans.Count()}\n" +
                   $"Просрочено: {_db.Loans.Count(l => l.ReturnDate == null && l.DueDate < DateTime.Today)}",
            AutoSize = false,
            Size = new Size(800, 400),
            Location = new Point(30, 50),
            Font = new Font("Segoe UI", 12)
        };
        Controls.Add(lbl);
    }

    private void ExportExcel()
    {
        using var dlg = new SaveFileDialog { Filter = "Excel|*.xlsx", FileName = "Задолженности.xlsx" };
        if (dlg.ShowDialog() != DialogResult.OK) return;
        var settings = LoadSettings();
        var svc = new LoanService(_db, settings);
        var debts = svc.GetDebts().Select(l => new DebtRow
        {
            Ticket = l.Reader.TicketNumber,
            Reader = l.Reader.FullName,
            Book = l.Book.Title,
            Due = l.DueDate,
            Days = (DateTime.Today - l.DueDate).Days,
            Fine = (DateTime.Today - l.DueDate).Days * settings.FinePerDay
        });
        ExcelReportExporter.ExportDebts(debts, dlg.FileName);
        MessageBox.Show("Экспортировано: " + dlg.FileName);
    }

    private LoanSettings LoadSettings() => new()
    {
        LoanDays = int.Parse(_cfg["Loans:LoanDays"] ?? "14"),
        MaxBooksPerReader = int.Parse(_cfg["Loans:MaxBooksPerReader"] ?? "5"),
        FinePerDay = decimal.Parse(_cfg["Loans:FinePerDay"] ?? "5"),
        MaxProlong = int.Parse(_cfg["Loans:MaxProlong"] ?? "1")
    };
}