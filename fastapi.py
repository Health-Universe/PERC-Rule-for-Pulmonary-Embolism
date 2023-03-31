from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PERCData(BaseModel):
    age: int
    hr: int
    o2_sat: int
    unilat_leg_swelling: bool
    hemoptysis: bool
    recent_surgery: bool
    hormone_use: bool
    prev_pe_dvt: bool

def calculate_perc(data: PERCData):
    # Criteria for PERC
    criteria = [
        data.age <= 50,
        data.hr < 100,
        data.o2_sat >= 95,
        not data.unilat_leg_swelling,
        not data.hemoptysis,
        not data.recent_surgery,
        not data.hormone_use,
        not data.prev_pe_dvt
    ]
    # If all criteria are met, then PERC rule is negative
    return all(criteria)

@app.post("/perc_rule")
def perc_rule(data: PERCData):
    result = calculate_perc(data)
    if result:
        return {"result": "PERC rule is negative. Low risk for pulmonary embolism."}
    else:
        return {"result": "PERC rule is positive. Further evaluation may be needed."}
