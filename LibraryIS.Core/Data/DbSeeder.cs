using LibraryIS.Core.Models;
using LibraryIS.Core.Services;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.Core.Data;

public static class DbSeeder
{
    public static void Seed(LibraryDbContext db)
    {
        if (db.Users.Any()) return;

        var genres = new[] { "Художественная", "Научная", "Учебная", "Детская", "Техническая" }
            .Select(n => new Genre { Name = n }).ToList();
        db.Genres.AddRange(genres);
        db.SaveChanges();

        var authors = new[] { "Достоевский Ф.М.", "Толстой Л.Н.", "Чехов А.П.", "Пушкин А.С.",
            "Лермонтов М.Ю.", "Гоголь Н.В.", "Тургенев И.С.", "Булгаков М.А." }
            .Select(n => new Author { FullName = n }).ToList();
        db.Authors.AddRange(authors);
        db.SaveChanges();

        var rnd = new Random(42);
        for (int i = 1; i <= 50; i++)
        {
            var book = new Book
            {
                Title = $"Книга №{i}",
                Isbn = $"978-{i:D5}-{rnd.Next(100, 999)}",
                Publisher = "Издательство",
                Year = rnd.Next(1990, 2025),
                CopiesTotal = rnd.Next(2, 10),
                GenreId = genres[rnd.Next(genres.Count)].Id
            };
            db.Books.Add(book);
        }
        db.SaveChanges();

        foreach (var b in db.Books.ToList())
        {
            db.BookAuthors.Add(new BookAuthor
            {
                BookId = b.Id,
                AuthorId = authors[rnd.Next(authors.Count)].Id
            });
        }
        db.SaveChanges();

        for (int i = 1; i <= 30; i++)
        {
            db.Readers.Add(new Reader
            {
                TicketNumber = $"ЧБ-{i:D4}",
                FullName = $"Читатель {i}",
                Phone = $"+79{rnd.Next(100000000, 999999999)}",
                Category = i % 3 == 0 ? "Преподаватель" : "Студент",
                RegisteredAt = DateTime.Today.AddMonths(-rnd.Next(1, 36))
            });
        }
        db.SaveChanges();

        db.Users.Add(new User
        {
            Login = "admin",
            FullName = "Администратор",
            Role = UserRole.Admin,
            PasswordHash = PasswordHasher.Hash("admin")
        });
        db.Users.Add(new User
        {
            Login = "librarian",
            FullName = "Библиотекарь",
            Role = UserRole.Librarian,
            PasswordHash = PasswordHasher.Hash("123")
        });
        db.SaveChanges();

        var books = db.Books.ToList();
        var readers = db.Readers.ToList();
        var admin = db.Users.First();
        var from = DateTime.Today.AddMonths(-24);
        for (var d = from; d < DateTime.Today; d = d.AddDays(1))
        {
            int month = d.Month;
            double season = month == 9 || month == 1 ? 1.8 : month == 7 ? 0.4 : 1.0;
            int count = (int)(rnd.NextDouble() * 3 * season);
            for (int j = 0; j < count; j++)
            {
                var loan = new Loan
                {
                    BookId = books[rnd.Next(books.Count)].Id,
                    ReaderId = readers[rnd.Next(readers.Count)].Id,
                    UserId = admin.Id,
                    IssueDate = d,
                    DueDate = d.AddDays(14),
                    ReturnDate = rnd.NextDouble() > 0.15 ? d.AddDays(rnd.Next(7, 25)) : null
                };
                if (loan.ReturnDate.HasValue && loan.ReturnDate > loan.DueDate)
                    loan.Fine = (loan.ReturnDate.Value - loan.DueDate).Days * 5m;
                db.Loans.Add(loan);
            }
        }
        db.SaveChanges();
    }
}