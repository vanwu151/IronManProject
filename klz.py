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

class MaoPaoklz(Kaolazi):  # 继承kaolazi类
    # def __init__(self, x):
    #     super().__init__(self)
    #     self.lis = self.klz()

    def MaoPao(self, x):
        kl = Kaolazi(self.x)  # 调用父类生成实例k
        kllist = kl.klz()      # 利用实例k生成kaolazi序列klist
        for i in range(0, len(kllist)):
            for j in range(0, len(kllist) - i - 1):
                if kllist[j] > kllist[j+1]:
                    kllist[j], kllist[j+1] = kllist[j+1], kllist[j]
        return kllist


if __name__ == "__main__":
    x = int(input("输入正整数: "))
    k = MaoPaoklz(x)
    klist2 = k.MaoPao(x)
    klist1 = k.klz()
    print("考拉兹序列：{}".format(klist1))
    print("冒泡排序后的考拉兹序列：{}".format(klist2))


