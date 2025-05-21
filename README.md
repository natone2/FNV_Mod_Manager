# FNV Mod Manager (Linux)

**Version 0.3 - Stable & Functional**

Author: Álex M  
Website: [natone.pro](https://natone.pro)  
[🔗 Project Page](https://natone.pro/proyectos/)
[📦 Binary](https://natone.pro/proyectos/uploads/FNV_Mod_Manager_v0.3_Linux.7z) 

---

## 📜 Description

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
   Replace the placeholder `YOUR_API_KEY` in the script.

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

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  
GNU General Public License for more details.

You should have received a copy of the GNU General Public License  
along with this program. If not, see <https://www.gnu.org/licenses/>.

---

&copy; 2025 Álex M — [natone.pro](https://natone.pro)
