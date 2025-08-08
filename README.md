# Local Media PWA

A lightweight **local network media browser** built with FastAPI + PWA frontend.  
Admins (localhost only) can set the media folder and rescan at any time.  
LAN users can browse and stream media without admin access.

---

## Features
- **Admin panel** (localhost only) to:
  - Choose and save the media root folder
  - Trigger rescans of media files
- **User view** (LAN) for:
  - Browsing images, videos, and audio files
  - Streaming media directly in the browser
- **PWA ready** – can be installed on phones or desktops
- **Supported formats**:
  - Video: `.mp4`, `.mkv`, `.webm`, `.avi`
  - Audio: `.mp3`, `.aac`, `.flac`, `.wav`
  - Images: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`

---

## Requirements
- **Windows** (tested)  
- **Python 3.12** installed and on PATH
- Local network connection for multi-device access

---

## Quick Start

### 1. Extract & open in VS Code
Unzip the project into a folder (e.g., `C:\local-media-pwa`)  
Open the folder in VS Code.

### 2. Set port (optional)
Edit `run_server.bat` and set your preferred port:
```bat
set "PORT=8080"
