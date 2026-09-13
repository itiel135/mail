import dns.resolver
from fastapi import FastAPI, Query

app = FastAPI()

# רשימת דומיינים זמניים נפוצים
DISPOSABLE_DOMAINS = {"tempmail.com", "guerrillamail.com", "10minutemail.com", "mailinator.com"}

def check_mx_record(domain: str) -> bool:
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except Exception:
        return False

@app.get("/v1/validate")
def validate_email(email: str = Query(..., description="Email address to validate")):
    if "@" not in email:
        return {"email": email, "is_valid": False, "reason": "Invalid format"}
    
    user, domain = email.split("@", 1)
    domain = domain.lower()
    
    # בדיקת מייל זמני
    if domain in DISPOSABLE_DOMAINS:
        return {
            "email": email,
            "is_valid": False,
            "is_disposable": True,
            "reason": "Disposable email domain"
        }
    
    # בדיקת רשומות MX (האם הדומיין מסוגל לקבל מיילים)
    has_mx = check_mx_record(domain)
    if not has_mx:
        return {
            "email": email,
            "is_valid": False,
            "is_disposable": False,
            "reason": "No valid MX records found for domain"
        }
        
    return {
        "email": email,
        "is_valid": True,
        "is_disposable": False,
        "reason": "Valid syntax and MX records"
    }
