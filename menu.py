from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
from foods import *

class Menu:
    def __init__(self):
        aplicacion = QtWidgets.QApplication([])
        menu = uic.loadUi("gui/menu.ui")
        menu.show()
        food = Food()

        # Table Configuration
        menu.table_foods.setHorizontalHeaderLabels(['ID', 'Nombre Alimento', 'Gramos Proteína', 'Gramos Carbohidrato', 'Gramos Grasa'])
        menu.table_foods.setEditTriggers(QTableWidget.NoEditTriggers)
        menu.table_foods.setSelectionBehavior(QTableWidget.SelectRows)# select the entire row and not the field
        menu.table_foods.cellClicked.connect(self.select)

        menu.btn_add_food.clicked.connect(self.add)
        menu.btn_modify_food.clicked.connect(self.modify)
        menu.btn_delete_food.clicked.connect(self.delete)
        menu.btn_cancel.clicked.connect(self.cancel)
        
        sys.exit(aplicacion.exec())
    
    def add(self):
        print("Hola, soy la acción de agregar")

    def modify(self):
        print("Hola, soy la acción de modificar")

    def delete(self):
        print("Hola, soy la acción de eliminar")

    def cancel(self):
        print("Hola, soy la acción de cancelar")

    def validate_fields(self):
        if self.menu.txtNombre.text() == "" or self.menu.txtCorreo.text() == "":
            alerta = QMessageBox()
            alerta.setText('¡Debes llenar todos los campos!')
            alerta.setIcon(QMessageBox.Information)#ícono de mensaje
            alerta.exec()
            return True

    def consult(self):
        pass

    def select(self):
        id = self.menu.table_foods.selectedIndexes()[0].data()
        food_name = self.menu.table_foods.selectedIndexes()[1].data()
        protein_grams = self.menu.table_foods.selectedIndexes()[2].data()
        carbos_grams = self.menu.table_foods.selectedIndexes()[2].data()
        fat_grams = self.menu.table_foods.selectedIndexes()[2].data()
        print(id, food_name, protein_grams, carbos_grams, fat_grams)
        self.menu.txtId.setText(id)
        self.menu.txtNombre.setText(food_name)
        self.menu.txtCorreo.setText(protein_grams)
        self.menu.txtNombre.setText(carbos_grams)
        self.menu.txtCorreo.setText(fat_grams)
        self.menu.btn_add.setEnabled(False)

    def clean_spaces(self):
        pass

