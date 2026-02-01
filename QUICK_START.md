# Quick Start Guide

## Step-by-Step Instructions

### 1. Install Dependencies (One-time setup)
```bash
pip install -r requirements.txt
```

### 2. Start the Server
Open a terminal and run:
```bash
cd backend
python server.py
```

You should see:
```
Starting WebSocket server on ws://localhost:8765
Host should connect first, then fruit players can join
```

**Keep this terminal open!** The server must stay running.

### 3. Host Opens Their Game

**Method 1: Using the script (Easiest)**
```bash
./open_host.sh
```

**Method 2: Drag and Drop**
1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Open Finder (macOS) or File Explorer
3. Navigate to the `frontend` folder
4. **Drag** `host.html` and **drop** it into your browser window

**Method 3: Right-click and Open**
1. Navigate to the `frontend` folder in Finder/File Explorer
2. **Right-click** on `host.html`
3. Select **"Open With"** → Choose your browser (Chrome, Firefox, Safari, etc.)

**Method 4: From Browser**
1. Open your web browser
2. Press `Cmd+O` (macOS) or `Ctrl+O` (Windows/Linux) to open a file
3. Navigate to `frontend/host.html` and select it

Once open, wait for "Host registered!" message, then use **arrow keys** to control the snake.

### 4. Fruit Players Join

**Method 1: Using the script (Easiest)**
```bash
./open_fruit_player.sh
```

**Method 2: Drag and Drop**
1. Open your web browser
2. Open Finder (macOS) or File Explorer
3. Navigate to the `frontend` folder
4. **Drag** `fruit_player.html` and **drop** it into your browser window

**Method 3: Right-click and Open**
1. Navigate to the `frontend` folder
2. **Right-click** on `fruit_player.html`
3. Select **"Open With"** → Choose your browser

**Method 4: From Browser**
1. Open your web browser
2. Press `Cmd+O` (macOS) or `Ctrl+O` (Windows/Linux)
3. Navigate to `frontend/fruit_player.html` and select it

Once open, wait for "Registered!" message, then **click anywhere** on the board to move your fruit.

## Multiple Players

- **Same Computer**: Open `fruit_player.html` in multiple browser tabs/windows
- **Different Computers**: 
  - Make sure all computers are on the same network
  - Replace `localhost` with the server's IP address in the HTML files
  - Example: `ws://192.168.1.100:8765` (use your server's actual IP)

## Troubleshooting

**"Connection error" message?**
- Make sure the server is running (`python backend/server.py`)
- Check that the server terminal shows it's listening on port 8765

**Host can't connect?**
- Make sure you started the server first
- Check for any firewall blocking port 8765

**Fruit players can't connect?**
- Make sure the host has already connected first
- Check the server terminal for connection messages

## Stopping the Game

1. Close all browser windows
2. In the server terminal, press `Ctrl+C` to stop the server
