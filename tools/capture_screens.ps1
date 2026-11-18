Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class W {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint flags);
  public struct RECT { public int Left, Top, Right, Bottom; }
}
"@

$root = Split-Path $PSScriptRoot -Parent
$exe = Join-Path $root 'LibraryIS.App\bin\Debug\net8.0-windows\LibraryIS.App.exe'
$out = Join-Path $PSScriptRoot 'report_assets\screens'
New-Item -ItemType Directory -Force -Path $out | Out-Null

function Save-Window([IntPtr]$hwnd, [string]$name) {
    $r = New-Object W+RECT
    [W]::GetWindowRect($hwnd, [ref]$r) | Out-Null
    $w = $r.Right - $r.Left
    $hh = $r.Bottom - $r.Top
    if ($w -le 0 -or $hh -le 0) { return $false }
    $bmp = New-Object System.Drawing.Bitmap($w, $hh)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $hdc = $g.GetHdc()
    $ok = [W]::PrintWindow($hwnd, $hdc, 2)
    $g.ReleaseHdc($hdc)
    if (-not $ok) { $g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size) }
    $g.Dispose()
    $path = Join-Path $out $name
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output ("saved {0} ({1}x{2})" -f $name, $w, $hh)
    return $true
}

$p = Get-Process LibraryIS.App -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $p) {
    $p = Start-Process -FilePath $exe -WorkingDirectory (Split-Path $exe) -PassThru
    for ($i = 0; $i -lt 40; $i++) {
        Start-Sleep -Milliseconds 500
        $p.Refresh()
        if ($p.MainWindowHandle -ne 0) { break }
    }
}
$h = $p.MainWindowHandle
[W]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 700
Write-Output "start title=$($p.MainWindowTitle)"

$rootEl = [System.Windows.Automation.AutomationElement]::FromHandle($h)
$cond = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::ControlTypeProperty,
    [System.Windows.Automation.ControlType]::Edit)
$edits = $rootEl.FindAll([System.Windows.Automation.TreeScope]::Descendants, $cond)
Write-Output "edits=$($edits.Count)"
if ($edits.Count -ge 2) {
    $edits[0].SetFocus()
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait('admin')
    $edits[1].SetFocus()
    Start-Sleep -Milliseconds 200
    [System.Windows.Forms.SendKeys]::SendWait('admin')
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    Start-Sleep -Seconds 3
    $p.Refresh()
}

$main = [W]::GetForegroundWindow()
if ($main -eq [IntPtr]::Zero) { $main = $p.MainWindowHandle }
[W]::SetForegroundWindow($main) | Out-Null
Start-Sleep -Milliseconds 1000
Save-Window $main '02-main.png' | Out-Null

function Open-Menu([int]$top, [int]$item, [string]$name) {
    [W]::SetForegroundWindow($main) | Out-Null
    Start-Sleep -Milliseconds 400
    [System.Windows.Forms.SendKeys]::SendWait('%')
    Start-Sleep -Milliseconds 400
    for ($i = 0; $i -lt $top; $i++) {
        [System.Windows.Forms.SendKeys]::SendWait('{RIGHT}')
        Start-Sleep -Milliseconds 200
    }
    [System.Windows.Forms.SendKeys]::SendWait('{DOWN}')
    Start-Sleep -Milliseconds 400
    for ($i = 0; $i -lt $item; $i++) {
        [System.Windows.Forms.SendKeys]::SendWait('{DOWN}')
        Start-Sleep -Milliseconds 200
    }
    [System.Windows.Forms.SendKeys]::SendWait('{ENTER}')
    Start-Sleep -Seconds 2
    $fg = [W]::GetForegroundWindow()
    Save-Window $fg $name | Out-Null
    [System.Windows.Forms.SendKeys]::SendWait('%{F4}')
    Start-Sleep -Milliseconds 900
    [W]::SetForegroundWindow($main) | Out-Null
    Start-Sleep -Milliseconds 400
}

Open-Menu 0 0 '03-books.png'
Open-Menu 0 1 '04-readers.png'
Open-Menu 0 2 '05-authors.png'
Open-Menu 0 3 '06-genres.png'
Open-Menu 1 0 '07-issue.png'
Open-Menu 1 1 '08-return.png'
Open-Menu 2 0 '09-debts.png'
Open-Menu 2 1 '10-forecast.png'

[W]::SetForegroundWindow($main) | Out-Null
Start-Sleep -Milliseconds 300
[System.Windows.Forms.SendKeys]::SendWait('%{F4}')
Start-Sleep -Seconds 1
Write-Output 'done'
