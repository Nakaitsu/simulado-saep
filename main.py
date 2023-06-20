from PyQt5.QtWidgets import QApplication
from Controllers.TelaInicial import TelaInicial

def startup():
  app = QApplication([])

  tela = TelaInicial()
  app.exec()

if __name__ == '__main__':
  startup()