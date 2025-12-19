from fastapi import FastAPI, HTTPException, Path 
# from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel, Field
from typing import Annotated , Optional

app = FastAPI()


# ------------------ Pydantic Model ------------------
class Quote(BaseModel):
    id: Annotated[int, Field(..., description="Quote ID", example=2)]
    author: Annotated[str, Field(..., description="Author name")]
    quote: Annotated[str, Field(..., description="Quote text")]

class UpdateQuote(BaseModel):
    author: Annotated[Optional[str], Field(..., description="Author name")]
    quote: Annotated[Optional[str], Field(..., description="Quote text")]


# ------------------ Load JSON Data ------------------
def load_data():
    with open("assets/quotes_100.json", "r") as file:
        return json.load(file)


def save_data(data):
    with open("assets/quotes_100.json", "w") as file:
        json.dump(data, file, indent=4 , )


# ------------------ Root API ------------------
@app.get("/")
def home():
    return {"message": "FastAPI server is running"}


# ------------------ Get All Quotes ------------------
@app.get("/quotes")
def get_quotes():
    return load_data()


# ------------------ Get Quote By ID ------------------
@app.get("/quotes/{quote_id}")
def get_quote_by_id(
    quote_id: int = Path(..., description="ID of the quote", example=2)
):
    data = load_data()
    for quote in data:
        if quote["id"] == quote_id:
            return quote

    raise HTTPException(status_code=404, detail="Quote not found")


# ------------------ Create New Quote ------------------
@app.post("/quotes", status_code=201)
def create_quote(quote: Quote):
    data = load_data()

    for q in data:
        if q["id"] == quote.id:
            raise HTTPException(
                status_code=400,
                detail="Quote with this ID already exists"
            )

    data.append(quote.model_dump())
    save_data(data)

    return {"message": "Quote created successfully", "quote": quote}


# Upadate end point 
# step --> create a new pydentic model

@app.put("/edit/{quote_id}", status_code=200)
def update_quote(quote_id: int, update_quote: UpdateQuote):
    data = load_data()

    for q in data:
        if q["id"] == quote_id:
            if update_quote.author is not None:
                q["author"] = update_quote.author

            if update_quote.quote is not None:
                q["quote"] = update_quote.quote

            save_data(data)
            return {
                "message": "Quote updated successfully",
                "updated_quote": q
            }

    # ❗ Only runs if loop finishes without finding ID
    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )



@app.delete("/delete/{qeote_id}" , status_code = 200)
def delete_qeote(qeote_id:int):
    data = load_data()

    for index , qeote in enumerate(data):
        if qeote["id"] ==qeote_id:
            deleted_quote = data.pop(index)
            save_data(data)
            return {
                "message": "Quote deleted successfully",
                "deleted_quote": deleted_quote
            }
    raise HTTPException(
        status_code=404,
        detail="Quote not found"
    )








# #  HTTP status code are three digits return by the web server lime fast api  to indicatehe result a clients requestlike from broweser


# # 2xx ---> success 
# # 200 -> ok , 201 created , 204 no content 
# # 3xx ---> redirections
# # 4xx ---> Client Error
# # 400 bad request , 401 unautorised
# # 5xx ---> Server error