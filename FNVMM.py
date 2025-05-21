#!/usr/bin/env python3
"""
FNV Mod Manager for Linux
Auto-detects FNV path, manages mods list, and supports Nexus Mods API.
by Álex M (me@natone.pro)
"""
import os
import sys
import json
import requests
import zipfile
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QFileDialog, QMessageBox, QListWidget,
    QHBoxLayout, QTabWidget
)
from PyQt5.QtCore import Qt

# --- Constants ---
CONFIG_FILE = os.path.expanduser("~/.config/fnv_mod_manager.json")
NEXUS_API_KEY = "YOUR_API_KEY_HERE"  # Register to Nexus Mods!
NEXUS_API_URL = "https://api.nexusmods.com/v1/games/falloutnewvegas/mods/{mod_id}.json"

class ModManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FNV Mod Manager (Linux) v0.3")
        self.setGeometry(300, 300, 800, 600)
        self.mod_list = []
        self.fnv_path = None

        # Initialize UI
        self.init_ui()
        self.load_config()

    def init_ui(self):
        """Set up the main window with tabs"""
        tabs = QTabWidget()

        # Tab 1: Install Mods
        self.tab_install = QWidget()
        self.setup_install_tab()
        
        # Tab 2: Installed Mods
        self.tab_mods = QWidget()
        self.setup_mods_tab()

        tabs.addTab(self.tab_install, "Install Mods")
        tabs.addTab(self.tab_mods, "Installed Mods")
        self.setCentralWidget(tabs)

    def setup_install_tab(self):
        """Install mods tab UI"""
        layout = QVBoxLayout()

        # Path selection
        path_layout = QHBoxLayout()
        self.path_label = QLabel("FNV Path: Not set")
        path_btn = QPushButton("Change Path")
        path_btn.clicked.connect(self.set_fnq_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(path_btn)

        # Mod input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter Nexus Mod ID or local file path")
        browse_btn = QPushButton("Browse Local File")
        browse_btn.clicked.connect(self.browse_file)
        
        # Install button
        install_btn = QPushButton("Install Mod")
        install_btn.clicked.connect(self.install_mod)
        
        # Status
        self.status = QLabel("Status: Ready")
        self.status.setAlignment(Qt.AlignCenter)

        layout.addLayout(path_layout)
        layout.addWidget(QLabel("Mod Source:"))
        layout.addWidget(self.input)
        layout.addWidget(browse_btn)
        layout.addWidget(install_btn)
        layout.addWidget(self.status)
        self.tab_install.setLayout(layout)

    def setup_mods_tab(self):
        """Installed mods list tab"""
        layout = QVBoxLayout()
        self.mod_list_widget = QListWidget()
        self.mod_list_widget.itemDoubleClicked.connect(self.remove_mod)
        
        layout.addWidget(QLabel("Double-click to remove mod:"))
        layout.addWidget(self.mod_list_widget)
        self.tab_mods.setLayout(layout)

    def load_config(self):
        """Load saved configuration"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.mod_list = data.get("mods", [])
                self.fnv_path = data.get("fnv_path")
                self.update_path_label()
                self.update_mod_list()

        if not self.fnv_path:
            self.auto_detect_fnq_path()

    def save_config(self):
        """Save current configuration"""
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump({
                "mods": self.mod_list,
                "fnv_path": self.fnv_path
            }, f, indent=2)

    def auto_detect_fnq_path(self):
        """Try to find FNV path automatically"""
        # Steam/Proton default location
        steam_path = os.path.expanduser("~/.steam/steam/steamapps/common/Fallout New Vegas")
        if os.path.exists(steam_path):
            self.fnv_path = steam_path
            self.update_path_label()
            return True
        return False

    def set_fnq_path(self):
        """Let user manually set FNV path"""
        path = QFileDialog.getExistingDirectory(self, "Select Fallout New Vegas Folder")
        if path:
            self.fnv_path = path
            self.update_path_label()
            self.save_config()

    def update_path_label(self):
        """Update the path display"""
        if self.fnv_path:
            self.path_label.setText(f"FNV Path: {self.fnv_path}")
        else:
            self.path_label.setText("FNV Path: Not set")

    def update_mod_list(self):
        """Refresh the installed mods list"""
        self.mod_list_widget.clear()
        for mod in self.mod_list:
            self.mod_list_widget.addItem(f"{mod['name']} (installed: {mod['date']})")

    def browse_file(self):
        """Open file dialog for local mods"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Mod File", "", "Mod Files (*.zip *.rar *.7z)"
        )
        if file_path:
            self.input.setText(file_path)

    def install_mod(self):
        """Main mod installation logic"""
        if not self.fnv_path:
            self.status.setText("Status: Error - No FNV path set!")
            return

        source = self.input.text().strip()
        if not source:
            self.status.setText("Status: Error - No mod specified!")
            return

        try:
            # Nexus Mods download
            if source.isdigit():
                mod_data = self.download_nexus_mod(int(source))
                mod_name = mod_data["name"]
                mod_file = os.path.join(self.fnv_path, f"{mod_name}.zip")
            # Local file
            else:
                mod_name = os.path.basename(source)
                mod_file = source

            # Extract to Data folder
            self.status.setText("Status: Installing mod...")
            with zipfile.ZipFile(mod_file, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(self.fnv_path, "Data"))

            # Add to mod list
            self.mod_list.append({
                "name": mod_name,
                "file": mod_file,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            self.save_config()
            self.update_mod_list()

            self.status.setText(f"Status: Installed {mod_name}!")
            QMessageBox.information(self, "Success", "Mod installed successfully!")

        except Exception as e:
            self.status.setText(f"Status: Error - {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to install mod: {str(e)}")

    def download_nexus_mod(self, mod_id):
        """Download mod from Nexus Mods API"""
        headers = {"apikey": NEXUS_API_KEY}
        
        # Get mod info
        info_url = NEXUS_API_URL.format(mod_id=mod_id)
        response = requests.get(info_url, headers=headers)
        response.raise_for_status()
        mod_data = response.json()

        # Download mod
        download_url = mod_data["download_url"]
        self.status.setText(f"Status: Downloading {mod_data['name']}...")
        mod_file = requests.get(download_url, headers=headers)
        
        # Save to FNV folder
        mod_path = os.path.join(self.fnv_path, f"{mod_data['name']}.zip")
        with open(mod_path, "wb") as f:
            f.write(mod_file.content)
            
        return mod_data

    def remove_mod(self, item):
        """Remove selected mod (doesn't delete files yet)"""
        mod_name = item.text().split(" (")[0]
        reply = QMessageBox.question(
            self, "Remove Mod",
            f"Remove {mod_name} from list? (This won't delete files)",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.mod_list = [m for m in self.mod_list if m["name"] != mod_name]
            self.save_config()
            self.update_mod_list()
            self.status.setText(f"Status: Removed {mod_name} from list")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModManager()
    window.show()
    sys.exit(app.exec_())
