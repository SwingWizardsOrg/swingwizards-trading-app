import sys
from gui.main_bar import MainBar
from gui.splash import SplashScreen  
from PyQt5.QtWidgets import QApplication


def check_splash_done(splash, window):
    if splash.counter >= 100:
        splash.timer.stop()
        window.show()


def main():
    app = QApplication(sys.argv)
    
    # Show splash screen
    splash = SplashScreen()  
    splash.show()
    
    # Initialize mainbar
    mainbar = MainBar()
   
    splash.timer.timeout.connect(lambda: check_splash_done(splash, mainbar))

    
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()