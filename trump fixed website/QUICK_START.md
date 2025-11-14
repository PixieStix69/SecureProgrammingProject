# Quick Start Guide - Brute Force Lab

## 🚀 Fast Setup (3 Steps)

### Step 1: Start Flask App
```powershell
cd "c:\Users\Pixie\OneDrive\Documents\YEAR 3\Semester1\SecureProg\Project\trump"
python app.py
```
✅ App runs on: `http://127.0.0.1:5000`

### Step 2: Choose Your Method

#### Option A: Burp Suite (Lab Requirement)
1. Open Burp Suite → Proxy → Open Browser
2. Navigate to `http://127.0.0.1:5000/login`
3. Enter test credentials, turn Intercept ON, click Submit
4. Send to Intruder → Configure Cluster Bomb attack
5. Load `username.txt` and `passwords.txt`
6. Start Attack → Look for Status 302

#### Option B: Python Script (Faster)
```powershell
python brute_force.py
```

#### Option C: Hydra (If installed via WSL)
```bash
hydra -L username.txt -P passwords.txt -s 5000 127.0.0.1 http-post-form "/login:username=^USER^&password=^PASS^:Invalid Credentials"
```

### Step 3: Analyze Results
- ✅ Success = Status 302 + No "Invalid Credentials"
- ❌ Failure = Status 200 + "Invalid Credentials"

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `app.py` | Vulnerable Flask application |
| `username.txt` | List of usernames to test |
| `passwords.txt` | List of passwords to test |
| `brute_force.py` | Python brute-force script |
| `LAB_GUIDE.md` | Complete lab instructions |
| `LAB_ANSWERS.txt` | Answer template for submission |

---

## 🎯 Lab Questions Quick Reference

**Task 1:** Parameters = `username` & `password`, Method = POST

**Q1:** Why identify parameters? → Attack tool needs exact field names

**Q2:** How identify success? → Status 302, different length, no error message

**Q3:** Post-login page? → Profile page at `/profile/<user_id>`

---

## 🔍 What to Look For in Burp Suite

| Column | Failed Login | Successful Login |
|--------|--------------|------------------|
| Status | 200 | 302 |
| Length | ~2145 bytes | ~219 bytes |
| Response | Contains "Invalid Credentials" | Redirect to /profile |

---

## 🛡️ Vulnerabilities Found

1. ❌ SQL Injection (line 143)
2. ❌ No rate limiting
3. ❌ No account lockout
4. ❌ No CAPTCHA
5. ❌ Plaintext passwords

---

## 📝 For Submission

Upload to Brightspace:
- [ ] Completed `LAB_ANSWERS.txt`
- [ ] Screenshots of Burp Suite Intruder results
- [ ] Any modified code files (if you implemented mitigations)

---

## 🆘 Troubleshooting

**"Cannot connect to server"**
→ Make sure Flask app is running: `python app.py`

**"File not found"**
→ Check you're in the correct directory with `pwd` or `cd`

**Burp Suite throttling**
→ Normal with Community Edition, just wait longer

**No successful logins found**
→ Check username.txt and passwords.txt contain valid credentials from database

---

## 💡 Pro Tips

- Run Flask app in one terminal, attack tool in another
- Watch Flask terminal for incoming requests
- Use Ctrl+C to stop the Flask app or Python script
- Check `trump.db` with DB Browser for SQLite to see all users
- The first user "Holmes" with password "MEC15DBF3XD" should work

---

## 🔗 Key URLs

- Login Page: `http://127.0.0.1:5000/login`
- Home Page: `http://127.0.0.1:5000/`
- Admin Panel: `http://127.0.0.1:5000/admin_panel`

---

**Remember:** Only test on your own systems! 🔒
