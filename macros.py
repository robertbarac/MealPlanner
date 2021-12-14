from math import log

class Macros:

    def calculo_macros(self, peso, altura, cintura, cuello, etapa, nivel_actividad):

        # fat percentage and lean body mass
        porcentaje_grasa = round(495 / ( 1.0324 - 0.19077 * log( (cintura - cuello), 10 ) + 0.15456 * log( altura, 10 )) - 450, 1)
        peso_sin_grasa = round(peso * ((100 - porcentaje_grasa)/100), 1)

        # basal metabolism: I used Katch-McArdle formula
        metabolismo_basal = round(370 + (21.6 * peso_sin_grasa))
        calorias_mantenimiento = round(metabolismo_basal * nivel_actividad)
        # Stage Selection
        if etapa == "Volumen":
            gramos_proteina, gramos_carbos, gramos_grasa, calorias = self.etapa_volumen(calorias_mantenimiento, peso)
        elif etapa == "Mantenimiento":
            gramos_proteina, gramos_carbos, gramos_grasa, calorias = self.etapa_mantenimiento(calorias_mantenimiento, peso)
        elif etapa == "Definición":
            gramos_proteina, gramos_carbos, gramos_grasa, calorias = self.etapa_definicion(calorias_mantenimiento, peso)
        #Para ahorrar funciones, ahora vamos a dividir aquí los macros en 4 partes iguales
        gr_pro_plato = round(gramos_proteina / 4)
        gr_carb_plato = round(gramos_carbos / 4)
        gr_grasa_plato = round(gramos_grasa / 4)

        return gramos_proteina, gramos_carbos, gramos_grasa, calorias, peso_sin_grasa, porcentaje_grasa, gr_pro_plato, gr_carb_plato, gr_grasa_plato

    def etapa_volumen(self, calorias_mantenimiento, peso):
        superavit = 250
        calorias_volumen = calorias_mantenimiento + superavit
        gramos_por_Kgpeso_proteina = 1.8
        gramos_diarios_proteina = round(gramos_por_Kgpeso_proteina * peso)
        #Calcular las calorías de las proteínas y restarlas de las calorías de volumen
        cal_proteína = gramos_diarios_proteina * 4
        remanente = calorias_mantenimiento + superavit
        remanente -= cal_proteína
        #Ahora los gramos de grasa y restarlas a las calorías remanentes
        gramos_grasa = 1.1
        gramos_diarios_grasa = round(gramos_grasa * peso)
        cal_grasa = gramos_diarios_grasa * 9
        remanente -= cal_grasa
        # Ahora por defecto, el restante serán los cálculos de gramos de carbos
        gramos_diarios_carbos = round(remanente / 4)

        return gramos_diarios_proteina, gramos_diarios_carbos, gramos_diarios_grasa, calorias_volumen

    def etapa_definicion(self, calorias_mantenimiento, peso):
        deficit = 400
        calorias_definicion = calorias_mantenimiento - deficit
        gramos_por_Kgpeso_proteina = 2.2
        gramos_diarios_proteina = round(gramos_por_Kgpeso_proteina * peso)
        #Calcular las calorías de las proteínas y restarlas de las calorías de volumen
        cal_proteína = gramos_diarios_proteina * 4
        remanente = calorias_mantenimiento - deficit #Aquí se resta el déficit
        remanente -= cal_proteína #aquí se restan las calorías de la proteína
        #Ahora los gramos de grasa y restarlas a las calorías remanentes
        gramos_grasa = 1
        gramos_diarios_grasa = round(gramos_grasa * peso)
        cal_grasa = gramos_diarios_grasa * 9
        remanente -= cal_grasa
        # Ahora por defecto, el restante serán los cálculos de gramos de carbos
        gramos_diarios_carbos = round(remanente / 4)

        return gramos_diarios_proteina, gramos_diarios_carbos, gramos_diarios_grasa, calorias_definicion

    def etapa_mantenimiento(self, calorias_mantenimiento, peso):
        gramos_por_Kgpeso_proteina = 1.8
        gramos_diarios_proteina = round(gramos_por_Kgpeso_proteina * peso)
        #Calcular las calorías de las proteínas y restarlas de las calorías de volumen
        cal_proteína = gramos_diarios_proteina * 4
        remanente = calorias_mantenimiento
        remanente -= cal_proteína
        #Ahora los gramos de grasa y restarlas a las calorías remanentes
        gramos_grasa = 1.1
        gramos_diarios_grasa = round(gramos_grasa * peso)
        cal_grasa = gramos_diarios_grasa * 9
        remanente -= cal_grasa
        # Ahora por defecto, el restante serán los cálculos de gramos de carbos
        gramos_diarios_carbos = round(remanente / 4)
        return gramos_diarios_proteina, gramos_diarios_carbos, gramos_diarios_grasa, calorias_mantenimiento
    
    def __Dg(self, array):
        return array[0][0]*array[1][1]*array[2][2] + array[1][0]*array[2][1]*array[0][2] + array[2][0]*array[0][1]*array[1][2] - array[0][0]*array[2][1]*array[1][2] - array[1][0]*array[0][1]*array[2][2] - array[2][0]*array[1][1]*array[0][2]

    def __Dx(self, array, prote_plato, carbos_plato, grasa_plato):
        return prote_plato*array[1][1]*array[2][2] + array[1][0]*array[2][1]*grasa_plato + array[2][0]*carbos_plato*array[1][2] - prote_plato*array[2][1]*array[1][2] - array[1][0]*carbos_plato*array[2][2] - array[2][0]*array[1][1]*grasa_plato

    def __Dy(self, array, prote_plato, carbos_plato, grasa_plato):
        return array[0][0]*carbos_plato*array[2][2] + prote_plato*array[2][1]*array[0][2] + array[2][0]*array[0][1]*grasa_plato - array[0][0]*array[2][1]*grasa_plato - prote_plato*array[0][1]*array[2][2] - array[2][0]*carbos_plato*array[0][2]

    def __Dz(self, array, prote_plato, carbos_plato, grasa_plato):
        return array[0][0]*array[1][1]*grasa_plato + array[1][0]*carbos_plato*array[0][2] + prote_plato*array[0][1]*array[1][2] - array[0][0]*carbos_plato*array[1][2] - array[1][0]*array[0][1]*grasa_plato - prote_plato*array[1][1]*array[0][2]
    
    def calculate_plate(self, marray, prote_plate, carbo_plate, fat_plate):
        #plato1 = [[29.7, 0.2, 4.9], [2.3, 30.9, 2.1], [1.3, 6.7 16.4]]
        dg = self.__Dg(marray)
        dx = self.__Dx(marray, prote_plate, carbo_plate, fat_plate)
        dy = self.__Dy(marray, prote_plate, carbo_plate, fat_plate)
        dz = self.__Dz(marray, prote_plate, carbo_plate, fat_plate)
        x, y, z = dx/dg, dy/dg, dz/dg
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if z < 0:
            z = 0
        return x, y, z
        
        
