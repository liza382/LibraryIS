using LibraryIS.Core.Data;
using LibraryIS.Core.Services;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.App;

public partial class IssueForm : Form
{
    private readonly LibraryDbContext _db;
    private readonly AuthService _auth;

    public IssueForm(LibraryDbContext db, AuthService auth)
    {
        _db = db; _auth = auth;
        Text = "Выдача книги"; Size = new Size(500, 350);
        StartPosition = FormStartPosition.CenterParent;

        var cbBook = new ComboBox { Location = new Point(150, 30), Width = 300, DropDownStyle = ComboBoxStyle.DropDownList };
        var cbReader = new ComboBox { Location = new Point(150, 70), Width = 300, DropDownStyle = ComboBoxStyle.DropDownList };
        var lblInfo = new Label { Location = new Point(150, 110), Width = 300, Text = "Доступно: -" };
        var btn = new Button { Text = "Выдать", Location = new Point(150, 150), Width = 150 };
        var lblRes = new Label { Location = new Point(150, 200), Width = 300, ForeColor = System.Drawing.Color.DarkGreen };

        cbBook.DataSource = _db.Books.Select(b => new { b.Id, b.Title }).ToList();
        cbBook.DisplayMember = "Title"; cbBook.ValueMember = "Id";

        cbReader.DataSource = _db.Readers.Select(r => new { r.Id, r.FullName, r.TicketNumber }).ToList();
        cbReader.DisplayMember = "FullName"; cbReader.ValueMember = "Id";

        cbBook.SelectedIndexChanged += (s, e) => {
            if (cbBook.SelectedValue is int id)
            {
                var svc = new LoanService(_db, new LoanSettings());
                lblInfo.Text = $"Доступно экземпляров: {svc.AvailableCopies(id)}";
            }
        };

        btn.Click += (s, e) => {
            try
            {
                var svc = new LoanService(_db, new LoanSettings());
                var loan = svc.Issue((int)cbBook.SelectedValue!, (int)cbReader.SelectedValue!, _auth.Current!.Id);
                lblRes.Text = $"✓ Выдано. Срок возврата: {loan.DueDate:dd.MM.yyyy}";
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        };

        Controls.AddRange(new Control[] {
            new Label { Text = "Книга:", Location = new Point(30, 33) }, cbBook,
            new Label { Text = "Читатель:", Location = new Point(30, 73) }, cbReader,
            lblInfo, btn, lblRes
        });
    }
}