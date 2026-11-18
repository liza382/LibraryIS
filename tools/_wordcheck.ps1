$ErrorActionPreference = 'Stop'
$local = 'C:\Users\student\AppData\Local\Temp\_doc.docx'
Copy-Item -LiteralPath '.\_doc.docx' -Destination $local -Force
$app = New-Object -ComObject Word.Application
$app.Visible = $false
$app.DisplayAlerts = 0
$doc = $app.Documents.Open($local, $false, $false)
Write-Output ("FIELDS=" + $doc.Fields.Count + " TOCS=" + $doc.TablesOfContents.Count)
$doc.TablesOfContents.Item(1).Update()
$doc.Repaginate()
$pages = $doc.ComputeStatistics(2)
$shapes = $doc.InlineShapes.Count
$tables = $doc.Tables.Count
$toc = $doc.TablesOfContents.Item(1).Range.Paragraphs.Count
$bad = @()
for ($i = 1; $i -le $shapes; $i++) {
    $sh = $doc.InlineShapes.Item($i)
    $sp = $sh.Range.Information(3)
    $end = [Math]::Min($sh.Range.End + 120, $doc.Content.End)
    $rng = $doc.Range($sh.Range.End, $end)
    $rng.Collapse(1)
    $para = $rng.Paragraphs.Item(1)
    if ($para.Range.Text.Trim().StartsWith([string][char]0x0420)) {
        $cp = $para.Range.Information(3)
        if ($cp -ne $sp) { $bad += "$i : $sp -> $cp" }
    }
}
$pagesWithText = @{}
for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
    $p = $doc.Paragraphs.Item($i)
    if ($p.Range.Text.Trim().Length -gt 0) { $pagesWithText[$p.Range.Information(3)] = $true }
}
$empty = @()
for ($p = 1; $p -le $pages; $p++) { if (-not $pagesWithText.ContainsKey($p)) { $empty += $p } }
$doc.Save()
$doc.Close(0)
$app.Quit()
Copy-Item -LiteralPath $local -Destination '.\_doc_done.docx' -Force
Write-Output ("PAGES=$pages SHAPES=$shapes TABLES=$tables TOC=$toc")
Write-Output ("EMPTY=" + ($empty -join ','))
Write-Output ("FIG_MISMATCH=" + $bad.Count)
$bad | Select-Object -First 6
