using LibraryIS.Core.Data;
using LibraryIS.Core.Services;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.App;

public partial class ReturnForm : Form
{
    public ReturnForm(LibraryDbContext db)
    {
        Text = "Возврат книги"; Size = new Size(600, 400);
        StartPosition = FormStartPosition.CenterParent;

        var dgv = new DataGridView
        {
            Location = new Point(20, 20),
            Size = new Size(550, 280),
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill,
            ReadOnly = true,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect
        };

        var loans = db.Loans.Include(l => l.Book).Include(l => l.Reader)
            .Where(l => l.ReturnDate == null)
            .Select(l => new {
                l.Id,
                Книга = l.Book.Title,
                Читатель = l.Reader.FullName,
                Билет = l.Reader.TicketNumber,
                Выдана = l.IssueDate,
                Срок = l.DueDate,
                Просрочка = Math.Max(0, (DateTime.Today - l.DueDate).Days)
            }).ToList();

        dgv.DataSource = loans;
        var btn = new Button { Text = "Оформить возврат", Location = new Point(20, 310), Width = 200 };
        var lblRes = new Label { Location = new Point(240, 315), Width = 300 };

        btn.Click += (s, e) => {
            if (dgv.CurrentRow == null) return;
            int id = (int)dgv.CurrentRow.Cells["Id"].Value;
            var svc = new LoanService(db, new LoanSettings());
            var fine = svc.Return(id);
            lblRes.Text = fine > 0 ? $"Пеня: {fine} ₽" : "✓ Возвращено без пени";
            dgv.DataSource = db.Loans.Include(l => l.Book).Include(l => l.Reader)
                .Where(l => l.ReturnDate == null)
                .Select(l => new {
                    l.Id,
                    Книга = l.Book.Title,
                    Читатель = l.Reader.FullName,
                    Билет = l.Reader.TicketNumber,
                    Выдана = l.IssueDate,
                    Срок = l.DueDate,
                    Просрочка = Math.Max(0, (DateTime.Today - l.DueDate).Days)
                }).ToList();
        };

        Controls.AddRange(new Control[] { dgv, btn, lblRes });
    }
}