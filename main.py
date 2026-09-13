import re
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Email Validator API")

# רשימת דומיינים זמניים נפוצים
DISPOSABLE_DOMAINS = {"mailinator.com", "10minutemail.com", "tempmail.com", "guerrillamail.com"}

def is_valid_syntax(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

@app.get("/v1/validate")
def validate_email(email: str):
    if not is_valid_syntax(email):
        return {"status": "invalid", "reason": "Syntax error", "is_disposable": False}
    
    domain = email.split("@")[1].lower()
    is_disposable = domain in DISPOSABLE_DOMAINS
    
    return {
        "status": "valid" if not is_disposable else "risky",
        "email": email,
        "domain": domain,
        "is_disposable": is_disposable
    }