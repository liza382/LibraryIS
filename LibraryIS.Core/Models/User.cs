namespace LibraryIS.Core.Models;

public enum UserRole { Guest = 0, Reader = 1, Librarian = 2, Admin = 3 }

public class User
{
    public int Id { get; set; }
    public string Login { get; set; } = "";
    public string PasswordHash { get; set; } = "";
    public string FullName { get; set; } = "";
    public UserRole Role { get; set; }
    public int? ReaderId { get; set; }
}