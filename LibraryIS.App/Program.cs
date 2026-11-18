using LibraryIS.Core.Data;
using Microsoft.Extensions.Configuration;
using Serilog;

namespace LibraryIS.App;

static class Program
{
    /// <summary>
    ///  The main entry point for the application.
    /// </summary>
    [STAThread]
    static void Main()
    {
        // To customize application configuration such as set high DPI settings or default font,
        // see https://aka.ms/applicationconfiguration.
        ApplicationConfiguration.Initialize();

        var cfg = new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: false, reloadOnChange: false)
            .Build();

        var logPath = Path.Combine(AppContext.BaseDirectory, cfg["Serilog:Path"] ?? "logs/app-.log");
        Directory.CreateDirectory(Path.GetDirectoryName(logPath)!);
        Log.Logger = new LoggerConfiguration()
            .MinimumLevel.Information()
            .WriteTo.File(logPath, rollingInterval: RollingInterval.Day)
            .CreateLogger();
        Log.Information("Запуск LibraryIS");

        var cs = cfg.GetConnectionString("Default");
        if (string.IsNullOrWhiteSpace(cs))
        {
            Log.Error("В appsettings.json не задана строка подключения Default");
            MessageBox.Show("В appsettings.json не задана строка подключения \"Default\".",
                "Ошибка конфигурации", MessageBoxButtons.OK, MessageBoxIcon.Error);
            Log.CloseAndFlush();
            return;
        }

        var db = new LibraryDbContext(cs);
        try
        {
            db.Database.EnsureCreated();
            DbSeeder.Seed(db);
        }
        catch (Exception ex)
        {
            Log.Error(ex, "Не удалось подключиться к базе данных");
            MessageBox.Show($"Не удалось подключиться к базе данных:\n{ex.Message}",
                "Ошибка подключения", MessageBoxButtons.OK, MessageBoxIcon.Error);
            Log.CloseAndFlush();
            return;
        }

        Application.Run(new LoginForm(db, cfg));
        Log.CloseAndFlush();
    }    
}