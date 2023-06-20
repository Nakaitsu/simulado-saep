from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
import Modules.database as db
from PyQt5.QtCore import pyqtSignal

class TelaVendas(QMainWindow):
  closed = pyqtSignal()

  def __init__(self, parent = None, id = None):
    super(TelaVendas, self).__init__(parent)
    uic.loadUi('UI/vendas.ui', self)

    self.parent = parent
    self.id = id
    self.btnFinalizar.clicked.connect(self.concluirVenda)

    self.veiculo = db.getVeiculoPorId(self.id)
    
    listaClientes = db.getClientes()
    listaConcessionarias = db.getConcessionarias()

    self.cbbClientes.addItem('[ selecionar ]', '')
    for cliente in listaClientes:
      self.cbbClientes.addItem(cliente['nome'], cliente['id'])

    self.cbbConcessionarias.addItem('[ selecionar ]', '')
    for concecionaria in listaConcessionarias:
      self.cbbConcessionarias.addItem(concecionaria['nome'], concecionaria['id'])

    self.lblModelo.setText(self.veiculo['modelo'])

    self.show()

  def concluirVenda(self):
    if self.cbbConcessionarias.currentIndex() > 0 and self.cbbClientes.currentIndex() > 0:
      idConcessionaria = self.cbbConcessionarias.currentData()
      idCliente = self.cbbClientes.currentData()

      db.insertVenda(self.veiculo['id'], idCliente, idConcessionaria, self.parent.area)

      QMessageBox.information(self, 'Sucesso', 'Venda realizada com sucesso!')

      self.close()

  def closeEvent(self, event):
    self.closed.emit()
    super(TelaVendas, self).closeEvent(event)