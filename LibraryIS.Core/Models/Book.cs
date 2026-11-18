namespace LibraryIS.Core.Models;

public class Book
{
    public int Id { get; set; }
    public string Title { get; set; } = "";
    public string? Isbn { get; set; }
    public string? Publisher { get; set; }
    public int Year { get; set; }
    public int CopiesTotal { get; set; }
    public int GenreId { get; set; }
    public Genre Genre { get; set; } = null!;
    public List<BookAuthor> BookAuthors { get; set; } = new();
    public List<Loan> Loans { get; set; } = new();
}