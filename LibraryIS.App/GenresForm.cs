using LibraryIS.Core.Data;
using LibraryIS.Core.Models;

namespace LibraryIS.App;

public partial class GenresForm : Form
{
    private readonly LibraryDbContext _db;
    public GenresForm(LibraryDbContext db)
    {
        _db = db; Text = "Жанры"; Size = new Size(400, 400);
        StartPosition = FormStartPosition.CenterParent;

        var dgv = new DataGridView { Dock = DockStyle.Fill, AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill };
        dgv.DataSource = _db.Genres.ToList();

        var btnAdd = new Button { Text = "Добавить", Dock = DockStyle.Bottom };
        btnAdd.Click += (s, e) => {
            var name = Microsoft.VisualBasic.Interaction.InputBox("Название жанра:", "Новый жанр");
            if (!string.IsNullOrWhiteSpace(name))
            {
                _db.Genres.Add(new Genre { Name = name });
                _db.SaveChanges();
                dgv.DataSource = _db.Genres.ToList();
            }
        };

        Controls.Add(dgv);
        Controls.Add(btnAdd);
    }
}