import time

import datetime

coeff = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]

check = [1,0,'X',9,8,7,6,5,4,3,2]

while True:

    today = datetime.datetime.now().strftime('%Y%m%d')

    year = time.localtime(time.time())[0]

    ID = input('请输入身份证号（输入Q结束）：')

    if ID != 'Q':

        if len(ID) == 18:

            if ID[0:17].isdigit():

                if int(ID[6:10]) in range(1900, year + 1):

                    if int(ID[6:14])  <= int(today):

                        try:

                            time.strptime(ID[6:14], "%Y%m%d")

                            tmp = 0

                            for i in range(0,17):

                                tmp = tmp + int(ID[i]) * coeff[i]

                            mod = tmp % 11

                            sex = '女' if int(ID[-2])%2 == 0 else '男'

                            if str(check[mod]) == ID[-1]:

                                print(f'\t********此身份证号校验无误，性别为[{sex}]********')

                            else:

                                print(f'\txxxx身份证末位校验码"{ID[-1]}"不正确（应为"{check[mod]}"）xxxx')

                        except:

                            print(f'\t出生日期[{ID[6:14]}:年月日]不是合法的格式，请重新输入！')

                    else:

                        print(f'\t出生日期[{ID[6:14]}]不应晚于当前日期[{today}]，请重新输入！')

                else:

                    print(f'\t出生年份{ID[6:10]}错误，应介于[1900--{year}]年之间，请重新输入！')

            else:

                print('\t身份证前17位应全部为数字，请重新输入！')

        else:

            print('\t身份证长度应为18位，请重新输入。')

    else:

        print('\t谢谢使用，再见！')

        break