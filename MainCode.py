df=pd.read_excel("")#Enter YOUR DATASET PATH where ever required in the code
index=20#some out of range value
j=1
#Stage 1(User Validity)
#--Asking user for either name or user id.If it crosses the maximum tries of invalid entry(i.e 3), block the status of the account or else ask for account number.
while j!=4:
    info=input("Enter the user Full name or User Id:").strip()
    for i in range(10):#change values if data increases/or do len of df
        try:
            if (df.loc[i,'User Id']==int(info)):#detecting id
                index=i#string index
                break
            else:
                continue
        except:
            if df.loc[i,'Full Name'].lower()==info.lower():  #detecting name
                index=i
                break
            else:
                continue
    else:
        print("Invalid User!Try entering correct details\n")
        j+=1
        continue
    break    
else:
    print("Sorry,Too many Wrong Attempts!")       

if index!=20:
    print("\n")
    print("\t\t\tWelcome User-{}😊!\n".format(df.loc[index,"Full Name"]))#greeting user
    i=1
    while i!=4:
        accountno=input("Enter the account number associated with you:").strip()#getting the account number
        if df.loc[index,"A/C No."]==accountno:
            break                 
        else:
            print("You have entered invalid/wrong account number(Try again)\n")
            i+=1 #chance starts
            continue
    else:
        df.loc[index,"A/C Status"]="Blocked"
        print("\t\t      Sorry,Too many Wrong Attempts\n\t\t\t   Account Blocked")
    df.to_excel("",index=False) #updating the dataset
    
#Stage 2 (OTP Generation and Validity)  
#OTP generation using MIME,SMTP

if df.loc[index,"A/C Status"]!="Blocked":
    str1=""
    a=np.random.randint(1,10,size=(4,))  #otp gerneration
    for i in a:
        str1=str1+str(i)
    #print("Generating an OTP........")
    fromaddr=""# Enter your email id
    toaddr=df.loc[index,"User Email"]
    msg=MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    msg['Subject']='Your OTP for Online Usage Access'

    body="Your One Time Password(OTP) is {}\nPlease Don't share this OTP with Anyone.".format(str1)
    msg.attach(MIMEText(body,"plain"))

    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(fromaddr,"YOUR EMAIL ID PASSWORD")
    text=msg.as_string()
    server.sendmail(fromaddr,toaddr,text)
    server.quit()
    print("\nOTP for online banking is sended to your respective Email id.")

    i=1
    while i!=4:
        otp=input("Enter the OTP:")     #entering the otp
        if str1==otp:
            print("\t\t\t  OTP Confirmed!🙂\n")
            break
        else:
            print("You have entered wrong OTP(Try again)\n")
            i+=1
            continue
    else:
        df.loc[index,"A/C Status"]="Blocked"
        print("\t\t      Sorry,Too many Wrong Attempts\n\t\t\t   Account Blocked")   
    df.to_excel("",index=False) #updating the dataset
    
#Stage 3 (Choice of Transaction) 

if df.loc[index,"A/C Status"]!="Blocked": 
    i=1
    while i!=4:
        trans=input("Do u like to Credit(C) or Debit(D) money:").strip()  #entering the choice of transaction
        if trans.lower()=="c":
            print("\t\t\t Current Balance:Rs",df.loc[index,"A/C Balance"])
            break
        elif trans.lower()=="d":
            print("\t\t\t Current Balance:Rs",df.loc[index,"A/C Balance"])
            break
        else:
            print("Invalid Input!(Try Again)")    
            i+=1
            continue
    else:
        df.loc[index,"A/C Status"]="Blocked"
        print("\t\t      Sorry,Too many Wrong Attempts\n\t\t\t   Account Blocked")
    df.to_excel("",index=False) #updating the dataset     
if df.loc[index,"A/C Status"]!="Blocked":
    if trans.lower()=='c':
        p="Credit"
        amt=int(input("\nEnter the amount to be Credited:"))        #enter the amount to be credited
        df.loc[index,"A/C Balance"]=df.loc[index,"A/C Balance"]+amt
        print("\t\t  Current Balance after Credition:Rs",df.loc[index,"A/C Balance"])
    elif trans.lower()=='d':
        p="Debit"
        amt=int(input("\nEnter the amount to be Debited:"))          #enter the amount to be debited
        df.loc[index,"A/C Balance"]=df.loc[index,"A/C Balance"]-amt
        print("\t\t  Current Balance after Debition:Rs",df.loc[index,"A/C Balance"])  
    
    df.to_excel("",index=False) #updating the dataset
    print("\n\t\tSuccessfull Transaction of Rs.%d is completed."%amt) 
    print("\nMini Statement:")
    print("\n")
    curr=datetime.datetime.now()
    date=str(curr.day)+"/"+str(curr.month)+"/"+str(curr.year)
    time=str(curr.hour)+":"+str(curr.minute)+":"+str(curr.second)
    print("\t\t\tDate          Time          USER   ID\t\t")
    print("\t\t\t{0:5s}     {1:7s}      {2:8d}\t\t".format(date,time,df.loc[index,"User Id"]))
    print("\n\t\t\tTransaction Amount({}):Rs {}\t\t".format(p,amt))


    print("\n\t\t\tA/C Number.{}\t\t\t".format("XXXXXXXXXXXXX" + df.loc[index,"A/C No."][-4:]))
    print("\t\t\tAVAIL BAL:Rs.{}\t\t\t\t".format(df.loc[index,"A/C Balance"]))
    
