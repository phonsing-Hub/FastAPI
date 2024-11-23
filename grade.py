# -*- coding: utf-8 -*-
Grade = int(input("Enter score :  ")) 

if Grade > 100:
    print("ปัญญาอ่อนคะแนนเหี้ยไรเกิน 100")
else:
    if Grade >= 80:
        print("เกรด 4")
    elif Grade >= 75:
        print("เกรด 3.5")
    elif Grade >= 70:
        print("เกรด 3")
    elif Grade >= 65:
        print("เกรด 3")
    elif Grade >= 60:
        print("เกรด 2.5")
    elif Grade >= 55:
        print("เกรด 2")
    elif Grade >= 50:
        print("เกรด 1")
    elif Grade < 50:
        print("เกรด 0")
        print("ตกสิไอโง่")
        
input(" Enter Close Program")