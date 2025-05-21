# FNV Mod Manager (Linux)

**Version 0.3 - Stable & Functional**

Author: Álex M  
Website: [natone.pro](https://natone.pro)  
[🔗 Project Page](https://natone.pro/proyectos/FNV_Mod_Manager/)

---

## 📦 Description

FNV Mod Manager for Linux is a lightweight GUI tool to manage Fallout: New Vegas mods on Linux.  
It supports both Nexus Mods integration and local mod installation, with a user-friendly tabbed interface.

---

## ✨ Features

- **Tabbed Interface**
  - `Install Mods`: Add mods via Nexus ID or a local ZIP file.
  - `Installed Mods`: View your current mods (double-click to remove from list).
- **Auto-Detection**
  - Automatically detects the FNV Steam path.
  - Manual override with path selection button.
- **Nexus Mods Integration**
  - Fetches mod info and downloads by just entering the mod ID.
  - *Requires a Nexus Mods API Key*.
- **Mod Management**
  - Keeps track of mod installation date and file.
  - Allows removing entries from the list (non-destructive).
- **Improved UX**
  - Clear status updates and error messages.
  - Robust handling of configuration and file paths.

---

## 🧪 Requirements

Install dependencies via pip:

```bash
pip install PyQt5 requests
```

---

## 🚀 Usage

1. **Set Your API Key**  
   Get a free API Key from [Nexus Mods](https://www.nexusmods.com)  
   Replace the placeholder `TU_API_KEY_AQUÍ` in the script.

2. **Run the Program**

```bash
python3 fnv_mod_manager.py
```

---

## 🧠 Notes

- Currently supports only `.zip` mods.
- Does **not** delete files when removing mods from the list.
- Config and installed mods list are saved at `~/.config/fnv_mod_manager.json`.

---

## 📄 License

MIT License (or specify if different).

---

&copy; 2025 Álex M — [natone.pro](https://natone.pro)
