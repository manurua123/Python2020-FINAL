
from datetime import datetime, date, time, timedelta


fecha = datetime.now()  # Obtiene fecha y hora actual
fecha = "{} de {} del {}".format(fecha.day, fecha.month, fecha.year)
print(fecha)
