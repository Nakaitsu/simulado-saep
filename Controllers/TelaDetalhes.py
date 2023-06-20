import Modules.database as db
from Controllers.TelaVendas import TelaVendas
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

class TelaDetalhes(QMainWindow):
  closed = pyqtSignal()

  def __init__(self, parent = None, idArea = None):
    super(TelaDetalhes, self).__init__(parent)
    uic.loadUi('UI/detalhes.ui', self)

    self.area = idArea
    self.parent = parent
    self.veiculoSelecionado = None
    self.setWindowTitle(f'{self.windowTitle()} {self.area}')
    self.lblArea.setText(f'ÁREA {self.area}')

    self.btnVender.clicked.connect(self.vender)

    self.atualizarVeiculos()

    self.cbbVeiculos.currentIndexChanged.connect(self.cbbVeiculos_indexChanged)

    self.show()

  def atualizarVeiculos(self):
    self.cbbVeiculos.clear()
    
    self.veiculos = db.getVeiculosPorArea(self.area)

    self.cbbVeiculos.addItem('[ selecionar ]', '')
    for veiculo in self.veiculos:
      self.cbbVeiculos.addItem(veiculo['modelo'], veiculo['id'])

  def cbbVeiculos_indexChanged(self, index):
    if index > 0:
      veiculo = next((v for v in self.veiculos if v['id'] == self.cbbVeiculos.currentData()), None)

      if veiculo:
        self.lblModelo.setText(veiculo['modelo'])
        self.lblPreco.setText(str(veiculo['preco']))
    else:
        self.lblModelo.setText('')
        self.lblPreco.setText('')

  def vender(self):
    if self.cbbVeiculos.currentIndex() > 0:
      self.hide()
      tela = TelaVendas(self, int(self.cbbVeiculos.currentData())) 
      tela.closed.connect(self.childClosed)
    else:
      QMessageBox.warning(self, 'Erro', 'Selecione um modelo')

  def closeEvent(self, event):
    self.closed.emit()
    super(TelaDetalhes, self).closeEvent(event)

  def childClosed(self):
    self.atualizarVeiculos()
    self.show()