
import mysql.connector
from mysql.connector import Error
from email.headerregistry import Address
from email.message import EmailMessage
import os
import smtplib

#Create e-mail for defined from/to addresses, subject and text

def create_email_message(from_address, to_address, subject, plaintext, html=None):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(plaintext)
    if html is not None:
        msg.add_alternative(html, subtype='html')
    return msg



#Send HTML message from particular Gmail mailbox with with subject-title
# to defined e-mail address: displayed name [username@domain]

def sendMail(HTML_MESSAGE, display_name, username, domain, title):
#Gmail mailbox details
    email_address = 'testEmail@gmail.com' #gmail  mailbox
    email_password = 'testPsw' #password to the mailbox
#Define recipent
    to_address = (
    Address(display_name, username, domain),)
#Create message with defined from/to  addresss, subject and text    
    msg = create_email_message(
    from_address=email_address,
    to_address=to_address,
    subject=title,
    plaintext="Plain text version.", #plain e-mail text
    html=HTML_MESSAGE    )          #html e-mail text
#Connect to Gmail mail server and send message
    with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email_address, email_password)
        smtp_server.send_message(msg)
    print('Email sent successfully')



#create HTML table raws for AC owned by European companies from SQL query
def createTable1(query):
    cursor.execute(query)
    htmlTable=""""""
    for (TAIL_NUMBER,MODEL_NUMBER,DESCRIPTION,COMPANY_NAME,CODE,COUNTRY_NAME,SDF_COC_002,SDF_COC_003) in cursor:
        if SDF_COC_003=='T':
            rColor='AliceBlue' #color for EU companies
        else:
            rColor='white'
        if SDF_COC_002=='Europe':
            htmlTable=(htmlTable+"""<tr bgcolor="""+rColor+"""><td width="20%">"""+TAIL_NUMBER+"""</td>"""+
                       """<td width="10%">"""+MODEL_NUMBER+"""</td>"""+
                       """<td width="15%">"""+DESCRIPTION+"""</td>"""+
                       """<td width="35%">"""+COMPANY_NAME+"""</td>"""+
                       """<td width="5%">"""+CODE+"""</td>"""+
                       """<td width="15%">"""+COUNTRY_NAME+"""</td></tr>""")
    return htmlTable


#Create HTML table raws for AC owned by non-European companies from SQL query
def createTable2(query):
    cursor.execute(query)
    htmlTable=""""""
    for (TAIL_NUMBER,MODEL_NUMBER,DESCRIPTION,COMPANY_NAME,CODE,COUNTRY_NAME,SDF_COC_002,SDF_COC_003) in cursor:
        if SDF_COC_002!='Europe':
            htmlTable=(htmlTable+"""<tr bgcolor='white'><td width="20%">"""+TAIL_NUMBER+"""</td>"""+
                       """<td width="10%">"""+MODEL_NUMBER+"""</td>"""+
                       """<td width="15%">"""+DESCRIPTION+"""</td>"""+
                       """<td width="35%">"""+COMPANY_NAME+"""</td>"""+
                       """<td width="5%">"""+CODE+"""</td>"""+
                       """<td width="15%">"""+COUNTRY_NAME+"""</td></tr>""")
    return htmlTable


#Script entry point

#Connection to DB   
conn = mysql.connector.connect(host='xx.xxx.xxx.xx',  #server IP
                                       database='test', #database name
                                       user='root', #user name 
                                       password='dbPsw') #password
    
cursor=conn.cursor()

#Define query
query=("SELECT AIRCRAFT.TAIL_NUMBER, MODEL.MODEL_NUMBER, MODEL.DESCRIPTION,"
                           " COMPANIES.COMPANY_NAME, COUNTRY_CODES.CODE, COUNTRY_CODES.COUNTRY_NAME,"
                           " COUNTRY_CODES.SDF_COC_002, COUNTRY_CODES.SDF_COC_003"
       " FROM AIRCRAFT "
       " LEFT JOIN MODEL ON AIRCRAFT.MDL_AUTO_KEY=MODEL.MDL_AUTO_KEY"
       " LEFT JOIN COMPANIES ON AIRCRAFT.CMP_OWNER=COMPANIES.CMP_AUTO_KEY"
       " LEFT JOIN COUNTRY_CODES ON COMPANIES.COC_AUTO_KEY=COUNTRY_CODES.COC_AUTO_KEY"
       " ORDER BY COUNTRY_NAME")


#Compiling E-mail content with tables headers and tables raws created with reateTable1 and reateTable2 functions

HTML_MESSAGE = ("""\
    <html>
    <head>
    <style>
    table, th, td {
    border: 1px solid silver;
    border-collapse: collapse;
    
    }

    td {
    padding: 10px;
    text-align: left;
    }

    th {
    color: white;
    background-color:Gray;
    font-size:120%;
    padding: 15px;
    text-align: left;
    }   
    h1 { 
    font-size: 100%;
    font-weight: bold;
    }
    </style>
    </head>

    <body>
    <h1>AC OWNED BY EUROPEAN COMPANIES</h1>
    <p>legend: <i>light-blue - EU owners</i></p>

    <table style="width:100%">
        <tr>
        <th>Reg Number</th>
        <th>Model Number</th>
        <th>Model Description</th>
        <th>Owner</th>
        <th>Code</th>
        <th>Country</th>
      </tr>"""+createTable1(query)+
    """</table>"""+

    """
    <br />
    <h1>AC OWNED BY NON-EUROPEAN COMPANIES</h1>
    <table style="width:100%">
        <tr>
        <th>Reg Number</th>
        <th>Model Number</th>
        <th>Model Description</th>
        <th>Owner</th>
        <th>Code</th>
        <th>Country</th>
      </tr>"""+createTable2(query)+
    """</table>
    </body>
    </html>
    </p>
    """)

cursor.close()
conn.close()

#Filling E-mail details

#E-mail recepient

display_name='Name'
username='userName'
domain='domain'

#E-mail subject

title='Aircraft report'

#Send e-mail

sendMail(HTML_MESSAGE,display_name,username,domain,title)
