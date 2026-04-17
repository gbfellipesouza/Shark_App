import os
import sys
import subprocess
import ctypes
import tempfile
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to check if running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Self-elevate
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def run_powershell(code, title="SharkApp Execution"):
    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, f"shark_py_{random.randint(1000, 9999)}.ps1")
    
    replacements = {
        'ã': 'a', 'õ': 'o', 'ç': 'c', 'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'â': 'a', 'ê': 'e', 'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'É': 'E', 'Ê': 'E',
        'Í': 'I', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ú': 'U', 'Ç': 'C'
    }
    
    # PowerShell console theming to match SharkApp dark UI
    ps_theme = (
        "$ui = $Host.UI.RawUI;\n"
        "$ui.WindowTitle = '" + title + "';\n"
        "$ui.BackgroundColor = 'Black';\n"
        "$ui.ForegroundColor = 'Gray';\n"
        "try { $s=@'\n"
        "using System; using System.Runtime.InteropServices; \n"
        "[StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)] public struct CFI { public uint cb; public uint n; public short x; public short y; public int f; public int w; [MarshalAs(UnmanagedType.ByValTStr, SizeConst=32)] public string nm; }\n"
        "public class CF { [DllImport(\"kernel32.dll\")] public static extern IntPtr GetStdHandle(int n); [DllImport(\"kernel32.dll\")] public static extern bool SetCurrentConsoleFontEx(IntPtr h, bool b, ref CFI f);\n"
        "public static void S(short s) { IntPtr h=GetStdHandle(-11); CFI f=new CFI(); f.cb=(uint)Marshal.SizeOf(f); f.y=s; SetCurrentConsoleFontEx(h,false,ref f); } }\n"
        "'@; Add-Type $s; [CF]::S(14) } catch {}\n"
        "try { $sz = $ui.WindowSize; $sz.Width = 100; $sz.Height = 30; $ui.WindowSize = $sz } catch {}\n"
        "try { $bf = $ui.BufferSize; $bf.Width = 100; $ui.BufferSize = $bf } catch {}\n"
        "Clear-Host;\n"
        "Write-Host '';\n"
        "Write-Host '  ======================================' -ForegroundColor DarkCyan;\n"
        "Write-Host '    SharkApp  //  ' -NoNewLine -ForegroundColor Cyan;\n"
        "Write-Host '" + title + "' -ForegroundColor White;\n"
        "Write-Host '  ======================================' -ForegroundColor DarkCyan;\n"
        "Write-Host '';\n"
    )
    
    final_code = ps_theme + f"try {{\n{code}\n}} catch {{\n Write-Host 'ERRO FATAL:' $_.Exception.Message -ForegroundColor Red\n}}\nWrite-Host ''\nWrite-Host '  ======================================' -ForegroundColor DarkCyan\nWrite-Host -NoNewLine '  Pressione qualquer tecla para fechar...' -ForegroundColor DarkGray\n$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')\n"
    
    for k, v in replacements.items():
        final_code = final_code.replace(k, v)
        
    with open(script_path, "w", encoding="mbcs") as f:
        f.write(final_code)
    
    subprocess.call(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Normal", "-File", script_path])

def set_dark_titlebar(window):
    try:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), 4)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(value), 4)
    except Exception as e:
        pass

class CustomButton(tk.Frame):
    def __init__(self, parent, num, icon_char, title, desc, command, *args, **kwargs):
        super().__init__(parent, bg="#1e242c", bd=1, relief="solid", highlightbackground="#334155", highlightthickness=1, cursor="hand2")
        self.command = command
        self.config(width=200, height=180)
        self.pack_propagate(False)
        self.grid_propagate(False)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

        self.lbl_icon = tk.Label(self, text=icon_char, font=("Segoe UI Emoji", 26), bg="#1e242c", fg="#d1d5db", cursor="hand2")
        self.lbl_icon.pack(pady=(15, 5))
        self.lbl_icon.bind("<Button-1>", self.on_click)
        self.lbl_icon.bind("<Enter>", self.on_enter)
        self.lbl_icon.bind("<Leave>", self.on_leave)

        self.lbl_title = tk.Label(self, text=f"{num}. {title}", font=("Segoe UI", 11, "bold"), bg="#1e242c", fg="#f9fafb", cursor="hand2")
        self.lbl_title.pack(pady=(0, 5))
        self.lbl_title.bind("<Button-1>", self.on_click)
        self.lbl_title.bind("<Enter>", self.on_enter)
        self.lbl_title.bind("<Leave>", self.on_leave)

        self.lbl_desc = tk.Label(self, text=desc, font=("Segoe UI", 8), bg="#1e242c", fg="#9ca3af", wraplength=170, justify="center", cursor="hand2")
        self.lbl_desc.pack(padx=10, pady=(0, 10))
        self.lbl_desc.bind("<Button-1>", self.on_click)
        self.lbl_desc.bind("<Enter>", self.on_enter)
        self.lbl_desc.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(bg="#2a333f", highlightbackground="#475569")
        self.lbl_icon.configure(bg="#2a333f", fg="#ffffff")
        self.lbl_title.configure(bg="#2a333f")
        self.lbl_desc.configure(bg="#2a333f")

    def on_leave(self, event):
        self.configure(bg="#1e242c", highlightbackground="#334155")
        self.lbl_icon.configure(bg="#1e242c", fg="#d1d5db")
        self.lbl_title.configure(bg="#1e242c")
        self.lbl_desc.configure(bg="#1e242c")

    def on_click(self, event):
        self.command()

class SharkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.attributes('-alpha', 0.0)
        self.title("SharkApp")
        self.geometry("950x750")
        self.configure(bg="#111418")
        
        # Load Icon
        if getattr(sys, 'frozen', False):
            self.base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(self.base_path, "icon3.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        
        # Load icon image for header display
        self.header_icon = None
        try:
            self.header_icon = tk.PhotoImage(file=os.path.join(self.base_path, "icon3.png"))
        except:
            pass
            
        # Load background texture image
        self.bg_photo = None
        self.bg_img_raw = None
        try:
            texture_path = os.path.join(self.base_path, "bg_texture.png")
            if os.path.exists(texture_path):
                self.bg_img_raw = Image.open(texture_path).convert("RGBA")
        except Exception as e:
            print(f"Error loading texture: {e}")
            
        self.scripts = {}
        
        self.scripts["bios_key"] = r"""
$key=(Get-CimInstance -ClassName 'SoftwareLicensingService').OA3xOriginalProductKey
if([string]::IsNullOrWhiteSpace($key)) {
    Write-Host 'Chave nao encontrada na BIOS.' -ForegroundColor Red
} else {
    Write-Host 'Chave encontrada:' $key -ForegroundColor Green
    Write-Host 'Instalando chave...'
    cscript //nologo $env:windir\system32\slmgr.vbs /ipk $key > $null
    Write-Host 'Ativando o Windows...'
    cscript //nologo $env:windir\system32\slmgr.vbs /ato > $null
    Write-Host 'Ativacao concluida.' -ForegroundColor Green
}
"""

        self.scripts["winget"] = r"""
Write-Host 'Verificando e instalando atualizacoes (Winget)...' -ForegroundColor Cyan
winget update --all --include-unknown --accept-package-agreements --accept-source-agreements
"""

        self.scripts["crack"] = r"""
Write-Host 'Forcando TLS 1.2 e abrindo ativador MAS...' -ForegroundColor Cyan
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
irm https://get.activated.win -UseBasicParsing | iex
"""

        self.scripts["sfc"] = r"""
Write-Host '============================================================'
Write-Host '         REPARAR ARQUIVOS DO SISTEMA (SFC + DISM)'
Write-Host '============================================================'
Write-Host ''
Write-Host '  [1/2] Reparando imagem do Windows (DISM)...' -ForegroundColor Cyan
Write-Host '  Aguarde, isso pode levar varios minutos.'
Write-Host ''
DISM /Online /Cleanup-Image /RestoreHealth
if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host '  Aviso: DISM nao concluiu com sucesso. Continuando com SFC...' -ForegroundColor Yellow
}
Write-Host ''
Write-Host '============================================================'
Write-Host '  [2/2] Verificando arquivos do sistema (SFC)...' -ForegroundColor Cyan
Write-Host '  Aguarde, isso pode levar alguns minutos.'
Write-Host ''
sfc /scannow
Write-Host ''
Write-Host '  Verificacao e reparo concluidos!' -ForegroundColor Green
Write-Host '============================================================'
"""

        self.scripts["chkdsk"] = r"""
while ($true) {
    Clear-Host
    Write-Host '============================================================'
    Write-Host '             VERIFICACAO DE DISCO (CHKDSK)'
    Write-Host '============================================================'
    Write-Host ''
    Write-Host '  [1]  Corrigir erros do disco        (chkdsk /f)'
    Write-Host '  [2]  Recuperar setores defeituosos  (chkdsk /r)'
    Write-Host '  [3]  Reparo completo                (chkdsk /f /r /x)'
    Write-Host '  [4]  Verificar disco especifico'
    Write-Host '  [0]  Voltar ao menu'
    Write-Host -NoNewLine '  Pressione a tecla correspondente: '
    
    while ($true) {
        $key = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
        $choice = $key.Character.ToString()
        if ('1','2','3','4','0' -contains $choice) {
            Write-Host $choice
            break
        }
    }
    
    if ($choice -eq '1') {
        Write-Host ''
        Write-Host "  Solicitando chkdsk /f para $($env:SystemDrive)..."
        chkdsk $env:SystemDrive /f
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '2') {
        Write-Host ''
        Write-Host "  Solicitando chkdsk /r para $($env:SystemDrive)..."
        chkdsk $env:SystemDrive /r
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '3') {
        Write-Host ''
        Write-Host "  Solicitando chkdsk /f /r /x para $($env:SystemDrive)..."
        chkdsk $env:SystemDrive /f /r /x
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '4') {
        Write-Host ''
        $letra = Read-Host '  Digite a letra do disco (ex: D)'
        Write-Host ''
        chkdsk "$letra`:" /f /r /x
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '0') {
        break
    }
}
"""

        self.scripts["network"] = r"""
while ($true) {
    Clear-Host
    Write-Host '============================================================'
    Write-Host '             DIAGNOSTICO DE REDE'
    Write-Host '============================================================'
    Write-Host ''
    Write-Host '  [1]  Configuracoes basicas           (ipconfig)'
    Write-Host '  [2]  Detalhes completos              (ipconfig /all)'
    Write-Host '  [3]  Liberar IP                      (ipconfig /release)'
    Write-Host '  [4]  Renovar IP                      (ipconfig /renew)'
    Write-Host '  [5]  Liberar e renovar IP (reset)'
    Write-Host '  [6]  Ver endereco MAC                (getmac)'
    Write-Host '  [7]  Ping em host'
    Write-Host '  [0]  Voltar ao menu'
    Write-Host -NoNewLine '  Pressione a tecla correspondente: '
    
    while ($true) {
        $key = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
        $choice = $key.Character.ToString()
        if ('1','2','3','4','5','6','7','0' -contains $choice) {
            Write-Host $choice
            break
        }
    }
    
    if ($choice -eq '1') {
        Write-Host ''
        ipconfig
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '2') {
        Write-Host ''
        ipconfig /all
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '3') {
        Write-Host ''
        ipconfig /release
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '4') {
        Write-Host ''
        ipconfig /renew
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '5') {
        Write-Host ''
        Write-Host '  Liberando IP...'
        ipconfig /release
        Write-Host '  Renovando IP...'
        ipconfig /renew
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '6') {
        Write-Host ''
        getmac
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '7') {
        Write-Host ''
        $host_ip = Read-Host '  Digite o hostname ou IP'
        Write-Host ''
        ping $host_ip
        Write-Host ''
        cmd /c pause
    } elseif ($choice -eq '0') {
        break
    }
}
"""

        self.scripts["inventory"] = r"""
$ErrorActionPreference = 'SilentlyContinue'
Write-Host 'Preparando o ambiente para inventario...' -ForegroundColor Cyan
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters' -Name RequireSecuritySignature -Value 0 -Force
Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters' -Name AllowInsecureGuestAuth -Value 1 -Force
Start-Sleep 1
Restart-Service lanmanworkstation -ErrorAction SilentlyContinue
Restart-Service lanmanserver -ErrorAction SilentlyContinue
Start-Sleep 1
$hostname = 'C3PO.local'
$networkPath = '\\' + $hostname + '\inventarios\Ryan'
$mesAtual = Get-Date -Format 'MMMM'
$dataAtual = Get-Date -Format 'dd-MM-yyyy'
$mesPath = Join-Path $networkPath $mesAtual
$dataPath = Join-Path $mesPath $dataAtual
if (!(Test-Path $dataPath)) { New-Item -ItemType Directory -Path $dataPath -Force | Out-Null }
$clienteResposta = Read-Host 'Voce deseja criar uma pasta customizada para o cliente? (Y/N)'
if ($clienteResposta -match '^[Yy]$') {
    $clienteNome = Read-Host 'Digite o nome do cliente'
    $dataPath = Join-Path $dataPath $clienteNome
    if (!(Test-Path $dataPath)) { New-Item -ItemType Directory -Path $dataPath -Force | Out-Null }
}
Write-Host 'Digite o nome do arquivo final (sem a extensao .txt):' -ForegroundColor Yellow
$nomeArquivo = Read-Host
$arquivo = Join-Path $dataPath ($nomeArquivo + '.txt')
Write-Host 'Extraindo dados...' -ForegroundColor Cyan
$sys = Get-CimInstance Win32_ComputerSystem
$computador = 'Computer:      ' + $sys.Model
$proc = Get-CimInstance Win32_Processor | Select-Object -First 1
$cpu = 'CPU:           ' + $proc.Name
$cpuClock = '               ' + [math]::Round($proc.MaxClockSpeed / 1000, 2).ToString() + ' GHz'
$bb = Get-CimInstance Win32_BaseBoard
$motherboard = 'Motherboard:   ' + $bb.Manufacturer + ' ' + $bb.Product
$biosObj = Get-CimInstance Win32_BIOS
$bios = 'BIOS:          ' + $biosObj.SMBIOSBIOSVersion
$chipsetArr = (Get-PnpDevice -Class System -ErrorAction SilentlyContinue | Where-Object { $_.FriendlyName -match 'Intel|AMD' })
$chipset = 'Chipset:       ' + ($chipsetArr.FriendlyName -join ', ')
$memoria = Get-CimInstance Win32_PhysicalMemory
$memSum = ($memoria | Measure-Object -Property Capacity -Sum).Sum
$totalMemoria = 'Memory:        ' + [math]::Round($memSum / 1GB, 0).ToString() + ' MBytes'
$memoriaDetalhes = ($memoria | ForEach-Object { '               - ' + [math]::Round($_.Capacity / 1GB, 0).ToString() + ' MB ' + $_.Speed.ToString() + 'MHz ' + $_.Manufacturer + ' ' + $_.PartNumber }) -join [Environment]::NewLine
$gpu = Get-CimInstance Win32_VideoController
$gpuDetalhes = ($gpu | ForEach-Object { 'Graphics:      ' + $_.Name + ' [' + $_.PNPDeviceID.Split([char]92)[1] + ']' + [Environment]::NewLine + '               ' + $_.Name + ', ' + [math]::Round($_.AdapterRAM / 1MB, 0).ToString() + ' MB' }) -join [Environment]::NewLine
$discos = Get-CimInstance Win32_DiskDrive
$discosDetalhes = ($discos | ForEach-Object { 'Drive:         ' + $_.Model + ', ' + [math]::Round($_.Size / 1GB, 1).ToString() + ' GB, ' + $_.InterfaceType }) -join [Environment]::NewLine
$audio = Get-CimInstance Win32_SoundDevice
$audioDetalhes = ($audio | ForEach-Object { 'Sound:         ' + $_.Name }) -join [Environment]::NewLine
$redeObj = Get-CimInstance Win32_NetworkAdapter | Where-Object { $_.NetEnabled -eq $true } | Select-Object -First 1
$rede = 'Network:       ' + $redeObj.Name
$os = Get-CimInstance Win32_OperatingSystem
$sistema = 'OS:            ' + $os.Caption + ' (x64) Build ' + $os.BuildNumber
$conteudo = @($computador, $cpu, $cpuClock, $motherboard, $bios, $chipset, $totalMemoria, $memoriaDetalhes, $gpuDetalhes, $discosDetalhes, $audioDetalhes, $rede, $sistema) -join [Environment]::NewLine
$conteudo | Out-File -Encoding utf8 -FilePath $arquivo
Write-Output ('Arquivo salvo com sucesso em: ' + $arquivo) -ForegroundColor Green
Start-Process 'explorer.exe' $dataPath
"""

        self.scripts["titus"] = r"""
Write-Host 'Abrindo Chris Titus Tool... aguarde.' -ForegroundColor Cyan
iwr -useb https://christitus.com/win | iex
"""
        self.build_ui()
        self.update()
        set_dark_titlebar(self)
        self.attributes('-alpha', 1.0) # Map interface smoothly after applying darkness
        
    def execute_action(self, script_key):
        try:
            code = self.scripts.get(script_key)
            if code:
                # No replace needed since we used multiline strings properly now
                run_powershell(code)
            else:
                messagebox.showwarning("Erro", f"Script '{script_key}' não encontrado!")
        except Exception as e:
            messagebox.showerror("Aviso Fatal", f"Ocorreu um erro: {e}")

    def build_ui(self):
        main_container = tk.Frame(self, bg="#111418")
        main_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(main_container, bg="#111418", highlightthickness=0)
        
        # Custom dark scrollbar built from a Canvas (Windows ignores native Scrollbar colors)
        sb_width = 10
        sb_canvas = tk.Canvas(main_container, width=sb_width, bg="#0d0f12", highlightthickness=0, bd=0)
        sb_thumb_id = sb_canvas.create_rectangle(0, 0, sb_width, 50, fill="#334155", outline="", tags="thumb")
        sb_dragging = [False]
        sb_drag_y = [0]

        def sb_update_thumb(*args):
            if len(args) == 2:
                top, bottom = float(args[0]), float(args[1])
                sb_h = sb_canvas.winfo_height()
                y1 = int(top * sb_h)
                y2 = int(bottom * sb_h)
                if y2 - y1 < 20:
                    y2 = y1 + 20
                sb_canvas.coords(sb_thumb_id, 1, y1, sb_width - 1, y2)
                # Hide scrollbar thumb if content fits
                if top <= 0.0 and bottom >= 1.0:
                    sb_canvas.itemconfig(sb_thumb_id, state="hidden")
                else:
                    sb_canvas.itemconfig(sb_thumb_id, state="normal")

        def sb_on_press(event):
            tx1, ty1, tx2, ty2 = sb_canvas.coords(sb_thumb_id)
            if ty1 <= event.y <= ty2:
                sb_dragging[0] = True
                sb_drag_y[0] = event.y - ty1
            else:
                sb_h = sb_canvas.winfo_height()
                fraction = event.y / sb_h
                canvas.yview_moveto(fraction)

        def sb_on_drag(event):
            if sb_dragging[0]:
                sb_h = sb_canvas.winfo_height()
                new_top = (event.y - sb_drag_y[0]) / sb_h
                canvas.yview_moveto(max(0.0, min(1.0, new_top)))

        def sb_on_release(event):
            sb_dragging[0] = False

        def sb_on_enter(event):
            sb_canvas.itemconfig(sb_thumb_id, fill="#475569")

        def sb_on_leave(event):
            sb_canvas.itemconfig(sb_thumb_id, fill="#334155")

        sb_canvas.bind("<ButtonPress-1>", sb_on_press)
        sb_canvas.bind("<B1-Motion>", sb_on_drag)
        sb_canvas.bind("<ButtonRelease-1>", sb_on_release)
        sb_canvas.bind("<Enter>", sb_on_enter)
        sb_canvas.bind("<Leave>", sb_on_leave)
        
        scrollable_frame = tk.Frame(canvas, bg="#111418")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def draw_bg_texture(event):
            canvas.delete("bg_texture")
            w, h = event.width, event.height
            if w > 0 and h > 0 and self.bg_img_raw:
                # Optimized tiling using Pillow
                tile_w, tile_h = self.bg_img_raw.size
                tiled_img = Image.new('RGBA', (w, h))
                for x in range(0, w, tile_w):
                    for y in range(0, h, tile_h):
                        tiled_img.paste(self.bg_img_raw, (x, y))
                
                self.bg_photo = ImageTk.PhotoImage(tiled_img)
                canvas.create_image(0, 0, image=self.bg_photo, anchor="nw", tags="bg_texture")
                canvas.tag_lower("bg_texture")

            canvas.itemconfig(canvas_window, width=event.width)
            if hasattr(self, 'buttons_list') and self.buttons_list:
                available_width = event.width - 40
                cols = max(1, available_width // 220)
                for idx, btn in enumerate(self.buttons_list):
                    btn.grid(row=idx // cols, column=idx % cols, padx=10, pady=10)
            
        canvas.bind("<Configure>", draw_bg_texture)

        canvas.pack(side="left", fill="both", expand=True)
        sb_canvas.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=sb_update_thumb)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.bind_all("<MouseWheel>", _on_mousewheel)

        header = tk.Frame(scrollable_frame, bg="#111418")
        header.pack(pady=(40, 20), fill="x")
        
        title_row = tk.Frame(header, bg="#111418")
        title_row.pack()
        
        if self.header_icon:
            icon_lbl = tk.Label(title_row, image=self.header_icon, bg="#111418")
            icon_lbl.pack(side="left", padx=(0, 15))
        
        title_lbl = tk.Label(title_row, text="SHARKAPP", font=("Segoe UI Light", 32), fg="#f3f4f6", bg="#111418")
        title_lbl.pack(side="left")
        
        sub_lbl = tk.Label(header, text="BY: RYAN MOORE, CELSO GARCIA E GABRIEL FELLIPE", font=("Segoe UI", 10, "bold"), fg="#8b949e", bg="#111418")
        sub_lbl.pack(pady=(5, 15))
        
        admin_lbl = tk.Label(header, text="🟢 RUNNING AS ADMIN", font=("Segoe UI", 9, "bold"), fg="#10b981", bg="#1e293b", padx=15, pady=5, relief="flat")
        admin_lbl.pack()

        grid_wrapper = tk.Frame(scrollable_frame, bg="#111418")
        grid_wrapper.pack(expand=True, pady=10)

        self.buttons_list = []

        buttons = [
            ("🔑", "Ativação (BIOS)", "Obtem a chave contida na BIOS e ativa o Windows automaticamente.", "bios_key"),
            ("🔄", "Atualizar Aplicativos", "Atualiza o Windows e todos os programas pendentes usando Winget.", "winget"),
            ("🔓", "Ativação Temporária", "Ativação de Windows e pacote Office usando o Microsoft Activation Scripts (MAS).", "crack"),
            ("🧰", "Reparar Sistema", "Usa SFC e DISM para encontrar e corrigir arquivos vitais do sistema corrompidos.", "sfc"),
            ("💽", "Verificar Disco", "Inicia a verificação por problemas no sistema de arquivos ou setores defeituosos.", "chkdsk"),
            ("🌐", "Diagnóstico de Rede", "Libera, renova IP e faz uma limpeza completa no cache de registro DNS.", "network"),
            ("📋", "Criar Inventário", "Gera um relatório minucioso dos componentes de hardware da máquina atual no servidor.", "inventory"),
            ("⚙️", "Chris Titus Tool", "Inicia uma ferramenta utilitária e avançada para debloat, tweaks e instalações essenciais.", "titus")
        ]

        for idx, (icon, title, desc, action) in enumerate(buttons):
            num = idx + 1
            btn = CustomButton(grid_wrapper, num, icon, title, desc, lambda a=action: self.execute_action(a))
            self.buttons_list.append(btn)
            
            # Map Keyboard Bindings 
            self.bind(str(num), lambda e, a=action: self.execute_action(a))
            self.bind(f"<KP_{num}>", lambda e, a=action: self.execute_action(a))

if __name__ == "__main__":
    app = SharkApp()
    app.mainloop()
