namespace LibraryIS.Core.Models;

public class Reader
{
    public int Id { get; set; }
    public string TicketNumber { get; set; } = "";
    public string FullName { get; set; } = "";
    public string? Phone { get; set; }
    public string? Email { get; set; }
    public string? Category { get; set; }
    public DateTime RegisteredAt { get; set; }
    public bool IsActive { get; set; } = true;
    public List<Loan> Loans { get; set; } = new();
}