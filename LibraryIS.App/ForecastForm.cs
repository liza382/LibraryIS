using LibraryIS.Core.Analytics;
using LibraryIS.Core.Data;
using ScottPlot.WinForms;

namespace LibraryIS.App;

public partial class ForecastForm : Form
{
    public ForecastForm(LibraryDbContext db)
    {
        Text = "Прогноз спроса на книги"; Size = new Size(900, 600);
        StartPosition = FormStartPosition.CenterParent;

        var result = DemandSeriesBuilder.Monthly(db, DateTime.Today.AddMonths(-24), DateTime.Today);
        var labels = result.labels;
        var values = result.values;
        var fc = DemandForecaster.Forecast(values, horizon: 3);

        var plot = new FormsPlot { Dock = DockStyle.Fill };

        int n = values.Length;
        double[] xFact = Enumerable.Range(0, n).Select(i => (double)i).ToArray();
        double[] xFit = Enumerable.Range(0, n).Select(i => (double)i).ToArray();
        double[] xFc = Enumerable.Range(n, 3).Select(i => (double)i).ToArray();

        plot.Plot.Add.Scatter(xFact, values, ScottPlot.Colors.Blue);
        plot.Plot.Add.Scatter(xFit, fc.Fitted, ScottPlot.Colors.Green);
        plot.Plot.Add.Scatter(xFc, fc.Forecast, ScottPlot.Colors.Red);

        plot.Plot.Title("Прогноз спроса (выдач в месяц)");
        plot.Plot.YLabel("Количество выдач");
        plot.Plot.XLabel("Период");
        plot.Refresh();

        var info = new Label
        {
            Dock = DockStyle.Bottom,
            Height = 80,
            Text = $"Тренд: y = {fc.A:F2} + {fc.B:F2}·t\n" +
                   $"MAE = {fc.Mae:F2}, MAPE = {fc.Mape:F1}%\n" +
                   $"Прогноз на 3 мес: {string.Join(", ", fc.Forecast.Select(v => v.ToString("F0")))}",
            Font = new System.Drawing.Font("Consolas", 10)
        };

        Controls.Add(plot);
        Controls.Add(info);
        info.BringToFront();
    }
}