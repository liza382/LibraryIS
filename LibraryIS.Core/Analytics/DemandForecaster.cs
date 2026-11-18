using LibraryIS.Core.Data;
using Microsoft.EntityFrameworkCore;

namespace LibraryIS.Core.Analytics;

public record ForecastResult(double A, double B, double[] Fitted, double[] Forecast,
                             double Mae, double Mape);

public static class DemandForecaster
{
    public static ForecastResult Forecast(IReadOnlyList<double> y, int horizon = 3)
    {
        int n = y.Count;
        if (n < 3) throw new ArgumentException("Нужно минимум 3 периода");

        double st = 0, sy = 0, sty = 0, st2 = 0;
        for (int i = 0; i < n; i++)
        {
            double t = i + 1;
            st += t; sy += y[i]; sty += t * y[i]; st2 += t * t;
        }
        double b = (sty - st * sy / n) / (st2 - st * st / n);
        double a = sy / n - b * st / n;

        var fitted = Enumerable.Range(1, n).Select(t => a + b * t).ToArray();
        var fc = Enumerable.Range(n + 1, horizon).Select(t => a + b * t).ToArray();

        double mae = y.Zip(fitted, (yi, fi) => Math.Abs(yi - fi)).Average();
        var nz = y.Zip(fitted, (yi, fi) => (yi, fi)).Where(p => p.yi > 0).ToList();
        double mape = nz.Count == 0 ? 0 : nz.Average(p => Math.Abs((p.yi - p.fi) / p.yi)) * 100;

        return new ForecastResult(a, b, fitted, fc, mae, mape);
    }
}

public static class DemandSeriesBuilder
{
    public static (List<string> labels, double[] values) Monthly(
            LibraryDbContext db, DateTime from, DateTime to, int? bookId = null, int? genreId = null)
    {
        var q = db.Loans.Where(l => l.IssueDate >= from && l.IssueDate < to);
        if (bookId.HasValue) q = q.Where(l => l.BookId == bookId.Value);
        if (genreId.HasValue) q = q.Where(l => l.Book.GenreId == genreId.Value);

        var raw = q.GroupBy(l => new { l.IssueDate.Year, l.IssueDate.Month })
                   .Select(g => new { g.Key.Year, g.Key.Month, C = g.Count() })
                   .ToList()
                   .ToDictionary(x => (x.Year, x.Month), x => (double)x.C);

        var labels = new List<string>();
        var vals = new List<double>();
        for (var d = new DateTime(from.Year, from.Month, 1); d < to; d = d.AddMonths(1))
        {
            labels.Add(d.ToString("MM.yyyy"));
            vals.Add(raw.TryGetValue((d.Year, d.Month), out var c) ? c : 0);
        }
        return (labels, vals.ToArray());
    }
}