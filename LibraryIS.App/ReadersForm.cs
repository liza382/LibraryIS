using LibraryIS.Core.Data;

namespace LibraryIS.App;

public partial class ReadersForm : Form
{
    public ReadersForm(LibraryDbContext db)
    {
        Text = "Читатели";
        Size = new Size(800, 500);
        StartPosition = FormStartPosition.CenterParent;

        var dgv = new DataGridView
        {
            Dock = DockStyle.Fill,
            ReadOnly = true,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };
        dgv.DataSource = db.Readers
            .OrderBy(r => r.FullName)
            .Select(r => new
            {
                r.Id,
                Билет = r.TicketNumber,
                ФИО = r.FullName,
                Телефон = r.Phone,
                r.Email,
                Категория = r.Category,
                Зарегистрирован = r.RegisteredAt,
                Активен = r.IsActive
            })
            .ToList();

        Controls.Add(dgv);
    }
}
