#Importing required libraries to our code
from flask import *
from suds.client import Client

#Setting Flask framework to our site
app = Flask(__name__)

#Needed information for Zarinpal.com
MERCHANT = "fc9510ec-d226-4c1f-b0c1-c3f6210d2f01"  #Required
ZARINPAL = "https://www.zarinpal.com/pg/services/WebGate/wsdl"  #Required

amount = 1000 #Tomans #Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  #Required
email = "example@example.com"  #Optional
mobile = "090000000"  #Optional

#Rendering index.html
@app.route("/")
def home():
    return render_template("index.html")

#Sending a payment request
@app.route("/request/")
def send_request():
    client = Client(ZARINPAL)
    result = client.service.PaymentRequest(MERCHANT,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           str(url_for("verify", _external=True)))
    if result.Status == 100:
        return redirect("https://www.zarinpal.com/pg/StartPay/" + result.Authority)
    else:
        return "Error"

#Cheching if payment was successfull or not
@app.route("/verify/", methods=["GET", "POST"])
def verify():
    client = Client(ZARINPAL)

    #Checking request status 
    if request.args.get("Status") == "OK":
        result = client.service.PaymentVerification(MERCHANT,
                                                    request.args["Authority"],
                                                    amount)
        if result.Status == 100:
            return redirect("/downlowd/")

        elif result.Status == 101:
            return "Transaction submitted : " + str(result.Status)

        else:
            return "Transaction failed. Status: " + str(result.Status)

    else:
        return "Transaction failed or canceled by user"

#Download files after successfull payment
@app.route("/download/")
def download():
    path = "static/files/course-bo-1.docx"

    return send_file(path, as_attachment=True)
