const {app, ipcMain, BrowserWindow} = require('electron');

function createWindow() {
    const mainWindow = new BrowserWindow({
        minWidth:850,
        minHeight:850,
        width:1000,
        height:1000,
        titleBarStyle:'hidden',
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true, // Enable remote module for fullscreen apps
        },
    });

    const appurl = "http://127.0.0.1:8000/agents/talk/";
    mainWindow.loadURL(appurl);



    ipcMain.on('window-action', (event, action) => {
        switch (action) {
            case 'minimize':
                mainWindow.minimize();
                break;
            case 'toggle-maximize':
                if (mainWindow.isMaximized()) {
                    mainWindow.unmaximize();
                } else {
                    mainWindow.maximize();
                }
                break;
            case 'close':
                mainWindow.close();
                break;
        }
    });

    ipcMain.handle('window-action', async (event, action) => {
        if (action === 'is-maximized') {
            return mainWindow.isMaximized();
        }
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
