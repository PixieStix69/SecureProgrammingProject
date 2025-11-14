# Brute-Force Authentication Lab

## 📚 Lab Assignment Overview

This lab demonstrates brute-force attacks against vulnerable authentication systems using Burp Suite and alternative tools. Part of the Secure Programming course assignment.

---

## 📂 Project Structure

```
trump/
├── app.py                  # Vulnerable Flask web application
├── trump.db                # SQLite database with user credentials
├── trump.sql               # Database schema and seed data
├── username.txt            # Username list for brute-force attack
├── passwords.txt           # Password list for brute-force attack
├── brute_force.py          # Python script for automated brute-forcing
├── LAB_GUIDE.md            # Complete lab instructions and answers
├── LAB_ANSWERS.txt         # Answer template for submission
├── QUICK_START.md          # Quick reference guide
└── README.md               # This file
```

---

## 🎯 Learning Objectives

1. Understand how brute-force attacks work
2. Use Burp Suite Intruder for web application testing
3. Identify successful authentication attempts
4. Recognize authentication vulnerabilities
5. Learn mitigation strategies

---

## 🚀 Quick Start

### Prerequisites
- Python 3.x installed
- Flask and dependencies: `pip install flask flask-sqlalchemy requests`
- Burp Suite Community Edition (download from portswigger.net)

### Running the Lab

1. **Start the vulnerable web application:**
   ```powershell
   python app.py
   ```

2. **Choose your attack method:**
   - **Burp Suite** (recommended for lab): See `LAB_GUIDE.md`
   - **Python Script**: `python brute_force.py`
   - **Hydra**: See `QUICK_START.md`

3. **Complete the lab questions** in `LAB_ANSWERS.txt`

---

## 🔐 Vulnerabilities Demonstrated

### 1. SQL Injection
```python
# VULNERABLE CODE (app.py line 143)
query = text(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
```

### 2. No Rate Limiting
- Unlimited login attempts allowed
- No delays between attempts

### 3. No Account Lockout
- Failed attempts don't trigger account locks
- No temporary bans

### 4. No CAPTCHA
- Automated attacks trivial to execute
- No human verification

### 5. Weak Password Storage
- Passwords stored in plaintext
- No hashing or salting

---

## 🛠️ Tools Provided

### 1. Burp Suite Method (Lab Requirement)
- Industry-standard web security testing tool
- Intruder module for automated attacks
- Cluster Bomb attack type for username/password combinations

### 2. Python Script (`brute_force.py`)
- Automated brute-force testing
- Clear output showing all attempts
- Identifies successful logins

### 3. Hydra (Optional)
- Command-line brute-force tool
- Fast and efficient
- Requires WSL or Cygwin on Windows

---

## 📊 Expected Results

### Database Contains:
- 100 users with various usernames
- Passwords in format like: `MEC15DBF3XD`, `PVO84UPH4JN`, etc.

### Sample Valid Credentials:
| Username | Password |
|----------|----------|
| Holmes | MEC15DBF3XD |
| Louis | PVO84UPH4JN |
| Colin | UBN90KIN1MZ |
| Cameron | WPX87QUO0TE |

### Success Indicators:
- HTTP Status: **302** (redirect)
- Response Length: **~219 bytes**
- No "Invalid Credentials" message
- Redirect to: `/profile/<user_id>`

---

## 📝 Lab Questions

### Task 1
**Q:** Identify the parameters and HTTP method used for authentication.  
**A:** Parameters: `username` and `password`, Method: `POST`

### Question 1
**Q:** Why is it essential to correctly identify the parameters?  
**A:** The attack tool needs exact field names to modify during brute-force attempts.

### Question 2
**Q:** How did you identify successful login attempts?  
**A:** By analyzing status codes (302 vs 200), response lengths, and absence of error messages.

### Question 3
**Q:** What page are you on after successful login?  
**A:** Profile page at `/profile/<user_id>`

---

## 🛡️ Mitigation Strategies

### Implement These Security Controls:

1. **Rate Limiting**
   ```python
   from flask_limiter import Limiter
   @limiter.limit("5 per minute")
   ```

2. **Account Lockout**
   - Lock after 3-5 failed attempts
   - Temporary lockout (15-30 minutes)

3. **CAPTCHA**
   - After 2-3 failed attempts
   - Use reCAPTCHA or similar

4. **Strong Password Policy**
   - Minimum 12 characters
   - Complexity requirements
   - No common passwords

5. **Multi-Factor Authentication (MFA)**
   - SMS codes
   - Authenticator apps
   - Email verification

6. **Parameterized Queries**
   ```python
   query = text("SELECT * FROM users WHERE username = :username AND password = :password")
   user = db.session.execute(query, {'username': username, 'password': password})
   ```

7. **Password Hashing**
   ```python
   from werkzeug.security import generate_password_hash, check_password_hash
   hashed = generate_password_hash(password)
   ```

---

## 📤 Submission Requirements

Upload to Brightspace:
1. Completed `LAB_ANSWERS.txt` with your responses
2. Screenshots of Burp Suite showing:
   - Intercepted request
   - Intruder configuration
   - Attack results with successful login highlighted
3. Any modified code files (if you implemented mitigations)

---

## ⚠️ Important Notes

- **Only test on your own systems or with explicit permission**
- This is for educational purposes only
- Unauthorized access to computer systems is illegal
- The vulnerabilities demonstrated are intentional for learning

---

## 🔗 Useful Resources

- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't connect to server | Ensure Flask app is running: `python app.py` |
| Import errors | Install dependencies: `pip install flask flask-sqlalchemy requests` |
| Database not found | Delete `trump.db` and restart app to recreate |
| Burp Suite throttling | Normal with Community Edition, be patient |
| No successful logins | Verify `username.txt` and `passwords.txt` contain valid credentials |

---

## 📧 Support

For questions about this lab:
1. Check `LAB_GUIDE.md` for detailed instructions
2. Review `QUICK_START.md` for quick reference
3. Contact your instructor or TA

---

## 📄 License

This project is for educational purposes as part of the Secure Programming course.

---

**Last Updated:** November 2025  
**Course:** Secure Programming (Year 3, Semester 1)  
**Assignment:** Brute-Force Authentication Lab
