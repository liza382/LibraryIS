using LibraryIS.Core.Data;
using LibraryIS.Core.Models;

namespace LibraryIS.App;

public partial class AuthorsForm : Form
{
    public AuthorsForm(LibraryDbContext db)
    {
        Text = "Авторы";
        Size = new Size(500, 400);
        StartPosition = FormStartPosition.CenterParent;

        var dgv = new DataGridView
        {
            Dock = DockStyle.Fill,
            ReadOnly = true,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };

        void Reload() => dgv.DataSource = db.Authors
            .OrderBy(a => a.FullName)
            .Select(a => new
            {
                a.Id,
                ФИО = a.FullName,
                Книг = a.BookAuthors.Count
            })
            .ToList();

        var btnAdd = new Button { Text = "Добавить", Dock = DockStyle.Bottom };
        btnAdd.Click += (s, e) =>
        {
            var name = Microsoft.VisualBasic.Interaction.InputBox("ФИО автора:", "Новый автор");
            if (!string.IsNullOrWhiteSpace(name))
            {
                db.Authors.Add(new Author { FullName = name });
                db.SaveChanges();
                Reload();
            }
        };

        Controls.Add(dgv);
        Controls.Add(btnAdd);
        Reload();
    }
}
