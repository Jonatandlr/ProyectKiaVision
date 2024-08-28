import qrcode
con= 1234

while con<=1239:
    roster=con
    id = '65'+str(con)
    qr= qrcode.make (id, error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.save ('A'+str(roster)+'.png',scale=6)
    con=con+1
     