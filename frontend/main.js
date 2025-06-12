// frontend/main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  // Crea la ventana principal
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      // Si no vas a usar funciones de Node en el renderer,
      // deja nodeIntegration: false y usa contextIsolation: true.
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // Carga el HTML de tu UI
  win.loadFile(path.join(__dirname, 'renderer', 'index.html'));

  // (Opcional) Abre las DevTools para debug
  // win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

// En macOS suele quedarse activo hasta que cierres explícitamente
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
