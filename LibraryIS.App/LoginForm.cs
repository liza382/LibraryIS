using LibraryIS.Core.Data;
using LibraryIS.Core.Models;
using LibraryIS.Core.Services;
using Microsoft.Extensions.Configuration;

namespace LibraryIS.App;

public partial class LoginForm : Form
{
    private readonly LibraryDbContext _db;
    private readonly IConfiguration _cfg;

    public LoginForm(LibraryDbContext db, IConfiguration cfg)
    {
        _db = db; _cfg = cfg;
        Text = "ИС Библиотеки — Вход";
        ClientSize = new Size(420, 220);
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        StartPosition = FormStartPosition.CenterScreen;
        Font = new Font("Segoe UI", 10F);

        var layout = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            Padding = new Padding(24, 28, 24, 20),
            ColumnCount = 2,
            RowCount = 4
        };
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));
        layout.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        layout.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        layout.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

        var lblLogin = new Label
        {
            Text = "Логин:",
            AutoSize = true,
            Anchor = AnchorStyles.Left,
            Margin = new Padding(0, 0, 12, 14)
        };
        var txtLogin = new TextBox
        {
            Dock = DockStyle.Fill,
            Margin = new Padding(0, 0, 0, 14)
        };
        var lblPass = new Label
        {
            Text = "Пароль:",
            AutoSize = true,
            Anchor = AnchorStyles.Left,
            Margin = new Padding(0, 0, 12, 14)
        };
        var txtPass = new TextBox
        {
            Dock = DockStyle.Fill,
            UseSystemPasswordChar = true,
            Margin = new Padding(0, 0, 0, 14)
        };
        var btn = new Button
        {
            Text = "Войти",
            Dock = DockStyle.Top,
            Height = 34,
            Margin = new Padding(0, 6, 0, 0)
        };

        layout.Controls.Add(lblLogin, 0, 0);
        layout.Controls.Add(txtLogin, 1, 0);
        layout.Controls.Add(lblPass, 0, 1);
        layout.Controls.Add(txtPass, 1, 1);
        layout.Controls.Add(btn, 1, 2);
        Controls.Add(layout);

        btn.Click += (s, e) => {
            var auth = new AuthService(_db);
            if (auth.Login(txtLogin.Text.Trim(), txtPass.Text))
            {
                Hide();
                new MainForm(_db, _cfg, auth).Show();
            }
            else
            {
                MessageBox.Show("Неверный логин или пароль", "Ошибка",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
                txtPass.SelectAll();
                txtPass.Focus();
            }
        };

        AcceptButton = btn;
    }
}