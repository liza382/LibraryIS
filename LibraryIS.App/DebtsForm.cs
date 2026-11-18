using LibraryIS.Core.Data;
using LibraryIS.Core.Services;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.App;

public partial class DebtsForm : Form
{
    public DebtsForm(LibraryDbContext db)
    {
        Text = "Задолженности"; Size = new Size(800, 500);
        StartPosition = FormStartPosition.CenterParent;

        var dgv = new DataGridView { Dock = DockStyle.Fill, ReadOnly = true, AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill };
        var svc = new LoanService(db, new LoanSettings());
        dgv.DataSource = svc.GetDebts().Select(l => new {
            l.Id,
            Билет = l.Reader.TicketNumber,
            Читатель = l.Reader.FullName,
            Книга = l.Book.Title,
            Срок = l.DueDate,
            Просрочка = (DateTime.Today - l.DueDate).Days,
            Пеня = (DateTime.Today - l.DueDate).Days * 5m
        }).ToList();

        Controls.Add(dgv);
    }
}