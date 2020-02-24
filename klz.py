class Kaolazi:
    def __init__(self, x):
        self.x = x

    def cal(self):
        if self.x % 2 == 0:
            r = self.x / 2
        else:
            r = self.x * 3 + 1
        return r

    def klz(self):
        klzList = []
        # x = int(input("输入正整数: "))
        while True:
            self.x = self.cal()
            klzList.append(self.x)
            if self.x == 1:
                break
        return klzList

def MaoPao(lis):
    for i in range(0, len(lis)):
        print("i = " + str(i))
        for j in range(0, len(lis) - i - 1):
            print("j = " + str(j))
            if lis[j] > lis[j+1]:
                lis[j], lis[j+1] = lis[j+1], lis[j]
    return lis


if __name__ == "__main__":
    x = int(input("输入正整数: "))
    k = Kaolazi(x)
    klist = k.klz()
    print(klist)
    print(MaoPao(klist))

