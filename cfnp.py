
import os
import shutil
import datetime
import PySimpleGUI as sg

# -- -- --
'''  Функции  '''


# -- -- --

# Эта Функция должна ускорить скорость копирования
def _copyfileobj_patched(fsrc, fdst, length=16 * 1024 * 1024):
    while 1:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)


# Окно для записи пути к папке
def window_enter_a_path(team_cap, input_name_command, path_to_save):
    layout = [[sg.Text(input_name_command)],
              [sg.InputText(path_to_save), sg.FolderBrowse()],
              [sg.Button('Ok')], ]
    window = sg.Window(team_cap,
                       layout,
                       keep_on_top=True)
    button, values = window.read()
    window.close()
    return button, values


# Окно для написания текста
def window_enter_a_text(team_cap, input_name_command, value_to_save):
    layout = [[sg.Text(input_name_command)],
              [sg.InputText(value_to_save)],
              [sg.Button('Ok')]]
    window = sg.Window(team_cap,
                       layout,
                       keep_on_top=True)
    button, values = window.read()
    window.close()
    return button, values


# Окно для вывода результата работы программы
def window_result(time):
    sg.set_options(text_justification='right')
    layout = [[sg.Text("Время создания папки проекта " + (str(time)) + ' сек')], [sg.Button("OK")]]
    sg.set_options(text_justification='left')
    window = sg.Window('Завершение',
                       layout,
                       keep_on_top=True)
    button, values = window.read()
    window.close()


# Ввод пути к корневой папке
def enter_a_path(var, save_addres):
    button, values = window_enter_a_path('Корневая папка',
                                         'Выберите место расположения папки с проектом',
                                         read_value_var(var, save_addres))
    f1 = str(values[0])
    f1 = f1.replace('\n', '')
    if button == sg.WIN_CLOSED:
        window.close()
    elif any((button != 'Ok', f1 == '')):
        sg.popup_error('Операционная ошибка')
    else:
        print_value_var(var, f1, save_addres)
        return f1


# Ввод шифра проекта
def code_project(var, save_addres):
    button, values = window_enter_a_text('Шифр проекта',
                                         'Введите шифр проекта (пример: 0000.0000)',
                                         read_value_var(var, save_addres))
    f1 = str(values[0])

    if button == sg.WIN_CLOSED:
        window.close()
    elif any((button != 'Ok', f1 == '')):
        sg.popup_error('Операционная ошибка')
    else:
        print_value_var(var, f1, save_addres)
        return f1


# Ввод короткого рабочего названия проекта
def name_project(var, save_addres):
    button, values = window_enter_a_text('Название проекта',
                                         'Введите короткое рабочее название проекта',
                                         read_value_var(var, save_addres))
    f1 = str(values[0])

    if button == sg.WIN_CLOSED:
        window.close()
    elif any((button != 'Ok', f1 == '')):
        sg.popup_error('Операционная ошибка')
    else:
        print_value_var(var, f1, save_addres)
        return f1


# Ввод города места проектирования
def name_project_sity(var, save_addres):
    button, values = window_enter_a_text('Город',
                                         'Введите город объекта проектирования',
                                         read_value_var(var, save_addres))
    f1 = str(values[0])

    if button == sg.WIN_CLOSED:
        window.close()
    elif any((button != 'Ok', f1 == '')):
        sg.popup_error('Операционная ошибка')
    else:
        print_value_var(var, f1, save_addres)
        return f1


# Ввод пути расположения образца папки проекта
def path_sample(var, save_addres):
    button, values = window_enter_a_path('Путь к образцу',
                                         'Введите путь расположения образца папки проекта (0000.0000 Пример)',
                                         read_value_var(var, save_addres))
    f1 = str(values[0])
    f1 = f1.replace('\n', '')
    if button == sg.WIN_CLOSED:
        window.close()
    elif any((button != 'Ok', f1 == '')):
        sg.popup_error('Операционная ошибка')
    else:
        print_value_var(var, f1, save_addres)
        return f1


# Извлекаем значение необходимой переменной из сейва
def read_value_var(var, save_addres):
    n = 0
    value = ''
    with open(save_addres, "r") as file:
        line = file.readline()
        while line:
            if (line.count(var)) > 0:
                value = line
            n += 1
            line = file.readline()
    if not (value == ''):
        value1 = value.split('=')
        if not (value1 == -1):
            value = value1[1]
        else:
            value = ''
        value = value.replace('\n', '')
    return (value)


# Переписываем значение переменной в сейве
def print_value_var(var, value_var, save_addres):
    n = 0
    value_n = ''
    with open(save_addres, "r") as file:
        line = file.readline()
        while line:
            if ((line.count(var)) > 0):
                value_n = n
            n += 1
            line = file.readline()
    if not (value_n == ''):
        with open(save_addres, "r") as file:
            line_1 = file.readlines()
            line_1[value_n] = var + '=' + value_var + '\n'
        with open(text_s_file, "w") as file:
            for n in range(0, len(line_1)):
                file.write(line_1[n])
    else:
        with open(save_addres, "a") as file:
            file.write(var + '=' + value_var + '\n')
    """ Зачищаем пробелы """
    with open(save_addres, "r") as file:
        line_1 = file.readlines()
        x = len(line_1)
        n = 0
        while n < x:
            if line_1[n] == '\n':
                line_1.pop(n)
                x -= 1
                n -= 1
            n += 1
    with open(save_addres, "w") as file:
        for n in range(0, len(line_1)):
            file.write(line_1[n])


# -- -- --
'''  Основное тело программы  '''
# -- -- --

shutil.copyfileobj = _copyfileobj_patched  # Должно ускорить скорость копирования
sg.theme('Dark2')  # Определяем стиль окна
slh = "\\"

# создание txt-файла для сохранения данных, если такого файла не было
name_prog_dir = (os.getcwd())
d = 0
text_s_file = name_prog_dir + slh + 'Create_folder_new_project - save.txt'
for dirpath, dirnames, filenames in os.walk(name_prog_dir):
    for filename in filenames:
        name_nn = os.path.join(dirpath, filename)
        if name_nn.count("Create_folder_new_project - save.txt") > 0:
            d += 1
if d == 0:
    print("!")
    text_file = open(text_s_file, "w")
# ---

adres_1 = enter_a_path('adres_1', text_s_file)
name_pro_code = code_project('name_pro_code', text_s_file)
name_pro_nickname = name_project('name_pro_nickname', text_s_file)
name_pro_sity = name_project_sity('name_pro_sity', text_s_file)
path = path_sample('path', text_s_file)

print('Начался процесс создания папки проекта')
time_0 = datetime.datetime.now()  # Запуск таймера
print(str(time_0))
print('Ожидайте...')

parent_dirr = []
new_folder = name_pro_code + " " + name_pro_nickname + ". " + name_pro_sity  # определяем название файла
# print (new_folder)
if not os.path.isdir(adres_1 + slh + new_folder):
    full_name = (adres_1 + slh + new_folder)
    # os.mkdir(full_name)
    for dirpath, dirnames, filenames in os.walk(path):
        # перебрать каталоги
        for dirname in dirnames:
            name_d = os.path.join(dirpath, dirname)
            name_d = name_d.replace(path, full_name)
            # print (name_d)
            os.makedirs(name_d)
        for filename in filenames:
            name_f = os.path.join(dirpath, filename)
            if (not (name_f.count("011 СМ\\Старое") > 0
                     or name_f.count(".JPG") > 0
                     or name_f.count(".pdf") > 0
                     or name_f.count("Thumbs") > 0
                     or name_f.count(".PDF") > 0
                     or name_f.count(".jpg") > 0) or name_f.count(".py") > 0):
                # print (not name_f.count("011 СМ\\Старое", ".JPG" or "001 ПД" or ".pdf" or "Thumbs" or ".PDF")>0)
                name_f = name_f.replace(path, full_name)
                shutil.copy(os.path.join(dirpath, filename), name_f)
                if name_f.count("0000.0000") > 0:
                    os.rename(name_f, name_f.replace("0000.0000", name_pro_code))

time_1 = datetime.datetime.now()
print(str(time_1))
time_d = time_1 - time_0
time1 = str(time_d.seconds)
window_result(time1)
