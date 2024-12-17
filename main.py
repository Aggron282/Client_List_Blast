import smtplib;
import datetime as dt;
import random;
from chat_ai import *;
import json;

root = "./data/"
file_urls = [f"{root}client_list_gyms.json",f"{root}client_list_hotels.json",f"{root}client_list_salon.json",f"{root}client_list_restaurants.json"]
e_username = "marco@theglassknight.com";
your_birthday = dt.datetime(year=1998,month=2,day=28,hour=4);
client_list = [];

def ShouldBotEmail(target_date):
    now = dt.datetime.now();
    month = now.month;
    year = now.year;
    day = now.day;
    if target_date.month <= month and target_date.day <= day and target_date.year <= year:
        return True;
    else:
        return False;
    

def SaveNextEmailDate(index,client):
    global client_list;
    if len(client_list) > 0:
        client = client_list[index];
        client_date = client["Email Date"].replace("/", "-") 
        for key in client:
            if key == "Email Date":
                old_date = dt.strptime(client_date, "%Y-%m-%d").date()
                two_weeks = dt.timedelta(weeks=2);
                two_weeks_from_now = old_date + two_weeks;
                client[key] = two_weeks_from_now.strftime("%Y-%m-%d");
                client_list[index] = client;


def EmailBlast(file_url):
    with open(file_url) as file:
        client_list = json.load(file);
        counter = 0;
        for client in client_list:
            client = client_list[counter];
            email_date = dt.datetime.strptime(client["Email Date"], "%m/%d/%Y %H:%M:%S");
            name_of_business = "";
            try:
                name_of_business = client["Business Name"];
            except:
                name_of_business = client["Company Name"];
            contact_name = client["Contact"];
            should_email = ShouldBotEmail(email_date);
            SaveNextEmailDate(counter,client);
            if should_email:
                adjs = ["Fun","Professional","Witty","Attention Grabbing","Corporate","Affordable","Competitve","Insightful","Informative","Engaging","Well-Written"];
                chosen_adjs = '';
                for _ in range(0,2):
                    chosen_adjs += " " + random.choice(adjs);
                if len(contact_name) <= 2:
                    contact_name = ""
                chat = chat_with_gpt(f"Write to {contact_name} and their business {name_of_business} about Glass Knight Window Cleaning and make it sound {chosen_adjs} end the email with a call to action about getting a quote for window cleaning from [Marco Khodr] [480-822-0511] [marco@glassknight.com]");
                chat = chat.replace("[Your Name]","Marco Khodr");
                chat = chat.replace("[Your Position]","Founder");
                chat = chat.replace("[Name]","Marco Khodr");
                chat = chat.replace("[Position]","Founder");
                chat = chat.replace("[Role]","Founder");
                chat = chat.replace("[Website URL]","");
                chat = chat.replace("[Phone Number]","");
                chat = chat.replace("[Your Phone Number]","");
                chat = chat.replace("[Your Company]","The Glass Night");
                chat = chat.replace("[Phone]","480-822-0511");
                chat = chat.replace("[Website]","");
                chat = chat.replace("[Business]","The Glass Knight");
                chat = chat.replace("[Your Company Name]","The Glass Knight");
                chat = chat.replace("[Your Contact Information]","marco@theglassknight.com | 480-822-0511");
                body = chat.split("\n",1)[1];
                subject = chat.split(":",1)[1];
                subject = subject.split("\n",1)[0];               
                subject = subject.strip();
                to = client["Email"];
                EmailToSomeone(e_username,to,subject,body);
                counter+=1;

                

def EmailToSomeone(from_who,to_who,subject,body):
    emailer = smtplib.SMTP("smtp.gmail.com");
    emailer.starttls();
    e_password = "mhgj ruhb wuub luhq";
    emailer.login(user=e_username,password=e_password);
    emailer.sendmail(from_who,to_who,f"Subject:{subject}\n\n{body}");


for file_url in file_urls:
    EmailBlast(file_url);
