from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
from foods_db_conexion import Food
from macros import Macros

class Menu:
    def __init__(self):
        aplicacion = QtWidgets.QApplication([])
        self.menu = uic.loadUi("gui/menu.ui")
        self.menu.show()
        self.food = Food()
        self.macros = Macros()
        self.consult()
        # Table Configuration
        self.menu.table_foods.setHorizontalHeaderLabels(['ID', 'Nombre Alimento', 'Gramos Proteína', 'Gramos Carbohidrato', 'Gramos Grasa'])
        self.menu.table_foods.setEditTriggers(QTableWidget.NoEditTriggers)
        self.menu.table_foods.setSelectionBehavior(QTableWidget.SelectRows)# select the entire row and not the field
        self.menu.table_foods.cellClicked.connect(self.select)

        self.menu.line_id.setReadOnly(True)
        #Click events for the CRUD of the food
        self.menu.btn_add_food.clicked.connect(self.add)
        self.menu.btn_modify_food.clicked.connect(self.modify)
        self.menu.btn_delete_food.clicked.connect(self.delete)
        self.menu.btn_cancel.clicked.connect(self.cancel)
        self.menu.btn_search_food.clicked.connect(self.search_food)
        self.menu.btn_clean_search.clicked.connect(self.clean_search_field)
        
        # Click events for the macros calculation and plates calculation
        self.menu.btn_calculate_macros.clicked.connect(self.calculate_macros)
        self.menu.btn_calculate_plates.clicked.connect(self.calculate_plates)
        
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
        if self.validate_fields():
            return False
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
        self.menu.table_foods.setRowCount(0) # Cleaning the table
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
        self.enable_add()

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
        self.unable_add()

    def clean_search_field(self):
        self.menu.line_search_food.setText("")
        self.consult()
        

    def unable_add(self):
        self.menu.btn_add_food.setEnabled(False)
        self.menu.btn_modify_food.setEnabled(True)
        self.menu.btn_delete_food.setEnabled(True)
        self.menu.btn_cancel.setEnabled(True)
    
    def enable_add(self):
        self.menu.btn_modify_food.setEnabled(True)
        self.menu.btn_modify_food.setEnabled(False)
        self.menu.btn_delete_food.setEnabled(False)
        self.menu.btn_cancel.setEnabled(False)
    
    def unable_all_crud_buttons(self):
        self.menu.btn_add_food.setEnabled(False)
        self.menu.btn_modify_food.setEnabled(False)
        self.menu.btn_delete_food.setEnabled(False)
        self.menu.btn_cancel.setEnabled(False)

    def search_food(self):
        if self.menu.line_search_food.text() != "":
            food_name = self.menu.line_search_food.text()
            search = self.food.search_food(food_name)
            self.menu.table_foods.setRowCount(0)
            index_control = 0
            for food in search:
                self.menu.table_foods.setRowCount(index_control + 1)
                self.menu.table_foods.setItem(index_control, 0, QTableWidgetItem(str(food[0])))
                self.menu.table_foods.setItem(index_control, 1, QTableWidgetItem(str(food[1])))
                self.menu.table_foods.setItem(index_control, 2, QTableWidgetItem(str(food[2])))
                self.menu.table_foods.setItem(index_control, 3, QTableWidgetItem(str(food[3])))
                self.menu.table_foods.setItem(index_control, 4, QTableWidgetItem(str(food[4])))
                index_control += 1
            self.unable_all_crud_buttons()
        else:
            alerta = QMessageBox()
            alerta.setText('\tEntrada vacía. \nEscribe un alimento en la entrada para poder buscar')
            alerta.setIcon(QMessageBox.Information)#ícono de mensaje
            alerta.exec()
    
    def calculate_macros(self):
        weight = float(self.menu.dsb_weight.value())
        height = float(self.menu.sb_height.value())
        waist = float(self.menu.sb_waist.value())
        neck = float(self.menu.sb_neck.value())
        activity_level = float(self.menu.dsb_activity_level.value())
        goal = str(self.menu.cb_goal.currentText())
        global protein_in_plate, carbos_inplate, fat_in_plate
        protein_grams, carbos_grams, fat_grams, calories, lean_body_mass, fat_percentage, protein_in_plate, carbos_inplate, fat_in_plate = self.macros.calculo_macros(weight, height, waist, neck, goal, activity_level)
        string = f"Tiene {calories} calorías diarias. Proteína: {protein_grams}; Carbohidratos: {carbos_grams}; Grasa: {fat_grams}\nPeso libre de grasa: {lean_body_mass}; porcentaje de grasa: {fat_percentage}%\nGramos de macronutrientes respectivos por plato (4 platos): {protein_in_plate}, {carbos_inplate} y {fat_in_plate}"
        self.menu.label_macros_results.setText(string)

    def calculate_plates(self):

        id_f1_p1 = self.menu.sb_a1_p1.value()
        id_f2_p1 = self.menu.sb_a2_p1.value()
        id_f3_p1 = self.menu.sb_a3_p1.value()
        id_f1_p2 = self.menu.sb_a1_p2.value()
        id_f2_p2 = self.menu.sb_a2_p2.value()
        id_f3_p2 = self.menu.sb_a3_p2.value()
        id_f1_p3 = self.menu.sb_a1_p3.value()
        id_f2_p3 = self.menu.sb_a2_p3.value()
        id_f3_p3 = self.menu.sb_a3_p3.value()
        id_f1_p4 = self.menu.sb_a1_p4.value()
        id_f2_p4 = self.menu.sb_a2_p4.value()
        id_f3_p4 = self.menu.sb_a3_p4.value()
        #plate1
        search1 = self.food.search_food_by_id(id_f1_p1)
        search2 = self.food.search_food_by_id(id_f2_p1)
        search3 = self.food.search_food_by_id(id_f3_p1)
        #plate2
        search4 = self.food.search_food_by_id(id_f1_p2)
        search5 = self.food.search_food_by_id(id_f2_p2)
        search6 = self.food.search_food_by_id(id_f3_p2)
        #plate3
        search7 = self.food.search_food_by_id(id_f1_p3)
        search8 = self.food.search_food_by_id(id_f2_p3)
        search9 = self.food.search_food_by_id(id_f3_p3)
        #plate4
        search10 = self.food.search_food_by_id(id_f1_p4)
        search11 = self.food.search_food_by_id(id_f2_p4)
        search12 = self.food.search_food_by_id(id_f3_p4)
        plate1 = [[float(search1[0][1]), float(search1[0][2]), float(search1[0][3])], [float(search2[0][1]), float(search2[0][2]), float(search2[0][3])], [float(search3[0][1]), float(search3[0][2]), float(search3[0][3])]]
        plate2 = [[float(search4[0][1]), float(search4[0][2]), float(search4[0][3])], [float(search5[0][1]), float(search5[0][2]), float(search5[0][3])], [float(search6[0][1]), float(search6[0][2]), float(search6[0][3])]]
        plate3 = [[float(search7[0][1]), float(search7[0][2]), float(search7[0][3])], [float(search8[0][1]), float(search8[0][2]), float(search8[0][3])], [float(search9[0][1]), float(search9[0][2]), float(search9[0][3])]]
        plate4 = [[float(search10[0][1]), float(search10[0][2]), float(search10[0][3])], [float(search11[0][1]), float(search11[0][2]), float(search11[0][3])], [float(search12[0][1]), float(search12[0][2]), float(search12[0][3])]]

        grams_food1, grams_food2, grams_food3 = self.macros.calculate_plate(plate1, protein_in_plate, carbos_inplate, fat_in_plate)
        grams_food4, grams_food5, grams_food6 = self.macros.calculate_plate(plate2, protein_in_plate, carbos_inplate, fat_in_plate)
        grams_food7, grams_food8, grams_food9 = self.macros.calculate_plate(plate3, protein_in_plate, carbos_inplate, fat_in_plate)
        grams_food10, grams_food11, grams_food12 = self.macros.calculate_plate(plate4, protein_in_plate, carbos_inplate, fat_in_plate)
        string = f"Plato 1: {round(grams_food1 * 100)} gramos de {search1[0][0]}, {round(grams_food2 * 100)} de {search2[0][0]} y {round(grams_food3 * 100)} de {search3[0][0]}."
        string += f"\nPlato 2: {round(grams_food4 * 100)} gramos de {search4[0][0]}, {round(grams_food5 * 100)} de {search5[0][0]} y {round(grams_food6 * 100)} de {search6[0][0]}."
        string += f"\nPlato 3: {round(grams_food7 * 100)} gramos de {search7[0][0]}, {round(grams_food8 * 100)} de {search8[0][0]} y {round(grams_food9 * 100)} de {search9[0][0]}."
        string += f"\nPlato 4: {round(grams_food10 * 100)} gramos de {search10[0][0]}, {round(grams_food11 * 100)} de {search11[0][0]} y {round(grams_food12 * 100)} de {search12[0][0]}."

        self.menu.label_plates_results.setText(string)

