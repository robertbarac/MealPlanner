from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
from foods import Food

class Menu:
    def __init__(self):
        aplicacion = QtWidgets.QApplication([])
        self.menu = uic.loadUi("gui/menu.ui")
        self.menu.show()
        self.food = Food()
        self.consult()
        # Table Configuration
        self.menu.table_foods.setHorizontalHeaderLabels(['ID', 'Nombre Alimento', 'Gramos Proteína', 'Gramos Carbohidrato', 'Gramos Grasa'])
        self.menu.table_foods.setEditTriggers(QTableWidget.NoEditTriggers)
        self.menu.table_foods.setSelectionBehavior(QTableWidget.SelectRows)# select the entire row and not the field
        self.menu.table_foods.cellClicked.connect(self.select)

        self.menu.line_id.setReadOnly(True)
        self.menu.btn_add_food.clicked.connect(self.add)
        self.menu.btn_modify_food.clicked.connect(self.modify)
        self.menu.btn_delete_food.clicked.connect(self.delete)
        self.menu.btn_cancel.clicked.connect(self.cancel)
        
        sys.exit(aplicacion.exec())
    
    def add(self):
        if self.validate_fields():
            return False
        food_name = self.menu.line_food_name.text() # It's like the get method of Tkinter
        prot_grams = self.menu.dsb_protein_grams.text().replace(',', '.')
        carb_grams = self.menu.dsb_carbos_grams.text().replace(',', '.')
        fat_grams = self.menu.dsb_fat_grams.text().replace(',', '.')
        self.food.add_food((food_name, prot_grams, carb_grams, fat_grams))
        self.consult()
        


    def modify(self):
        food_name = self.menu.line_food_name.text()
        id = self.menu.line_id.text()
        protein_grams = self.menu.dsb_protein_grams.text().replace(',', '.')
        carbos_grams = self.menu.dsb_carbos_grams.text().replace(',', '.')
        fat_grams = self.menu.dsb_fat_grams.text().replace(',', '.')
        self.food.modify_food((food_name , protein_grams, carbos_grams, fat_grams, id))
        self.consult()

    def delete(self):
        id = self.menu.line_id.text()
        self.food.delete_food(id)
        self.consult()

    def cancel(self):
        self.consult()


    def validate_fields(self):
        if self.menu.line_food_name.text() == "" or (self.menu.dsb_protein_grams.value() == "0.0" and self.menu.dsb_carbos_grams.value() == "0.0" and self.menu.dsb_fat_grams.value() == "0.0"):
            alerta = QMessageBox()
            alerta.setText('¡Debes llenar todos los campos!')
            alerta.setIcon(QMessageBox.Information)#ícono de mensaje
            alerta.exec()
            return True

    def consult(self):
        self.menu.table_foods.setRowCount(0) # limpiar la tabla 
        index_control = 0
        foods = self.food.read_foods()
        for food in foods:
            self.menu.table_foods.setRowCount(index_control + 1)
            self.menu.table_foods.setItem(index_control, 0, QTableWidgetItem(str(food[0])))
            self.menu.table_foods.setItem(index_control, 1, QTableWidgetItem(str(food[1])))
            self.menu.table_foods.setItem(index_control, 2, QTableWidgetItem(str(food[2])))
            self.menu.table_foods.setItem(index_control, 3, QTableWidgetItem(str(food[3])))
            self.menu.table_foods.setItem(index_control, 4, QTableWidgetItem(str(food[4])))
            index_control += 1
        self.menu.btn_add_food.setEnabled(True)
        self.menu.btn_modify_food.setEnabled(False)
        self.menu.btn_delete_food.setEnabled(False)
        self.menu.btn_cancel.setEnabled(False)

    def select(self):
        id = self.menu.table_foods.selectedIndexes()[0].data()
        food_name = self.menu.table_foods.selectedIndexes()[1].data()
        protein_grams = self.menu.table_foods.selectedIndexes()[2].data()
        carbos_grams = self.menu.table_foods.selectedIndexes()[3].data()
        fat_grams = self.menu.table_foods.selectedIndexes()[4].data()
        self.menu.line_id.setText(id)
        self.menu.line_food_name.setText(food_name)
        self.menu.dsb_protein_grams.setValue(float(protein_grams))
        self.menu.dsb_carbos_grams.setValue(float(carbos_grams))
        self.menu.dsb_fat_grams.setValue(float(fat_grams))
        self.menu.btn_add_food.setEnabled(False)
        self.menu.btn_modify_food.setEnabled(True)
        self.menu.btn_delete_food.setEnabled(True)
        self.menu.btn_cancel.setEnabled(True)

    def clean_fields(self):
        pass

