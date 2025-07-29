from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from amazon import get_amazon_deals
import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")

client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"),
                               os.getenv("RAZORPAY_KEY_SECRET")))


@app.get("/")
async def homepage():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/amazon-deals")
async def amazon_deals():
    return get_amazon_deals()


@app.post("/create_order")
async def create_order():
    order = client.order.create({
        "amount": 89,  # 89 paisa
        "currency": "INR",
        "payment_capture": 1
    })
    return order
