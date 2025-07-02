import sys
from gui.main_bar import MainBar
from gui.splash import SplashScreen  # This is correct
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QToolButton, QSizePolicy, QWidget, QDockWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPoint


def check_splash_done(splash, window):
    if splash.counter >= 100:
        splash.timer.stop()
        window.show()


def main():
    app = QApplication(sys.argv)
    
    # Show splash screen
    splash = SplashScreen()  # Create instance directly
    splash.show()
    
    # Initialize mainbar
    mainbar = MainBar()
   
    splash.timer.timeout.connect(lambda: check_splash_done(splash, mainbar))

    
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()