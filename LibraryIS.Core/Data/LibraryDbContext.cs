using LibraryIS.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.Core.Data;

public class LibraryDbContext : DbContext
{
    private readonly string _cs;
    public LibraryDbContext(string cs) => _cs = cs;

    public DbSet<Book> Books => Set<Book>();
    public DbSet<Author> Authors => Set<Author>();
    public DbSet<Genre> Genres => Set<Genre>();
    public DbSet<BookAuthor> BookAuthors => Set<BookAuthor>();
    public DbSet<Reader> Readers => Set<Reader>();
    public DbSet<Loan> Loans => Set<Loan>();
    public DbSet<User> Users => Set<User>();

    protected override void OnConfiguring(DbContextOptionsBuilder b)
    {
        b.UseSqlServer(_cs);
    }

    protected override void OnModelCreating(ModelBuilder m)
    {
        m.Entity<BookAuthor>().HasKey(x => new { x.BookId, x.AuthorId });
        m.Entity<Reader>().HasIndex(r => r.TicketNumber).IsUnique();
        m.Entity<User>().HasIndex(u => u.Login).IsUnique();
    }
}