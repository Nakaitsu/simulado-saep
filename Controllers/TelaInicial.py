import Modules.database as db
from Controllers.TelaDetalhes import TelaDetalhes
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

class TelaInicial(QMainWindow):
  def __init__(self):
    super(TelaInicial, self).__init__()
    uic.loadUi('UI/inicial.ui', self)

    self.botoes = []
    self.botoes.append(self.btnArea1)
    self.botoes.append(self.btnArea2)
    self.botoes.append(self.btnArea3)
    self.botoes.append(self.btnArea4)
    self.botoes.append(self.btnArea5)
    self.botoes.append(self.btnArea6)
    self.botoes.append(self.btnArea7)
    self.botoes.append(self.btnArea8)
    self.botoes.append(self.btnArea9)
    self.botoes.append(self.btnArea10)
    self.botoes.append(self.btnArea11)

    self.atualizarAreas()

    self.show()

  def atualizarAreas(self):
    listaAreas = db.getAreas()

    for botao in self.botoes:
      idBotao = int(botao.text())
      area = next((a for a in listaAreas if a['id'] == idBotao), None)

      if area and area['quantidade'] > 0:
        botao.clicked.connect(self.gerarAreaClickListener(area['id']))
        botao.setStyleSheet('background-color: #0000FF; color: #FFFFFF')
      else:
        botao.clicked.connect(lambda: QMessageBox.warning(self, 'Indisponível', 'A área selecionada está vazia!'))

  def gerarAreaClickListener(self, idArea):
    def Listener():
      self.mostrarDetalhesArea(idArea)

    return Listener

  def mostrarDetalhesArea(self, idArea):
    self.hide()
    tela = TelaDetalhes(self, idArea)
    tela.closed.connect(self.childClosed)

  def childClosed(self):
    self.atualizarAreas()
    self.show()