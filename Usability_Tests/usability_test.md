# Usability Test – Fitness App (Signup & Login Features)

## Intro

This usability test focused on two core features of our fitness app: **Signup** and **Login**. Initially, the app only allowed users to sign up and log in using their email and password. We tested this flow with two participants to gather feedback on usability, confusion points, and preferences. Based on the test, we updated our prototype to include third-party login options (Google and Apple), as one participant clearly preferred a faster, single-click login experience.

Participants were asked to think aloud during the test to provide real-time insights into their thought process. Both participants were simulated users representing different types of fitness app users.

---

## Tasks

1. **Task 1:**
   > You just found this fitness app online and want to get started. Try to create an account so you can use it later.

2. **Task 2:**
   > You’ve already created an account earlier. Now you want to log back into the app to check your fitness progress.

---

## Notes

### Participant 1 – Fitness Beginner, Not Tech-Savvy
**Task 1 (Signup):**
- Went straight to "Sign up with Email"
- Paused at password entry: “Do I need a symbol? A number? I’m guessing.”
- Didn’t see any password format hints.
- Didn’t notice lack of third-party login options until after typing.
- Reached home screen after signup.

**Task 2 (Login):**
- Mistyped password once
- No “Show Password” option; struggled to verify
- Eventually logged in

**Comments:**  
> “I didn’t notice any fast login options like Google… I’d probably use that instead.”

---

### Participant 2 – Tech-Savvy College Student
**Task 1 (Signup):**
- Looked for “Continue with Google” immediately
- Complained about having to type email and password
- Expressed annoyance at lack of faster sign-in methods
- Said they'd likely abandon signup in real life

**Task 2 (Login):**
- Wanted to tap “Google” to sign in
- Forced to use email and password again
- Logged in successfully

**Comments:**  
> “Why is there no Google or Apple login? I always use those.”

---

## Feedback

### What went well:
- Form layout was easy to follow
- Fields were labeled clearly

### What didn’t go well:
- Users missed faster login options
- One user felt email/password was outdated
- No password guidance created uncertainty
- No “Show Password” made typing error-prone

---

## Result

### Key Issues Identified:
1. **Missing third-party login options**
   - _Quote:_ “Why is there no Google or Apple login?”
   - **Fix:** Added "Continue with Google" and "Continue with Apple" options to welcome screen

2. **Unclear password requirements**
   - _Quote:_ “Do I need a symbol? A number?”
   - **Fix:** Added password hint text and a strength meter (future update)

3. **No 'Show Password' toggle**
   - _Quote:_ “I can’t tell what I typed.”
   - **Fix:** Added 👁️ icon to toggle password visibility

### Prototype Updates:
- Welcome screen redesigned to place Google/Apple buttons at top
- Signup and login screens now include password visibility toggle
- Signup flow includes guidance for password creation

These updates should improve user experience, reduce friction during account creation, and align the app with common authentication flows seen in modern mobile apps.