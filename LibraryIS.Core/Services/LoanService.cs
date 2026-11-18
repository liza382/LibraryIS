using LibraryIS.Core.Data;
using LibraryIS.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.Core.Services;

public class LoanSettings
{
    public int LoanDays { get; set; } = 14;
    public int MaxBooksPerReader { get; set; } = 5;
    public decimal FinePerDay { get; set; } = 5m;
    public int MaxProlong { get; set; } = 1;
}

public class LoanService
{
    private readonly LibraryDbContext _db;
    private readonly LoanSettings _s;

    public LoanService(LibraryDbContext db, LoanSettings s)
    {
        _db = db;
        _s = s;
    }

    public int AvailableCopies(int bookId)
    {
        int total = _db.Books.Where(b => b.Id == bookId).Select(b => b.CopiesTotal).First();
        int onHands = _db.Loans.Count(l => l.BookId == bookId && l.ReturnDate == null);
        return total - onHands;
    }

    public Loan Issue(int bookId, int readerId, int userId)
    {
        var reader = _db.Readers.Find(readerId) ?? throw new Exception("Читатель не найден");
        if (!reader.IsActive) throw new Exception("Читательский билет заблокирован");
        if (AvailableCopies(bookId) <= 0) throw new Exception("Нет свободных экземпляров");

        int onHands = _db.Loans.Count(l => l.ReaderId == readerId && l.ReturnDate == null);
        if (onHands >= _s.MaxBooksPerReader) throw new Exception($"Лимит {_s.MaxBooksPerReader} книг превышен");

        bool hasOverdue = _db.Loans.Any(l => l.ReaderId == readerId &&
                                            l.ReturnDate == null && l.DueDate < DateTime.Today);
        if (hasOverdue) throw new Exception("Есть просроченные книги");

        var loan = new Loan
        {
            BookId = bookId,
            ReaderId = readerId,
            UserId = userId,
            IssueDate = DateTime.Today,
            DueDate = DateTime.Today.AddDays(_s.LoanDays)
        };
        _db.Loans.Add(loan);
        _db.SaveChanges();
        return loan;
    }

    public decimal Return(int loanId, DateTime? date = null)
    {
        var loan = _db.Loans.Find(loanId) ?? throw new Exception("Выдача не найдена");
        if (loan.ReturnDate != null) throw new Exception("Книга уже возвращена");

        var d = (date ?? DateTime.Today).Date;
        int overdue = Math.Max(0, (d - loan.DueDate.Date).Days);
        loan.ReturnDate = d;
        loan.Fine = overdue * _s.FinePerDay;
        _db.SaveChanges();
        return loan.Fine;
    }

    public void Prolong(int loanId)
    {
        var l = _db.Loans.Find(loanId)!;
        if (l.ReturnDate != null) throw new Exception("Книга возвращена");
        if (l.ProlongCount >= _s.MaxProlong) throw new Exception("Лимит продлений исчерпан");
        if (l.DueDate < DateTime.Today) throw new Exception("Просроченную книгу продлить нельзя");
        l.DueDate = l.DueDate.AddDays(_s.LoanDays);
        l.ProlongCount++;
        _db.SaveChanges();
    }

    public List<Loan> GetDebts() => _db.Loans
        .Include(l => l.Book).Include(l => l.Reader)
        .Where(l => l.ReturnDate == null && l.DueDate < DateTime.Today)
        .OrderBy(l => l.DueDate).ToList();
}