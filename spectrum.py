def read(path):
    A = []    # Будущая матрица (вектор). Идея в том, чтобы перевести значения из двоичной системы в десятиричную
    with open(path) as f:
        for line in f:
            A.append(line.rstrip())
        n = len(A[0])    # Длина вектора, т.к. вектора должны быть равной длины. Взяли вектор [0]
        size = len(A)    # Количество векторов (строк) в файле

        for i in range(size):    # Проверим, что входной файл соотвестует необходимым критериям. Если нет, останавливаем процесс обработки.
            if len(A[i]) != n:
                first_message = "Размер строк данных имеет разные длины"
                second_message = "Строка: " + str(i)+" отличается от первой строки"
                return(print(first_message), print(second_message),print("Обработка остановлена..."))
            else:
                for j in range(n):
                    if int(A[i][j]) > 1:
                        first_message = "Входной файл содержит значение > 1. Вам нужно использовать только 0 и 1 значения во входном файле."
                        second_message = "Строка: " + str(i) + " Позиция: " + str(j)
                        return(print(first_message), print(second_message),print("Обработка остановлена..."))

        for i in range(len(A)):    # Перевод из двоичной системы
            A[i] = int(A[i],2)
    return(A, n, size)

def result(A,n,size):
    result = []    # Вектор, в котором будут записываться сумма биномиальных коэффициентов для n-й (n - количество строк) степени с индексом в качестве веса. 
    if n < size:    # Если длина вектора меньше количества векторов (строк), тогда значение биномальных коэффициентов симметрично. Биномальный коэффициент для n - длины.
        weight = [1]    # Пустой единичный вектор, для произведения
        for i in range(1,n+1): 
            weight.append(weight[i-1] * ((n-i+1))//i)    # Значение int, при возведении в степень, ограниченно вместимостью float. На выходе получаем округление.
            weight = [int(x) for x in weight]
        result = [int(x * 2**(size - n)) for x in weight]    # Находим корень (длина вектора - количество строк) для полученных произведений.
    
    elif n > size:    # Если длина вектора больше количества векторов (строк), меняем их значения местами для нахождения значений базиса.
        n, size = size, n
        #Посчитаем базис
        for r in range(2):
            basis = []
            for j in range(n):
                length = len(bin(A[j])[2:]) - 1
                for i in range(n):
                    if (A[i] & 2**length):
                        if i != j:
                            A[i] ^= A[j]
                    basis.append(A[i])
        #Поменяем местами значение длины вектора и количества строк.
        n, size = size, n
        #Производим рассчет биномальных коэффициентов, по найденому базису.
        weight = [0]*(n+1)    # Создаем пустой вектор, равного длине вектора (n+1, т.к. есть значение веса 0).
        for i in range(1):
            z = int(2**(size) * i)    # Посчитаем значение диапазона для значения 1. 
            zc = z ^ (z//2)    # Операция XOR. 
            temp = 0    # Временная переменная
            for k in range(zc):
                if zc % 2 == 1:    # Деление по модулю на 2.
                    temp ^= basis[k]    # XOR и присваивание.
                    zc // 2    # Держим int.
                
            location = bin(temp).count('1')    # Преобразование значений в двоичные строки и считаем количество совпадений с 1
            weight[location] += 1    # Распределению по весу вектора. (Количество единиц).
            
            elder, original = zc, (z+1) ^ ((z+1)//2)    # Присваиваем значения, для подсчета длины.
            for j in range(z + 1, int(2**(size) * (i+1))):
                id_j = bin(elder - original)[::-1].find('1')    # Ищем первое совпадание с 1 в двоичном значении. 
                temp ^= basis[id_j]    # XOR и присваивание.
                location = bin(temp).count('1') 
                weight[location] += 1
                elder, original = original, (j+1) ^ ((j+1)//2)    # Возвращаем значение длины в original для последующего сравния с предыдущем elder.
            result.append(weight)    # Записываем результат.
    return(result)

def outfile(path):
    with open("file.txt", "w") as output:
        if len(path) != 1:
            for i in range(len(path)):
                output.write(str(i)+'    '+str(path[i])+'\n')    # Приводим в нужный формат. TSV без заголовка: 2 столбца (вес, количество), разделитель полей - HT, разделитель записей - LF.
        else:
            for i in range(len(path[0])):
                output.write(str(i)+'    '+str(path[0][i])+'\n')

def main(path):
    A,n,size = read(path)
    path = result(A,n,size)
    outfile(path)
    print("Готово!")
    #print("Готово!".format([print(str(w) + "    " +str(path[0][w])) for w in range(len(path[0]))]))
