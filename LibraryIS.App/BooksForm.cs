using LibraryIS.Core.Data;

namespace LibraryIS.App;

public partial class BooksForm : Form
{
    public BooksForm(LibraryDbContext db)
    {
        Text = "Книги";
        Size = new Size(800, 500);
        StartPosition = FormStartPosition.CenterParent;

        var dgv = new DataGridView
        {
            Dock = DockStyle.Fill,
            ReadOnly = true,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill
        };
        dgv.DataSource = db.Books
            .OrderBy(b => b.Title)
            .Select(b => new
            {
                b.Id,
                Название = b.Title,
                ISBN = b.Isbn,
                Издательство = b.Publisher,
                Год = b.Year,
                Экземпляров = b.CopiesTotal,
                Жанр = b.Genre.Name
            })
            .ToList();

        Controls.Add(dgv);
    }
}
