Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class W {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint flags);
  public struct RECT { public int Left, Top, Right, Bottom; }
}
"@

$root = Split-Path $PSScriptRoot -Parent
$exe = Join-Path $root 'LibraryIS.App\bin\Debug\net8.0-windows\LibraryIS.App.exe'
$out = Join-Path $PSScriptRoot 'report_assets\screens'
New-Item -ItemType Directory -Force -Path $out | Out-Null

$p = Start-Process -FilePath $exe -WorkingDirectory (Split-Path $exe) -PassThru
for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 500
    $p.Refresh()
    if ($p.MainWindowHandle -ne 0) { break }
}
$h = $p.MainWindowHandle
Write-Output "handle=$h title=$($p.MainWindowTitle)"
[W]::SetForegroundWindow($h) | Out-Null
Start-Sleep -Milliseconds 800

function Save-Window([IntPtr]$hwnd, [string]$path) {
    $r = New-Object W+RECT
    [W]::GetWindowRect($hwnd, [ref]$r) | Out-Null
    $w = $r.Right - $r.Left
    $hh = $r.Bottom - $r.Top
    $bmp = New-Object System.Drawing.Bitmap($w, $hh)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $hdc = $g.GetHdc()
    $ok = [W]::PrintWindow($hwnd, $hdc, 2)
    $g.ReleaseHdc($hdc)
    if (-not $ok) { $g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size) }
    $g.Dispose()
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output "saved $path ($w x $hh)"
}

Save-Window $h (Join-Path $out '01-login.png')
