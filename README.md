# 🦈 SharkApp

**SharkApp** is a premium, all-in-one system utility tool designed for Windows. It provides a modern, high-performance interface to execute critical system maintenance, activation, and diagnostic tasks with a single click.

## 🚀 Features

SharkApp consolidates several powerful system tools into a single, intuitive dashboard:

1.  **🔑 Windows Activation (BIOS):** Automatically retrieves the OEM product key from your BIOS/UEFI and activates Windows.
2.  **🔄 Application Updates:** Batch updates Windows and all installed applications using **Winget**.
3.  **🔓 Software Activation:** Integrated access to **Microsoft Activation Scripts (MAS)** for Windows and Office.
4.  **🧰 System Repair:** Automated execution of **SFC (System File Checker)** and **DISM** to fix corrupted system files.
5.  **💽 Disk Verification:** Easy access to **CHKDSK** for finding and fixing disk errors/bad sectors.
6.  **🌐 Network Diagnostics:** A suite of tools to reset IP, flush DNS, check MAC addresses, and perform network pings.
7.  **📋 Hardware Inventory:** Generates a detailed hardware report and stores it locally or on a network server.
8.  **⚙️ Chris Titus Tool:** Quick access to the renowned Chris Titus Windows Utility for debloating and system tweaks.

## 💎 Design & UI

- **Premium Interface:** Modern dark-themed UI with a custom brushed-metal textured background.
- **Responsive Layout:** Dynamic grid system that adjusts based on window size.
- **Admin Awareness:** Built-in privilege checking with visual "Running as Admin" status.
- **Interactive Console:** Custom-themed PowerShell console for executing automated scripts.

## 🛠️ Built With

- **Python:** Core application logic.
- **Tkinter:** Native GUI framework.
- **Pillow (PIL):** High-performance image processing for UI textures.
- **PowerShell:** Backend automation for system tasks.
- **PyInstaller:** Used for compiling into a single, portable executable.

## 📦 How to Build (PyInstaller)

To compile SharkApp into a standalone `.exe`:

1.  Install the dependencies:
    ```bash
    pip install Pillow
    ```
2.  Run PyInstaller using the provided `.spec` file:
    ```bash
    pyinstaller shark.spec
    ```
3.  The compiled executable will be in the `dist/` folder.

## 👥 Credits

Developed by:
- **Gabriel Fellipe**

---

> [!WARNING]
> **Administrative Privileges Required:** This tool performs low-level system changes. Always run as Administrator.
