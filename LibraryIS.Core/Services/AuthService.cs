using LibraryIS.Core.Data;
using LibraryIS.Core.Models;

namespace LibraryIS.Core.Services;

public class AuthService
{
    private readonly LibraryDbContext _db;
    public User? Current { get; private set; }

    public AuthService(LibraryDbContext db)
    {
        _db = db;
    }

    public bool Login(string login, string password)
    {
        var u = _db.Users.FirstOrDefault(x => x.Login == login);
        if (u == null || !PasswordHasher.Verify(password, u.PasswordHash))
        {
            return false;
        }
        Current = u;
        return true;
    }

    public bool Can(UserRole need)
    {
        return Current != null && Current.Role >= need;
    }
}