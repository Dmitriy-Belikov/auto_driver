import os
import subprocess
import platform
import time
from elevate import elevate

def driver():
  pc = platform.node() #Узнаем имя ПК
  #Команда powershell для получения модели ПК
  laptop_model = subprocess.getoutput(f'powershell (Get-WmiObject -class Win32_ComputerSystem -ComputerName {pc}).model').split()[1]
  #Получаем полный путь местонахождения программы
  path_flash = os.path.splitdrive(os.getcwd())
  #Формируем путь до папки с драйверами на основе имени диска usb и модели ноутбука
  path_drivers = rf'{path_flash[0]}\Soft\Drivers\{laptop_model}'

  '''{path_flash[0]} - диск на котором запущена программа, \Soft\Drivers\ - путь до модели, {laptop_model} - модель ноутбука
  Полный путь получается: D:\Soft\Drivers\5430
  Для извлечения драйверов запускаем powershell от админа и выполняем команду export-windowsdriver -online -destination c:\drivers
  Драйвера сохранятся c:\drivers
  После можно переименовать папку в модель ноутбука и закинуть на флешку
  '''

  try:
    #Проверяем, есть ли модель ноутбука в списке драйверов
    os.listdir(path_drivers)
    print(f'Устанавливаю драйвера для {laptop_model}')
    #powershell команда установки драйверов из папки path_drivers
    subprocess.run(rf'powershell PNPUTIL /add-driver {path_drivers}\*.inf /subdirs /install')
  except:
    #Если драйверов под модель не найдено, выйдет надпись, надпись будет висеть 60 секунд
    print(f'Драйверы для {laptop_model} не найдены')
    time.sleep(60)


if __name__ == '__main__':
  elevate()#Нужна для запуска с повышенными привелегиями
  driver()#Запуск самой функции
