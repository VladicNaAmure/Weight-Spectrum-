def read(path):
    # Идея в том, чтобы перевести значения из двоичной системы в десятеричную
    A = []
    with open(path) as f:
        for line in f:
            A.append(line.rstrip())
        n = len(A[0])    # Длина вектора [0]
        size = len(A)    # Количество векторов (строк) в файле
        # Проверим входной файл по критериям
        for i in range(size):
            if len(A[i]) != n:
                first_message = "Размер строк данных имеет разные длины"
                second_message = "Строка: " + str(i)
                return(print(first_message), print(second_message),
                       print("Обработка остановлена..."))
            else:
                for j in range(n):
                    if int(A[i][j]) > 1:
                        first_message = "Значение > 1"
                        second_message = "Строка: " + str(i) + " Позиция: " + str(j)
                        return(print(first_message), print(second_message),
                               print("Обработка остановлена..."))

        for i in range(len(A)):    # Перевод из двоичной системы
            A[i] = int(A[i], 2)
    return(A, n, size)


def result(A, n, size):
    result = []    # Вектор, для записи конечного результата
    for r in range(1):
        basis = []    # Содержит линейно зависимые вектора.
        for j in range(size):
            length = len(bin(A[j])[2:]) - 1
            for i in range(size):
                if (A[i] & 2**length):
                    if i != j:
                        A[i] ^= A[j]
                basis.append(A[i])

    # Производим рассчет биномальных коэффициентов, по найденому базису.
    weight = [0]*(n+1)    # Равен длине вектора (n+1, из-за веса 0).

    z = int(2**(size))
    zc = z ^ (z//2)
    temp = 0
    for k in range(zc):
        if zc % 2 == 1:
            temp ^= basis[k]
            zc // 2
    # Преобразование значений в двоичные и считаем количество совпадений с 1
    location = bin(temp).count('1')
    weight[location] += 1    # Вес, как количество единиц
    # Присваиваем значения, для подсчета длины
    elder, original = zc, (z+1) ^ ((z+1)//2)
    for j in range(z + 1, int(2**(size) * 2)):
        # Ищем первое совпадание с 1 в двоичном значении
        id_j = bin(elder - original)[::-1].find('1')
        temp ^= basis[id_j]
        location = bin(temp).count('1')
        weight[location] += 1
        # Возвращаем значение длины в original для сравния elder
        elder, original = original, (j+1) ^ ((j+1)//2)
    result.append(weight)
    return(result)


def outfile(path):
    with open("file.txt", "w") as output:
        for i in range(len(path[0])):
            output.write(str(i)+'\t'+str(path[0][i])+'\n')


def main(path):
    A, n, size = read(path)
    path = result(A, n, size)
    outfile(path)
    print("Готово!")
